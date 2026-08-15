#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2
NORMAL_PR_CLASS = "B"

PINNED_SHA256 = {'scripts/risk_floor.py': 'e3be85d4c8d64ea8f24f74b3033dac5d127635a5aba3398220f36c0cab0bd283', 'policy/risk_floors.json': 'd68240ee3b13bd5f10ccce10dfd2da9af038495d9a7adeb6fe411ab5622b8a1b', 'scripts/run_functional.py': 'd08fe9bd6188508ae9fc181a6806ce7835a16ab48ce749b1de283655dce2b32f', 'tests/fixtures/good_splitter.py': '1c86e6843ad8ab5e07d2fac2575f53bfdbaa695646dde5211c68cda732b45827', 'tests/fixtures/bad_splitter.py': 'b9989b0e62c55b54528a87f26f835a137f52b2e5d76f6bf0608482351a50d3ce'}
GATE_REL = "scripts/base_gate.py"
CHECKER_REL = "scripts/risk_floor.py"
POLICY_REL = "policy/risk_floors.json"
RUNNER_REL = "scripts/run_functional.py"
GOOD_REL = "tests/fixtures/good_splitter.py"
BAD_REL = "tests/fixtures/bad_splitter.py"


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(args: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_bytes(repo: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_text(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], cwd=repo)


def authority_root() -> Path:
    return Path(__file__).resolve().parent.parent


def strict_binding(payload: dict[str, Any], base: str, head: str) -> bool:
    return (
        "base" in payload
        and "head" in payload
        and payload.get("base") == base
        and payload.get("head") == head
    )


def verify_authority_integrity(repo: Path, base: str) -> dict[str, Any]:
    root = authority_root()
    if repo.resolve() != root:
        raise RuntimeError("AUTHORITY_ROOT_REPO_MISMATCH")

    actual = git_text(repo, "rev-parse", "HEAD")
    if actual.returncode != 0 or actual.stdout.strip() != base:
        raise RuntimeError("AUTHORITY_CHECKOUT_NOT_EXACT_BASE")

    observed: dict[str, Any] = {}

    gate_disk = (root / GATE_REL).read_bytes()
    gate_blob = git_bytes(repo, "show", f"{base}:{GATE_REL}")
    if gate_blob.returncode != 0:
        raise RuntimeError("AUTHORITY_GATE_BASE_BLOB_MISSING")
    if gate_disk != gate_blob.stdout:
        raise RuntimeError("AUTHORITY_GATE_DISK_DIFFERS_FROM_BASE_BLOB")
    observed[GATE_REL] = {
        "disk_sha256": sha256_bytes(gate_disk),
        "base_blob_sha256": sha256_bytes(gate_blob.stdout),
        "pinned": False,
        "disk_equals_base_blob": True,
    }

    for rel, expected in PINNED_SHA256.items():
        disk = (root / rel).read_bytes()
        blob = git_bytes(repo, "show", f"{base}:{rel}")
        if blob.returncode != 0:
            raise RuntimeError(f"AUTHORITY_BASE_BLOB_MISSING:{rel}")
        disk_sha = sha256_bytes(disk)
        blob_sha = sha256_bytes(blob.stdout)
        if blob_sha != expected:
            raise RuntimeError(f"AUTHORITY_BASE_BLOB_HASH_MISMATCH:{rel}")
        if disk_sha != expected:
            raise RuntimeError(f"AUTHORITY_DISK_HASH_MISMATCH:{rel}")
        if disk != blob.stdout:
            raise RuntimeError(f"AUTHORITY_DISK_DIFFERS_FROM_BASE_BLOB:{rel}")
        observed[rel] = {
            "disk_sha256": disk_sha,
            "base_blob_sha256": blob_sha,
            "expected_sha256": expected,
            "pinned": True,
            "disk_equals_base_blob": True,
        }
    return observed


def parse_json(result: subprocess.CompletedProcess[str], label: str) -> dict[str, Any]:
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"{label}: invalid JSON: {exc}; stdout={result.stdout!r}; stderr={result.stderr!r}"
        ) from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label}: payload is not object")
    return payload


def run_risk(repo: Path, base: str, head: str, authorized_class: str):
    root = authority_root()
    result = run(
        [
            sys.executable,
            "-I",
            "-B",
            "-S",
            str(root / CHECKER_REL),
            "--policy",
            str(root / POLICY_REL),
            "--mode",
            "post",
            "--authorized-class",
            authorized_class,
            "--repo",
            str(repo),
            "--base",
            base,
            "--head",
            head,
        ],
        cwd=root,
    )
    return result, parse_json(result, "risk")


def common(base: str | None = None, head: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "authority_root": str(authority_root()),
        "normal_pr_authorized_class": NORMAL_PR_CLASS,
        "candidate_worktree_checked_out": False,
        "candidate_code_executed": False,
        "integrity_model": "PINNED_SHA256_PLUS_EXACT_BASE_GIT_BLOBS",
        "evaluation_before_self_test": True,
        "dc_006": "OPEN",
        "exp_01": "OPEN",
    }
    if base is not None:
        payload["base"] = base
    if head is not None:
        payload["head"] = head
    return payload


def evaluate(repo: Path, base: str, head: str) -> int:
    c = common(base, head)
    try:
        integrity = verify_authority_integrity(repo, base)
    except (OSError, RuntimeError) as exc:
        emit(
            {
                **c,
                "status": "FAIL",
                "reason_code": "AUTHORITY_INTEGRITY_FAILED",
                "error": str(exc),
            }
        )
        return EXIT_FAIL

    candidate = git_text(repo, "cat-file", "-e", f"{head}^{{commit}}")
    if candidate.returncode != 0:
        emit({**c, "status": "FAIL", "reason_code": "CANDIDATE_COMMIT_MISSING"})
        return EXIT_FAIL

    result, risk = run_risk(repo, base, head, NORMAL_PR_CLASS)
    c.update(
        {
            "integrity": integrity,
            "risk_checker_exit": result.returncode,
            "risk_status": risk.get("status"),
            "risk_reason_code": risk.get("reason_code"),
            "risk_floor": risk.get("mechanical_path_floor"),
            "risk_payload_base": risk.get("base"),
            "risk_payload_head": risk.get("head"),
        }
    )

    if not strict_binding(risk, base, head):
        emit({**c, "status": "FAIL", "reason_code": "RISK_PAYLOAD_OBJECT_MISMATCH"})
        return EXIT_FAIL

    if result.returncode == 0:
        if (
            risk.get("status") != "PASS"
            or risk.get("reason_code") != "FLOOR_WITHIN_AUTHORIZED_CLASS"
        ):
            emit({**c, "status": "ERROR", "reason_code": "RISK_EXIT_ZERO_WITH_NONPASS"})
            return EXIT_ERROR
        emit({**c, "status": "PASS", "reason_code": "BASE_ANCHORED_RISK_GATE_PASSED"})
        return EXIT_PASS

    if result.returncode == 3 and risk.get("status") == "FAIL":
        emit(
            {
                **c,
                "status": "FAIL",
                "reason_code": f"RISK_{risk.get('reason_code', 'UNKNOWN')}",
            }
        )
        return EXIT_FAIL

    emit(
        {
            **c,
            "status": "ERROR",
            "reason_code": "RISK_CHECKER_ERROR",
            "stderr": result.stderr,
        }
    )
    return EXIT_ERROR


def risk_self_test(root: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="r2aa011-risk-selftest-") as td:
        repo = Path(td) / "repo"
        repo.mkdir()
        for args in (
            ["git", "init", "-b", "main"],
            ["git", "config", "user.name", "R2 Selftest"],
            ["git", "config", "user.email", "r2-selftest@example.invalid"],
            ["git", "config", "user.useConfigOnly", "true"],
        ):
            result = run(args, cwd=repo)
            if result.returncode != 0:
                raise RuntimeError(result.stderr)

        (repo / "src").mkdir()
        (repo / "src/app.py").write_text("VALUE = 1\n", encoding="utf-8")
        (repo / "R2_STATE.md").write_text("# state\n", encoding="utf-8")
        result = run(["git", "add", "--all"], cwd=repo)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        result = run(["git", "commit", "-m", "base"], cwd=repo)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        base = run(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()

        def child(branch: str, rel: str, text: str) -> str:
            result = run(["git", "checkout", "-B", branch, base], cwd=repo)
            if result.returncode != 0:
                raise RuntimeError(result.stderr)
            p = repo / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
            result = run(["git", "add", "--all"], cwd=repo)
            if result.returncode != 0:
                raise RuntimeError(result.stderr)
            result = run(["git", "commit", "-m", branch], cwd=repo)
            if result.returncode != 0:
                raise RuntimeError(result.stderr)
            return run(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()

        b = child("b-pass", "src/app.py", "VALUE = 2\n")
        d = child("d-fail", "R2_STATE.md", "# changed\n")
        u = child("u-fail", "scripts/unknown.py", "VALUE=1\n")

        bres, bp = run_risk(repo, base, b, "B")
        dres, dp = run_risk(repo, base, d, "B")
        ures, up = run_risk(repo, base, u, "D")

        if not (
            bres.returncode == 0
            and bp.get("status") == "PASS"
            and bp.get("reason_code") == "FLOOR_WITHIN_AUTHORIZED_CLASS"
            and bp.get("mechanical_path_floor") == "B"
            and strict_binding(bp, base, b)
        ):
            raise RuntimeError(f"risk B selftest failed: {bp!r}")

        if not (
            dres.returncode == 3
            and dp.get("status") == "FAIL"
            and dp.get("reason_code") == "FLOOR_EXCEEDS_AUTHORIZED_CLASS"
            and dp.get("mechanical_path_floor") == "D"
            and strict_binding(dp, base, d)
        ):
            raise RuntimeError(f"risk D selftest failed: {dp!r}")

        if not (
            ures.returncode == 3
            and up.get("status") == "FAIL"
            and up.get("reason_code") == "UNKNOWN_HIGH_AUTHORITY_SUBJECT"
            and up.get("mechanical_path_floor") == "D"
            and strict_binding(up, base, u)
        ):
            raise RuntimeError(f"risk unknown selftest failed: {up!r}")

        return {
            "post_b_pass": {
                "exit": bres.returncode,
                "status": bp.get("status"),
                "reason": bp.get("reason_code"),
            },
            "post_d_under_b": {
                "exit": dres.returncode,
                "status": dp.get("status"),
                "reason": dp.get("reason_code"),
            },
            "post_unknown_at_d": {
                "exit": ures.returncode,
                "status": up.get("status"),
                "reason": up.get("reason_code"),
            },
        }


def runner_self_test(root: Path) -> dict[str, Any]:
    runner = root / RUNNER_REL
    good = root / GOOD_REL
    bad = root / BAD_REL

    good_result = run(
        [
            sys.executable,
            "-I",
            "-B",
            "-S",
            str(runner),
            "--implementation",
            str(good),
        ],
        cwd=root,
    )
    gp = parse_json(good_result, "runner GOOD")
    if not (
        good_result.returncode == 0
        and gp.get("status") == "PASS"
        and gp.get("reason_code") == "ALL_FUNCTIONAL_CHECKS_PASSED"
        and not good_result.stderr
    ):
        raise RuntimeError(f"runner GOOD failed: {gp!r}")

    bad_result = run(
        [
            sys.executable,
            "-I",
            "-B",
            "-S",
            str(runner),
            "--implementation",
            str(bad),
        ],
        cwd=root,
    )
    bp = parse_json(bad_result, "runner BAD")
    if not (
        bad_result.returncode == 1
        and bp.get("status") == "FAIL"
        and bp.get("reason_code") == "TOTAL_NOT_CONSERVED"
        and not bad_result.stderr
    ):
        raise RuntimeError(f"runner BAD failed: {bp!r}")

    return {
        "good": {
            "exit": good_result.returncode,
            "status": gp.get("status"),
            "reason": gp.get("reason_code"),
        },
        "bad": {
            "exit": bad_result.returncode,
            "status": bp.get("status"),
            "reason": bp.get("reason_code"),
        },
    }


def self_test(repo: Path, base: str) -> int:
    c = common(base, None)

    binding_contract = {
        "exact": strict_binding({"base": "B", "head": "H"}, "B", "H"),
        "missing_base_rejected": not strict_binding({"head": "H"}, "B", "H"),
        "missing_head_rejected": not strict_binding({"base": "B"}, "B", "H"),
        "wrong_base_rejected": not strict_binding(
            {"base": "X", "head": "H"}, "B", "H"
        ),
        "wrong_head_rejected": not strict_binding(
            {"base": "B", "head": "X"}, "B", "H"
        ),
    }
    if not all(binding_contract.values()):
        emit({**c, "status": "FAIL", "reason_code": "STRICT_BINDING_SELFTEST_FAILED"})
        return EXIT_FAIL

    try:
        before = verify_authority_integrity(repo, base)
        risk = risk_self_test(authority_root())
        runner = runner_self_test(authority_root())
        after = verify_authority_integrity(repo, base)
    except (OSError, RuntimeError) as exc:
        emit(
            {
                **c,
                "status": "FAIL",
                "reason_code": "SELF_TEST_FAILED",
                "error": str(exc),
            }
        )
        return EXIT_FAIL

    emit(
        {
            **c,
            "status": "PASS",
            "reason_code": "TRUSTED_VERIFIERS_AND_INTEGRITY_PROVED",
            "binding_contract": binding_contract,
            "integrity_before": before,
            "risk": risk,
            "runner": runner,
            "integrity_after": after,
        }
    )
    return EXIT_PASS


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=("evaluate", "self-test"))
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head")
    args = parser.parse_args()

    if args.mode == "evaluate":
        if args.head is None:
            emit({"status": "ERROR", "reason_code": "EVALUATE_REQUIRES_HEAD"})
            return EXIT_ERROR
        return evaluate(args.repo.resolve(), args.base, args.head)

    if args.head is not None:
        emit({"status": "ERROR", "reason_code": "SELF_TEST_DOES_NOT_ACCEPT_HEAD"})
        return EXIT_ERROR
    return self_test(args.repo.resolve(), args.base)


if __name__ == "__main__":
    raise SystemExit(main())
# R2-4 D NEGATIVE PROBE ONLY: candidate-side acceptance-authority edit; must be rejected and never merged.
