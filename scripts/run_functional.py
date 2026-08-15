#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

RUNNER_SCOPE = "COOPERATIVE_OR_BUGGY_IMPLEMENTATION"
RUNNER_LIMITATION = "NOT_A_SECURITY_SANDBOX"
OUT_OF_SCOPE = "HOSTILE_PROCESS_INTERNAL_TAMPERING"

OBSERVATION_PROTOCOL = "r2-functional-observation-v2"
VERDICT_PROTOCOL = "r2-functional-verdict-v2"
DEFAULT_TIMEOUT_SECONDS = 5.0
MAX_OBSERVATION_BYTES = 65536
EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

CASES: tuple[tuple[str, int, int], ...] = (
    ("valid_1000_3", 1000, 3),
    ("zero_people", 1000, 0),
    ("negative_amount", -1, 2),
)

# This source is executed by a separate Python interpreter. It contains no
# acceptance verdict logic. Its only role is to execute the implementation and
# return structured observations through a dedicated file descriptor.
WORKER_SOURCE = r'''from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


OBSERVATION_PROTOCOL = "r2-functional-observation-v2"
CASES = (
    ("valid_1000_3", 1000, 3),
    ("zero_people", 1000, 0),
    ("negative_amount", -1, 2),
)


def main() -> int:
    implementation = Path(sys.argv[1]).resolve()
    observation_fd = int(sys.argv[2])

    # Capture primitives before the implementation is imported. The worker
    # deliberately does not import json and has no PASS/FAIL authority.
    safe_repr = repr
    safe_write = os.write
    safe_close = os.close
    safe_type = type
    safe_getattr = getattr
    safe_callable = callable
    safe_str = str
    safe_all = all
    safe_len = len
    safe_memoryview = memoryview
    safe_list_type = list
    safe_int_type = int
    safe_protocol = OBSERVATION_PROTOCOL
    safe_cases = CASES

    def write_all(data: bytes) -> None:
        view = safe_memoryview(data)
        offset = 0
        while offset < safe_len(view):
            written = safe_write(observation_fd, view[offset:])
            if written <= 0:
                raise RuntimeError("No se pudo escribir la observación")
            offset += written

    def exception_observation(exc: BaseException) -> dict[str, str]:
        return {
            "exception_type": safe_type(exc).__name__,
            "exception_message": safe_str(exc),
        }

    def observe_return(case_id: str, result: object) -> dict[str, object]:
        result_type = safe_type(result)
        exact_list = result_type is safe_list_type
        if not exact_list:
            return {
                "case_id": case_id,
                "outcome": "RETURNED",
                "result_type": result_type.__name__,
                "result_is_exact_list": False,
                "items_all_exact_ints": None,
                "items": None,
            }

        items_all_exact_ints = safe_all(
            safe_type(item) is safe_int_type for item in result
        )
        items = [item for item in result] if items_all_exact_ints else None
        return {
            "case_id": case_id,
            "outcome": "RETURNED",
            "result_type": "list",
            "result_is_exact_list": True,
            "items_all_exact_ints": items_all_exact_ints,
            "items": items,
        }

    payload: dict[str, object]
    if not implementation.is_file():
        payload = {
            "protocol": safe_protocol,
            "worker_status": "LOAD_ERROR",
            "error": {
                "exception_type": "FileNotFoundError",
                "exception_message": f"No existe el archivo: {implementation}",
            },
        }
    else:
        try:
            spec = importlib.util.spec_from_file_location(
                "r2_splitter_implementation", implementation
            )
            if spec is None or spec.loader is None:
                raise RuntimeError(
                    f"No se pudo crear un loader para {implementation}"
                )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            candidate = safe_getattr(module, "split_expense", None)
            if not safe_callable(candidate):
                raise RuntimeError(
                    "La implementación no expone "
                    "split_expense(amount_cents, people)"
                )
            split_expense = candidate
        except Exception as exc:
            payload = {
                "protocol": safe_protocol,
                "worker_status": "LOAD_ERROR",
                "error": exception_observation(exc),
            }
        else:
            observations: list[dict[str, object]] = []
            for case_id, amount_cents, people in safe_cases:
                try:
                    result = split_expense(amount_cents, people)
                except Exception as exc:
                    observation = {
                        "case_id": case_id,
                        "outcome": "RAISED",
                        **exception_observation(exc),
                    }
                else:
                    observation = observe_return(case_id, result)
                observations.append(observation)

            payload = {
                "protocol": safe_protocol,
                "worker_status": "COMPLETE",
                "cases": observations,
            }

    encoded = (safe_repr(payload) + "\n").encode("utf-8")
    write_all(encoded)
    safe_close(observation_fd)
    return 0


raise SystemExit(main())
'''


def encode_verdict(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def emit_verdict(payload: dict[str, Any]) -> None:
    sys.stdout.buffer.write(encode_verdict(payload))
    sys.stdout.buffer.flush()


def verdict(
    status: str,
    reason_code: str,
    message: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "protocol": VERDICT_PROTOCOL,
        "status": status,
        "reason_code": reason_code,
        "message": message,
    }
    if details:
        payload["details"] = details
    return payload


def kill_process_group(pgid: int) -> None:
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return

    time.sleep(0.05)
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        return


def read_observation(fd: int) -> tuple[bytes, bool]:
    chunks: list[bytes] = []
    total = 0
    too_large = False
    while True:
        chunk = os.read(fd, 8192)
        if not chunk:
            break
        previous_total = total
        total += len(chunk)
        if previous_total < MAX_OBSERVATION_BYTES:
            available = MAX_OBSERVATION_BYTES - previous_total
            chunks.append(chunk[:available])
        if total > MAX_OBSERVATION_BYTES:
            too_large = True
    return b"".join(chunks), too_large


def protocol_failure(
    reason_code: str,
    message: str,
    *,
    implementation: Path,
    details: dict[str, Any] | None = None,
) -> int:
    merged_details = {
        "implementation": str(implementation),
        "judge_process": "controller",
        "worker_role": "observations_only",
        "worker_interpreter_separate": True,
        "runner_scope": RUNNER_SCOPE,
        "runner_limitation": RUNNER_LIMITATION,
        "out_of_scope": OUT_OF_SCOPE,
    }
    if details:
        merged_details.update(details)
    emit_verdict(
        verdict(
            "FAIL",
            reason_code,
            message,
            details=merged_details,
        )
    )
    return EXIT_FAIL


def contains_authority_keys(value: object) -> bool:
    forbidden = {"status", "reason_code", "verdict"}
    if isinstance(value, dict):
        if any(key in forbidden for key in value):
            return True
        return any(contains_authority_keys(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_authority_keys(item) for item in value)
    return False


def validate_raised_case(case: dict[str, Any], case_id: str) -> None:
    expected_keys = {
        "case_id",
        "outcome",
        "exception_type",
        "exception_message",
    }
    if set(case) != expected_keys:
        raise ValueError(f"schema RAISED inesperado en {case_id}")
    if case["case_id"] != case_id or case["outcome"] != "RAISED":
        raise ValueError(f"identidad RAISED inesperada en {case_id}")
    if not isinstance(case["exception_type"], str) or not case["exception_type"]:
        raise ValueError(f"exception_type inválido en {case_id}")
    if not isinstance(case["exception_message"], str):
        raise ValueError(f"exception_message inválido en {case_id}")


def validate_returned_case(case: dict[str, Any], case_id: str) -> None:
    expected_keys = {
        "case_id",
        "outcome",
        "result_type",
        "result_is_exact_list",
        "items_all_exact_ints",
        "items",
    }
    if set(case) != expected_keys:
        raise ValueError(f"schema RETURNED inesperado en {case_id}")
    if case["case_id"] != case_id or case["outcome"] != "RETURNED":
        raise ValueError(f"identidad RETURNED inesperada en {case_id}")
    if not isinstance(case["result_type"], str) or not case["result_type"]:
        raise ValueError(f"result_type inválido en {case_id}")
    if type(case["result_is_exact_list"]) is not bool:
        raise ValueError(f"result_is_exact_list inválido en {case_id}")
    exact_list = case["result_is_exact_list"]
    if exact_list:
        if case["result_type"] != "list":
            raise ValueError(f"result_type inconsistente en {case_id}")
        if type(case["items_all_exact_ints"]) is not bool:
            raise ValueError(f"items_all_exact_ints inválido en {case_id}")
        if case["items_all_exact_ints"]:
            if not isinstance(case["items"], list):
                raise ValueError(f"items inválido en {case_id}")
            if any(type(item) is not int for item in case["items"]):
                raise ValueError(f"items contiene valores no enteros en {case_id}")
        elif case["items"] is not None:
            raise ValueError(
                f"items debe ser null para elementos no enteros en {case_id}"
            )
    elif case["items_all_exact_ints"] is not None or case["items"] is not None:
        raise ValueError(f"campos de lista inesperados en {case_id}")


def parse_observation(
    *,
    returncode: int,
    observation: bytes,
    observation_too_large: bool,
    worker_stdout: bytes,
    worker_stderr: bytes,
    implementation: Path,
) -> tuple[dict[str, Any] | None, int | None]:
    common = {
        "worker_exit_code": returncode,
        "observation_bytes": len(observation),
        "worker_stdout_bytes": len(worker_stdout),
        "worker_stderr_bytes": len(worker_stderr),
    }

    if returncode != 0:
        return None, protocol_failure(
            "WORKER_NONZERO_EXIT",
            "El worker terminó sin completar el protocolo de observación.",
            implementation=implementation,
            details=common,
        )

    if observation_too_large:
        return None, protocol_failure(
            "OBSERVATION_TOO_LARGE",
            "El worker excedió el tamaño máximo del protocolo de observación.",
            implementation=implementation,
            details=common,
        )

    if not observation:
        return None, protocol_failure(
            "MISSING_OBSERVATION",
            "El worker terminó con exit 0 sin emitir observaciones obligatorias.",
            implementation=implementation,
            details=common,
        )

    try:
        decoded = observation.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        return None, protocol_failure(
            "INVALID_OBSERVATION_ENCODING",
            "La observación del worker no es UTF-8 válida.",
            implementation=implementation,
            details={**common, "error": str(exc)},
        )

    lines = decoded.splitlines()
    if len(lines) != 1 or not decoded.endswith("\n"):
        return None, protocol_failure(
            "INVALID_OBSERVATION_COUNT",
            "El worker debe emitir exactamente una observación terminada en LF.",
            implementation=implementation,
            details={**common, "observed_line_count": len(lines)},
        )

    try:
        payload = ast.literal_eval(lines[0])
    except (SyntaxError, ValueError) as exc:
        return None, protocol_failure(
            "INVALID_OBSERVATION_LITERAL",
            "La observación del worker no es un literal estructurado válido.",
            implementation=implementation,
            details={**common, "error": str(exc)},
        )

    if not isinstance(payload, dict):
        return None, protocol_failure(
            "INVALID_OBSERVATION_TYPE",
            "La observación del worker debe ser un objeto estructurado.",
            implementation=implementation,
            details=common,
        )

    if contains_authority_keys(payload):
        return None, protocol_failure(
            "WORKER_ATTEMPTED_VERDICT",
            "El worker intentó incluir campos reservados al juez del controlador.",
            implementation=implementation,
            details=common,
        )

    if payload.get("protocol") != OBSERVATION_PROTOCOL:
        return None, protocol_failure(
            "INVALID_OBSERVATION_PROTOCOL",
            "La observación no declara el protocolo esperado.",
            implementation=implementation,
            details=common,
        )

    worker_status = payload.get("worker_status")
    if worker_status == "LOAD_ERROR":
        if set(payload) != {"protocol", "worker_status", "error"}:
            return None, protocol_failure(
                "INVALID_OBSERVATION_SCHEMA",
                "La observación LOAD_ERROR no cumple el schema cerrado.",
                implementation=implementation,
                details=common,
            )
        error = payload.get("error")
        if not isinstance(error, dict) or set(error) != {
            "exception_type",
            "exception_message",
        }:
            return None, protocol_failure(
                "INVALID_OBSERVATION_SCHEMA",
                "El error de carga no cumple el schema cerrado.",
                implementation=implementation,
                details=common,
            )
        if not isinstance(error["exception_type"], str) or not error[
            "exception_type"
        ]:
            return None, protocol_failure(
                "INVALID_OBSERVATION_SCHEMA",
                "exception_type de carga inválido.",
                implementation=implementation,
                details=common,
            )
        if not isinstance(error["exception_message"], str):
            return None, protocol_failure(
                "INVALID_OBSERVATION_SCHEMA",
                "exception_message de carga inválido.",
                implementation=implementation,
                details=common,
            )
        return payload, None

    if worker_status != "COMPLETE":
        return None, protocol_failure(
            "INVALID_WORKER_STATUS",
            "La observación no contiene un worker_status reconocido.",
            implementation=implementation,
            details=common,
        )

    if set(payload) != {"protocol", "worker_status", "cases"}:
        return None, protocol_failure(
            "INVALID_OBSERVATION_SCHEMA",
            "La observación COMPLETE no cumple el schema cerrado.",
            implementation=implementation,
            details=common,
        )

    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != len(CASES):
        return None, protocol_failure(
            "INVALID_OBSERVATION_SCHEMA",
            "La observación no contiene exactamente los casos requeridos.",
            implementation=implementation,
            details=common,
        )

    expected_ids = [case_id for case_id, _, _ in CASES]
    observed_ids: list[object] = []
    try:
        for index, case in enumerate(cases):
            if not isinstance(case, dict):
                raise ValueError(f"case no es objeto en índice {index}")
            case_id = expected_ids[index]
            observed_ids.append(case.get("case_id"))
            outcome = case.get("outcome")
            if outcome == "RAISED":
                validate_raised_case(case, case_id)
            elif outcome == "RETURNED":
                validate_returned_case(case, case_id)
            else:
                raise ValueError(f"outcome inválido en {case_id}")
    except ValueError as exc:
        return None, protocol_failure(
            "INVALID_OBSERVATION_SCHEMA",
            "Las observaciones de casos no cumplen el schema cerrado.",
            implementation=implementation,
            details={
                **common,
                "error": str(exc),
                "observed_case_ids": observed_ids,
            },
        )

    return payload, None


def controller_verdict(
    observation: dict[str, Any],
    *,
    implementation: Path,
    timeout_seconds: float,
    worker_stdout: bytes,
    worker_stderr: bytes,
) -> tuple[dict[str, Any], int]:
    base_details = {
        "implementation": str(implementation),
        "judge_process": "controller",
        "worker_role": "observations_only",
        "worker_interpreter_separate": True,
        "runner_scope": RUNNER_SCOPE,
        "runner_limitation": RUNNER_LIMITATION,
        "out_of_scope": OUT_OF_SCOPE,
        "timeout_seconds": timeout_seconds,
        "worker_stdout_bytes": len(worker_stdout),
        "worker_stderr_bytes": len(worker_stderr),
    }

    if observation["worker_status"] == "LOAD_ERROR":
        return (
            verdict(
                "ERROR",
                "IMPLEMENTATION_LOAD_ERROR",
                "No se pudo cargar la implementación en el worker.",
                details={**base_details, **observation["error"]},
            ),
            EXIT_ERROR,
        )

    cases = {case["case_id"]: case for case in observation["cases"]}
    valid = cases["valid_1000_3"]

    if valid["outcome"] == "RAISED":
        return (
            verdict(
                "FAIL",
                "VALID_CASE_RAISED",
                "La implementación lanzó una excepción para 1000 céntimos y 3 personas.",
                details={**base_details, **valid},
            ),
            EXIT_FAIL,
        )

    if not valid["result_is_exact_list"]:
        return (
            verdict(
                "FAIL",
                "INVALID_RESULT_TYPE",
                "El resultado debe ser una lista exacta de céntimos enteros.",
                details={**base_details, **valid},
            ),
            EXIT_FAIL,
        )

    if not valid["items_all_exact_ints"]:
        return (
            verdict(
                "FAIL",
                "INVALID_PART_TYPE",
                "Todas las partes deben ser enteros exactos en céntimos.",
                details={**base_details, **valid},
            ),
            EXIT_FAIL,
        )

    parts = valid["items"]
    assert isinstance(parts, list)

    if len(parts) != 3:
        return (
            verdict(
                "FAIL",
                "INVALID_PART_COUNT",
                "El resultado debe contener exactamente una parte por persona.",
                details={
                    **base_details,
                    "expected": 3,
                    "observed": len(parts),
                    "parts": parts,
                },
            ),
            EXIT_FAIL,
        )

    observed_total = sum(parts)
    if observed_total != 1000:
        return (
            verdict(
                "FAIL",
                "TOTAL_NOT_CONSERVED",
                "La suma de las partes no conserva exactamente el importe original.",
                details={
                    **base_details,
                    "expected_total_cents": 1000,
                    "observed_total_cents": observed_total,
                    "parts": parts,
                },
            ),
            EXIT_FAIL,
        )

    expected_distribution = [334, 333, 333]
    if parts != expected_distribution:
        return (
            verdict(
                "FAIL",
                "DISTRIBUTION_MISMATCH",
                "La distribución no coincide con la demo aceptada.",
                details={
                    **base_details,
                    "expected": expected_distribution,
                    "observed": parts,
                },
            ),
            EXIT_FAIL,
        )

    checks = [
        {"name": "total_conservation", "result": "PASS"},
        {"name": "accepted_demo_distribution", "result": "PASS"},
    ]

    for case_id, check_name in (
        ("zero_people", "zero_people_rejected"),
        ("negative_amount", "negative_amount_rejected"),
    ):
        case = cases[case_id]
        if case["outcome"] == "RETURNED":
            return (
                verdict(
                    "FAIL",
                    "INVALID_INPUT_ACCEPTED",
                    "La implementación aceptó una entrada que debía rechazar.",
                    details={**base_details, "check": check_name, **case},
                ),
                EXIT_FAIL,
            )
        if case["exception_type"] != "ValueError":
            return (
                verdict(
                    "FAIL",
                    "WRONG_REJECTION_TYPE",
                    "La entrada inválida se rechazó con una excepción no prevista.",
                    details={**base_details, "check": check_name, **case},
                ),
                EXIT_FAIL,
            )
        if not case["exception_message"].strip():
            return (
                verdict(
                    "FAIL",
                    "UNCLEAR_REJECTION",
                    "La entrada inválida se rechazó sin un mensaje claro.",
                    details={**base_details, "check": check_name, **case},
                ),
                EXIT_FAIL,
            )
        checks.append(
            {
                "name": check_name,
                "result": "PASS",
                "exception_type": case["exception_type"],
                "exception_message": case["exception_message"],
            }
        )

    return (
        verdict(
            "PASS",
            "ALL_FUNCTIONAL_CHECKS_PASSED",
            "La implementación cumple la demo funcional mínima.",
            details={**base_details, "checks": checks},
        ),
        EXIT_PASS,
    )


def controller_main(implementation: Path, timeout_seconds: float) -> int:
    if timeout_seconds <= 0:
        emit_verdict(
            verdict(
                "ERROR",
                "INVALID_TIMEOUT",
                "El timeout debe ser mayor que cero.",
            )
        )
        return EXIT_ERROR

    implementation = implementation.resolve()
    runner = Path(__file__).resolve()
    observation_read, observation_write = os.pipe()
    command = [
        sys.executable,
        "-I",
        "-B",
        "-c",
        WORKER_SOURCE,
        str(implementation),
        str(observation_write),
    ]

    process: subprocess.Popen[bytes] | None = None
    worker_stdout = b""
    worker_stderr = b""
    observation = b""
    observation_too_large = False
    timed_out = False

    try:
        process = subprocess.Popen(
            command,
            cwd=runner.parent.parent,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            pass_fds=(observation_write,),
        )
        os.close(observation_write)
        observation_write = -1

        try:
            worker_stdout, worker_stderr = process.communicate(
                timeout=timeout_seconds
            )
        except subprocess.TimeoutExpired:
            timed_out = True
            kill_process_group(process.pid)
            worker_stdout, worker_stderr = process.communicate()

        observation, observation_too_large = read_observation(observation_read)
    except OSError as exc:
        if process is not None and process.poll() is None:
            kill_process_group(process.pid)
            process.communicate()
        emit_verdict(
            verdict(
                "ERROR",
                "WORKER_START_ERROR",
                "No se pudo iniciar o leer el worker.",
                details={
                    "implementation": str(implementation),
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                },
            )
        )
        return EXIT_ERROR
    finally:
        if observation_write >= 0:
            os.close(observation_write)
        os.close(observation_read)

    assert process is not None

    if timed_out:
        return protocol_failure(
            "WORKER_TIMEOUT",
            "El worker no completó las observaciones dentro del límite.",
            implementation=implementation,
            details={
                "timeout_seconds": timeout_seconds,
                "worker_exit_code": process.returncode,
                "observation_bytes": len(observation),
                "worker_stdout_bytes": len(worker_stdout),
                "worker_stderr_bytes": len(worker_stderr),
            },
        )

    payload, failure_exit = parse_observation(
        returncode=process.returncode,
        observation=observation,
        observation_too_large=observation_too_large,
        worker_stdout=worker_stdout,
        worker_stderr=worker_stderr,
        implementation=implementation,
    )
    if failure_exit is not None:
        return failure_exit
    assert payload is not None

    final_verdict, exit_code = controller_verdict(
        payload,
        implementation=implementation,
        timeout_seconds=timeout_seconds,
        worker_stdout=worker_stdout,
        worker_stderr=worker_stderr,
    )
    emit_verdict(final_verdict)
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Runner funcional con worker de observación y juez en un "
            "intérprete controlador separado."
        )
    )
    parser.add_argument(
        "--implementation",
        required=True,
        type=Path,
        help="Archivo Python que expone split_expense(amount_cents, people).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Límite para el worker de observación.",
    )
    args = parser.parse_args()
    return controller_main(args.implementation, args.timeout_seconds)


if __name__ == "__main__":
    sys.exit(main())
