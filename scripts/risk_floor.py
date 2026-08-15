#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


EXIT_PASS = 0
EXIT_USAGE_OR_ERROR = 2
EXIT_BLOCKED = 3


@dataclass(frozen=True)
class Finding:
    subject_type: str
    subject: str
    floor: str
    role: str
    reason: str
    explicit: bool
    blocks_unknown: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "subject_type": self.subject_type,
            "subject": self.subject,
            "floor": self.floor,
            "role": self.role,
            "reason": self.reason,
            "explicit": self.explicit,
            "blocks_unknown": self.blocks_unknown,
        }


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def git(repo: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


class Policy:
    def __init__(self, path: Path) -> None:
        self.path = path
        try:
            self.data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"No se pudo cargar la política: {exc}") from exc

        if self.data.get("decision_id") != "DEC-CP":
            raise ValueError("La política no declara decision_id=DEC-CP")
        if self.data.get("status") != "AUTHORIZED_LOCAL_EXPERIMENTAL":
            raise ValueError(
                "La política no está autorizada para el experimento local R2"
            )
        if self.data.get("activation_rule") != (
            "LOCAL_R2_EXPERIMENT_ONLY_NOT_ENFORCED_NOT_MERGE_AUTHORITY"
        ):
            raise ValueError("activation_rule no permite este uso local")

        order = self.data.get("class_order")
        if order != ["A", "B", "C", "D"]:
            raise ValueError("class_order inesperado")
        self.rank = {value: index for index, value in enumerate(order)}

        self.exact_paths = {
            item["path"]: item for item in self.data.get("exact_paths", [])
        }
        prefixes = self.data.get("prefix_rules", [])
        self.prefix_rules = sorted(
            prefixes,
            key=lambda item: len(item["prefix"]),
            reverse=True,
        )
        self.control_plane_roots = tuple(
            self.data.get("control_plane_roots", [])
        )
        self.defaults = self.data.get("defaults", {})
        self.action_floors = self.data.get("action_floors", {})
        self.capability_floors = self.data.get("capability_floors", {})

    def max_floor(self, floors: Iterable[str]) -> str:
        values = list(floors)
        if not values:
            return "A"
        for value in values:
            if value not in self.rank:
                raise ValueError(f"Clase desconocida: {value}")
        return max(values, key=self.rank.__getitem__)

    @staticmethod
    def normalize_path(raw: str) -> str:
        if not raw or "\x00" in raw or "\\" in raw:
            raise ValueError(f"Path inválido: {raw!r}")
        path = PurePosixPath(raw)
        if path.is_absolute():
            raise ValueError(f"Path absoluto no permitido: {raw!r}")
        parts = path.parts
        if not parts or any(part in ("", ".", "..") for part in parts):
            raise ValueError(f"Path no normalizado: {raw!r}")
        normalized = path.as_posix()
        if normalized != raw:
            raise ValueError(
                f"Path no canónico: recibido={raw!r} normalizado={normalized!r}"
            )
        return normalized

    def _is_control_plane(self, path: str) -> bool:
        for root in self.control_plane_roots:
            if root.endswith("/"):
                if path.startswith(root):
                    return True
            elif path == root:
                return True
        return False

    def classify_path(self, raw: str) -> Finding:
        path = self.normalize_path(raw)

        exact = self.exact_paths.get(path)
        if exact is not None:
            return Finding(
                subject_type="path",
                subject=path,
                floor=exact["floor"],
                role=exact.get("role", "unspecified"),
                reason=exact.get("reason", "exact_path"),
                explicit=True,
            )

        for rule in self.prefix_rules:
            if path.startswith(rule["prefix"]):
                return Finding(
                    subject_type="path",
                    subject=path,
                    floor=rule["floor"],
                    role=rule.get("role", "unspecified"),
                    reason=rule.get("reason", "longest_prefix"),
                    explicit=True,
                )

        if self._is_control_plane(path):
            return Finding(
                subject_type="path",
                subject=path,
                floor=self.defaults.get("unknown_control_plane", "D"),
                role="unknown_control_plane",
                reason=(
                    "Path desconocido dentro del control plane: "
                    "D/STOP hasta clasificación explícita."
                ),
                explicit=False,
                blocks_unknown=True,
            )

        return Finding(
            subject_type="path",
            subject=path,
            floor=self.defaults.get("unknown_normal", "B"),
            role="unknown_normal",
            reason="Path normal no clasificado: floor mínimo B.",
            explicit=False,
        )

    def classify_action(self, action: str) -> Finding:
        floor = self.action_floors.get(action)
        if floor is None:
            return Finding(
                subject_type="action",
                subject=action,
                floor="D",
                role="unknown_action",
                reason="Acción no clasificada: D/STOP.",
                explicit=False,
                blocks_unknown=True,
            )
        return Finding(
            subject_type="action",
            subject=action,
            floor=floor,
            role="action",
            reason=f"Floor explícito de la acción {action}.",
            explicit=True,
        )

    def classify_capability(self, capability: str) -> Finding:
        floor = self.capability_floors.get(capability)
        if floor is None:
            return Finding(
                subject_type="capability",
                subject=capability,
                floor="D",
                role="unknown_capability",
                reason="Capacidad no clasificada: D/STOP.",
                explicit=False,
                blocks_unknown=True,
            )
        return Finding(
            subject_type="capability",
            subject=capability,
            floor=floor,
            role="capability",
            reason=f"Floor explícito de la capacidad {capability}.",
            explicit=True,
        )


def evaluate(
    *,
    policy: Policy,
    mode: str,
    authorized_class: str,
    findings: list[Finding],
    changes: list[dict[str, Any]] | None = None,
    base: str | None = None,
    head: str | None = None,
) -> int:
    if authorized_class not in policy.rank:
        emit(
            {
                "status": "ERROR",
                "reason_code": "INVALID_AUTHORIZED_CLASS",
                "authorized_class": authorized_class,
            }
        )
        return EXIT_USAGE_OR_ERROR

    floor = policy.max_floor(item.floor for item in findings)
    unknown_blocks = [item for item in findings if item.blocks_unknown]

    payload: dict[str, Any] = {
        "mode": mode,
        "authorized_class": authorized_class,
        "mechanical_path_floor": floor,
        "findings": [item.as_dict() for item in findings],
    }
    if changes is not None:
        payload["changes"] = changes
    if base is not None:
        payload["base"] = base
    if head is not None:
        payload["head"] = head

    if unknown_blocks:
        payload.update(
            {
                "status": "FAIL",
                "reason_code": "UNKNOWN_HIGH_AUTHORITY_SUBJECT",
                "message": (
                    "Existe un path, acción o capacidad de alta autoridad "
                    "sin clasificación explícita."
                ),
            }
        )
        emit(payload)
        return EXIT_BLOCKED

    if policy.rank[floor] > policy.rank[authorized_class]:
        payload.update(
            {
                "status": "FAIL",
                "reason_code": "FLOOR_EXCEEDS_AUTHORIZED_CLASS",
                "message": (
                    "El floor mecánico supera la clase autorizada; "
                    "se requiere nueva autorización."
                ),
            }
        )
        emit(payload)
        return EXIT_BLOCKED

    payload.update(
        {
            "status": "PASS",
            "reason_code": "FLOOR_WITHIN_AUTHORIZED_CLASS",
        }
    )
    emit(payload)
    return EXIT_PASS


def parse_name_status_z(raw: bytes) -> list[tuple[str, list[str]]]:
    tokens = raw.split(b"\0")
    if tokens and tokens[-1] == b"":
        tokens.pop()

    records: list[tuple[str, list[str]]] = []
    index = 0
    while index < len(tokens):
        try:
            status = tokens[index].decode("ascii")
        except UnicodeDecodeError as exc:
            raise ValueError("Status Git no ASCII") from exc
        index += 1

        code = status[:1]
        path_count = 2 if code in {"R", "C"} else 1
        if code not in {"A", "M", "D", "R", "C", "T"}:
            raise ValueError(f"Status Git no soportado: {status!r}")
        if index + path_count > len(tokens):
            raise ValueError("Salida NUL de Git truncada")

        paths: list[str] = []
        for token in tokens[index : index + path_count]:
            try:
                paths.append(token.decode("utf-8", errors="surrogateescape"))
            except UnicodeDecodeError as exc:
                raise ValueError("Path Git no decodificable") from exc
        index += path_count
        records.append((status, paths))

    return records


def findings_from_post(
    policy: Policy,
    repo: Path,
    base: str,
    head: str,
) -> tuple[list[Finding], list[dict[str, Any]]]:
    ancestor = git(repo, "merge-base", "--is-ancestor", base, head)
    if ancestor.returncode != 0:
        stderr = ancestor.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(
            "HEAD no desciende del BASE autorizado"
            + (f": {stderr}" if stderr else "")
        )

    diff = git(
        repo,
        "diff",
        "--name-status",
        "--find-renames",
        "-z",
        base,
        head,
    )
    if diff.returncode != 0:
        raise ValueError(
            "git diff falló: "
            + diff.stderr.decode("utf-8", errors="replace").strip()
        )

    findings: list[Finding] = []
    changes: list[dict[str, Any]] = []

    for status, paths in parse_name_status_z(diff.stdout):
        code = status[:1]
        record: dict[str, Any] = {"status": status, "paths": paths}

        if code in {"A", "M", "T"}:
            path_finding = policy.classify_path(paths[0])
            findings.append(path_finding)
            record["floors"] = [path_finding.floor]

        elif code == "D":
            path_finding = policy.classify_path(paths[0])
            action_finding = policy.classify_action("deletion")
            findings.extend([path_finding, action_finding])
            record["floors"] = [path_finding.floor, action_finding.floor]

        elif code in {"R", "C"}:
            source_finding = policy.classify_path(paths[0])
            destination_finding = policy.classify_path(paths[1])
            findings.extend([source_finding, destination_finding])
            record["floors"] = [
                source_finding.floor,
                destination_finding.floor,
            ]

        changes.append(record)

    return findings, changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Risk-floor checker PRE/POST de R2."
    )
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--mode", required=True, choices=("pre", "post"))
    parser.add_argument(
        "--authorized-class",
        required=True,
        choices=("A", "B", "C", "D"),
    )
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--action", action="append", default=[])
    parser.add_argument("--capability", action="append", default=[])
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--base")
    parser.add_argument("--head")
    args = parser.parse_args()

    try:
        policy = Policy(args.policy.resolve())

        if args.mode == "pre":
            if args.repo is not None or args.base is not None or args.head is not None:
                raise ValueError("PRE no acepta --repo, --base ni --head")
            if not (args.path or args.action or args.capability):
                raise ValueError(
                    "PRE requiere al menos un --path, --action o --capability"
                )

            findings = [policy.classify_path(value) for value in args.path]
            findings.extend(
                policy.classify_action(value) for value in args.action
            )
            findings.extend(
                policy.classify_capability(value)
                for value in args.capability
            )
            return evaluate(
                policy=policy,
                mode="PRE",
                authorized_class=args.authorized_class,
                findings=findings,
            )

        if args.path or args.action or args.capability:
            raise ValueError(
                "POST obtiene paths y acciones del diff; no acepta "
                "--path, --action ni --capability"
            )
        if args.repo is None or args.base is None or args.head is None:
            raise ValueError("POST requiere --repo, --base y --head")

        repo = args.repo.resolve()
        if not repo.is_dir():
            raise ValueError(f"Repositorio inexistente: {repo}")

        findings, changes = findings_from_post(
            policy,
            repo,
            args.base,
            args.head,
        )
        return evaluate(
            policy=policy,
            mode="POST",
            authorized_class=args.authorized_class,
            findings=findings,
            changes=changes,
            base=args.base,
            head=args.head,
        )

    except ValueError as exc:
        emit(
            {
                "status": "ERROR",
                "reason_code": "CHECKER_ERROR",
                "message": str(exc),
            }
        )
        return EXIT_USAGE_OR_ERROR


if __name__ == "__main__":
    sys.exit(main())
