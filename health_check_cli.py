#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GUMROAD_KIT_URL = "https://designsy1.gumroad.com/l/toksiz"
CHECKLIST_RESULT_URL = (
    "https://github.com/xcapselx/repo-health-checks/issues/new?template=checklist-result.yml"
)

ESSENTIAL_FILES = {
    "readme": ("README.md", "README.rst", "README.txt"),
    "license": ("LICENSE", "LICENSE.md", "COPYING", "COPYING.md"),
    "security": ("SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md"),
}

DEPENDENCY_SETS = [
    {
        "ecosystem": "Node.js",
        "configs": ("package.json",),
        "lockfiles": ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb", "bun.lock"),
    },
    {
        "ecosystem": "Python",
        "configs": ("pyproject.toml", "requirements.txt", "setup.py", "Pipfile"),
        "lockfiles": ("uv.lock", "poetry.lock", "Pipfile.lock", "requirements.lock"),
    },
    {
        "ecosystem": "Rust",
        "configs": ("Cargo.toml",),
        "lockfiles": ("Cargo.lock",),
    },
    {
        "ecosystem": "Go",
        "configs": ("go.mod",),
        "lockfiles": ("go.sum",),
    },
    {
        "ecosystem": "Ruby",
        "configs": ("Gemfile",),
        "lockfiles": ("Gemfile.lock",),
    },
    {
        "ecosystem": "PHP",
        "configs": ("composer.json",),
        "lockfiles": ("composer.lock",),
    },
    {
        "ecosystem": ".NET",
        "configs": ("*.csproj", "*.fsproj", "*.vbproj", "packages.config"),
        "lockfiles": ("packages.lock.json",),
    },
]

IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "target",
    "coverage",
    ".next",
    ".turbo",
}

CLUTTER_EXTENSIONS = {".log", ".tmp", ".bak", ".swp", ".swo", ".orig"}
SECRETISH_PATTERN = re.compile(
    r"(?i)(secret|token|api[_-]?key|password|credential|private[_-]?key|access[_-]?key)"
)


@dataclass(frozen=True)
class CheckResult:
    name: str
    score: int
    max_score: int
    status: str
    detail: str


def _has_any(root: Path, names: tuple[str, ...]) -> bool:
    for name in names:
        if any(root.glob(name)):
            return True
    return False


def _repo_label(root: Path) -> str:
    return root.name or "repository"


def _iter_visible_files(root: Path, *, max_files: int = 5000) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        if path.is_file():
            files.append(relative)
            if len(files) >= max_files:
                break
    return files


def _check_essential_files(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    for label, names in ESSENTIAL_FILES.items():
        found = _has_any(root, names)
        pretty = label.replace("_", " ").title()
        results.append(
            CheckResult(
                name=pretty,
                score=2 if found else 0,
                max_score=2,
                status="ok" if found else "missing",
                detail="Found" if found else f"Add one of: {', '.join(names)}",
            )
        )
    return results


def _dependency_status(root: Path) -> CheckResult:
    detected: list[str] = []
    unlocked: list[str] = []
    for spec in DEPENDENCY_SETS:
        has_config = _has_any(root, spec["configs"])
        if not has_config:
            continue
        detected.append(spec["ecosystem"])
        if not _has_any(root, spec["lockfiles"]):
            unlocked.append(spec["ecosystem"])

    if not detected:
        return CheckResult(
            name="Dependency Files",
            score=1,
            max_score=2,
            status="not_detected",
            detail="No common dependency manifest found; this may be fine for docs-only repos.",
        )
    if unlocked:
        return CheckResult(
            name="Dependency Files",
            score=1,
            max_score=2,
            status="partial",
            detail="Detected " + ", ".join(detected) + "; lockfile missing for " + ", ".join(unlocked) + ".",
        )
    return CheckResult(
        name="Dependency Files",
        score=2,
        max_score=2,
        status="ok",
        detail="Detected " + ", ".join(detected) + " with matching lockfile evidence.",
    )


def _tree_hygiene(root: Path) -> CheckResult:
    files = _iter_visible_files(root)
    if not files:
        return CheckResult("File Tree Hygiene", 0, 2, "empty", "No visible files found.")

    max_depth = max((len(path.parts) for path in files), default=0)
    clutter = [path for path in files if path.suffix.lower() in CLUTTER_EXTENSIONS]
    secretish_names = [path for path in files if SECRETISH_PATTERN.search(path.name)]

    if max_depth <= 6 and len(clutter) <= 2 and not secretish_names:
        return CheckResult(
            "File Tree Hygiene",
            2,
            2,
            "ok",
            f"{len(files)} visible files, max depth {max_depth}, no obvious clutter names.",
        )
    if max_depth <= 9 and len(clutter) <= 10 and len(secretish_names) <= 2:
        return CheckResult(
            "File Tree Hygiene",
            1,
            2,
            "partial",
            f"{len(files)} visible files, max depth {max_depth}; review clutter or sensitive-looking filenames.",
        )
    return CheckResult(
        "File Tree Hygiene",
        0,
        2,
        "review",
        f"{len(files)} visible files, max depth {max_depth}; simplify tree or remove clutter before handoff.",
    )


def _check_ci_workflows(root: Path) -> CheckResult:
    workflows_dir = root / ".github" / "workflows"
    if workflows_dir.exists() and any(workflows_dir.glob("*.yml")) or any(workflows_dir.glob("*.yaml")):
        return CheckResult("CI Workflows", 2, 2, "ok", "GitHub Actions workflows detected.")
    if root.joinpath(".circleci").exists() or root.joinpath(".travis.yml").exists() or root.joinpath("Jenkinsfile").exists():
        return CheckResult("CI Workflows", 2, 2, "ok", "External CI configuration detected.")
    return CheckResult("CI Workflows", 0, 2, "missing", "No CI workflow files found. Add .github/workflows/ for automated testing.")


def _check_test_structure(root: Path) -> CheckResult:
    test_indicators = [
        root / "tests",
        root / "test",
        root / "spec",
        root / "__tests__",
    ]
    test_file_patterns = ["test_*.py", "*_test.py", "*.test.ts", "*.test.js", "*.spec.ts", "*.spec.js"]
    has_test_dir = any(d.exists() and d.is_dir() for d in test_indicators)
    has_test_files = any(any(root.glob(p)) for p in test_file_patterns)
    if has_test_dir and has_test_files:
        return CheckResult("Test Structure", 2, 2, "ok", "Test directory and test files detected.")
    if has_test_dir or has_test_files:
        return CheckResult("Test Structure", 1, 2, "partial", "Some test structure found but incomplete.")
    return CheckResult("Test Structure", 0, 2, "missing", "No test directory or test files found.")


def _check_gitignore(root: Path) -> CheckResult:
    gitignore = root / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text(errors="replace").lower()
        has_node_modules = "node_modules" in content
        has_env = ".env" in content
        has_build = "build" in content or "dist" in content
        coverage = sum([has_node_modules, has_env, has_build])
        if coverage >= 2:
            return CheckResult("Gitignore", 2, 2, "ok", ".gitignore covers common build artifacts and secrets.")
        if coverage >= 1:
            return CheckResult("Gitignore", 1, 2, "partial", ".gitignore exists but may miss common patterns.")
        return CheckResult("Gitignore", 1, 2, "partial", ".gitignore exists but lacks common patterns.")
    return CheckResult("Gitignore", 0, 2, "missing", "No .gitignore file found. Add one to exclude build artifacts and secrets.")


def _check_community_files(root: Path) -> CheckResult:
    files = {
        "CONTRIBUTING.md": root / "CONTRIBUTING.md" or root / ".github" / "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md": root / "CODE_OF_CONDUCT.md" or root / ".github" / "CODE_OF_CONDUCT.md",
        "CHANGELOG.md": root / "CHANGELOG.md",
        "issue template": root / ".github" / "ISSUE_TEMPLATE",
        "PR template": root / ".github" / "PULL_REQUEST_TEMPLATE.md" or root / ".github" / "pull_request_template.md",
    }
    found = []
    for label, path in files.items():
        p = Path(path) if not isinstance(path, Path) else path
        if p.exists():
            found.append(label)
    if len(found) >= 3:
        return CheckResult("Community Files", 2, 2, "ok", f"Found: {', '.join(found)}.")
    if len(found) >= 1:
        return CheckResult("Community Files", 1, 2, "partial", f"Found: {', '.join(found)}. Consider adding more.")
    return CheckResult("Community Files", 0, 2, "missing", "No CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, or templates found.")


def scan_repository(path: str | Path) -> dict[str, Any]:
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError("Target repository directory does not exist.")

    checks = [
        *_check_essential_files(root),
        _dependency_status(root),
        _tree_hygiene(root),
        _check_ci_workflows(root),
        _check_test_structure(root),
        _check_gitignore(root),
        _check_community_files(root),
    ]
    score = sum(item.score for item in checks)
    max_score = sum(item.max_score for item in checks)
    pct = round(score / max_score * 100) if max_score > 0 else 0
    if pct >= 80:
        band = "good shape for a lightweight pass"
    elif pct >= 50:
        band = "usable with handoff friction"
    else:
        band = "basic recovery pass needed"

    return {
        "repo": _repo_label(root),
        "score": score,
        "max_score": max_score,
        "score_percent": pct,
        "score_band": band,
        "checks": [item.__dict__ for item in checks],
        "external_action": False,
        "network_used": False,
    }


def render_scorecard(result: dict[str, Any]) -> str:
    lines = [
        "# Repo Health Mini Scorecard",
        "",
        f"Repository: {result['repo']}",
        f"Score: {result['score']}/{result['max_score']} ({result.get('score_percent', 0)}%) - {result['score_band']}",
        "",
        "| Check | Status | Score | Note |",
        "| --- | --- | ---: | --- |",
    ]
    for check in result["checks"]:
        lines.append(
            f"| {check['name']} | {check['status']} | {check['score']}/{check['max_score']} | {check['detail']} |"
        )
    lines.extend(
        [
            "",
            "## Next Step",
            "",
            "Start free: use the README Health Mini Checklist and fix the lowest-scoring row first.",
            f"Optional signal: if you want to share a public-safe result, open a checklist-result issue: {CHECKLIST_RESULT_URL}",
            f"Fuller self-serve kit: Repo Health Snapshot Kit ($29): {GUMROAD_KIT_URL}",
            "",
            "Public safety: do not paste secrets, credentials, private repo URLs, production access details, customer/user data, tokens/API keys, private logs, or private context into public issues.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a local, non-invasive repo health mini scan.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Proof-packet drafts:\n"
            "  Use --json to emit scanner output suitable for a local proof-packet compiler.\n"
            "  Proof-packet generation is currently a local/internal workflow, not a public web service.\n"
            "  A proof packet can map scan findings to the free checklist, sample proof artifacts, and kit resources.\n"
            "  This scanner does not make network calls, and it does not upload repo data.\n"
            "  Do not paste secrets, logs, tokens, production URLs, customer data, credentials, private repo data,\n"
            "  or internal context into public issues.\n"
        ),
    )
    parser.add_argument("path", nargs="?", default=".", help="Repository directory to scan.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of Markdown.")
    args = parser.parse_args(argv)

    try:
        result = scan_repository(args.path)
    except FileNotFoundError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_scorecard(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
