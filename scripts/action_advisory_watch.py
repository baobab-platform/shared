"""BA-SEC-DEP-001: public advisory watch for SHA-pinned GitHub Actions.

Dependabot Alerts do not cover Actions pinned by SHA. This produces a bounded
package-name-level *triage queue* from GitHub's reviewed Actions advisories.
A package-name match does not prove the pinned SHA is vulnerable; a missing
match does not prove safety. Do not use this as release acceptance or replace
the existing SHA-pinning check. No private GHSA or secrets are published.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://api.github.com/advisories"
USES = re.compile(
    r"^\s*(?:-\s*)?uses:\s*['\"]?"
    r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"
    r"(?:/[^@\s'\"]+)?@([0-9a-fA-F]{40})(?:\s|['\"]|$)"
)
ANNOTATED_VERSION = re.compile(r"\s+#\s+(v[0-9][A-Za-z0-9_.+-]*)")
SKIP_DIRECTORIES = {".git", "node_modules", "vendor", ".venv", "dist", "build"}
MAX_PAGES = 10  # bounded, avoid unbounded API traversal on schedule


def inventory(root: Path) -> list[dict]:
    candidate_files = sorted((root / ".github/workflows").rglob("*.yml"))
    candidate_files += sorted((root / ".github/workflows").rglob("*.yaml"))
    candidate_files += sorted((root / ".github/actions").rglob("action.yml"))
    candidate_files += sorted((root / ".github/actions").rglob("action.yaml"))
    entries = []
    for path in candidate_files:
        if any(part in SKIP_DIRECTORIES for part in path.parts):
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = USES.match(line)
            if not match:
                continue  # local actions and Docker actions covered by pinning gate
            comment = ANNOTATED_VERSION.search(line)
            entries.append({
                "package": match.group(1).lower(),
                "sha": match.group(2).lower(),
                "version_hint": comment.group(1) if comment else None,
                "source": path.relative_to(root).as_posix(),
                "line": number,
            })
    return sorted(entries, key=lambda e: (e["package"], e["source"], e["line"]))


def fetch_public_advisories(token: str | None = None) -> list[dict]:
    advisories: list[dict] = []
    for page in range(1, MAX_PAGES + 1):
        url = f"{API_URL}?ecosystem=actions&type=reviewed&per_page=100&page={page}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "baobab-platform-action-advisory-watch",
        }
        if token:
            headers["Authorization"] = "Bearer " + token
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=20) as response:
                data = json.load(response)
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            raise RuntimeError(f"GitHub public advisory API unavailable on page {page}: {type(exc).__name__}") from exc
        if not isinstance(data, list):
            raise RuntimeError("GitHub public advisory API response is not a list")
        advisories.extend(data)
        if len(data) < 100:
            return advisories
    raise RuntimeError(f"Advisory API exceeded bounded {MAX_PAGES}-page review; cannot report coverage")


def review(root: Path, advisories: list[dict]) -> dict:
    actions = inventory(root)
    by_name: dict[str, list[dict]] = {}
    for advisory in advisories:
        if not isinstance(advisory, dict) or not advisory.get("ghsa_id"):
            continue
        # Use the reviewed GitHub database's package identity, not a text
        # search over the advisory description or a guessed commit version.
        for item in advisory.get("vulnerabilities") or []:
            pkg = item.get("package") if isinstance(item, dict) else None
            if not isinstance(pkg, dict) or pkg.get("ecosystem") != "actions":
                continue
            name = str(pkg.get("name") or "").strip().lower()
            if not name:
                continue
            by_name.setdefault(name, []).append({
                "ghsa_id": advisory["ghsa_id"],
                "severity": advisory.get("severity", "unknown"),
                "html_url": advisory.get("html_url", ""),
                "affected_range": item.get("vulnerable_version_range"),
                "first_patched_version": item.get("first_patched_version"),
            })

    matches = []
    for entry in actions:
        matched = by_name.get(entry["package"], [])
        for item in matched:
            matches.append({
                **entry,
                **item,
                # Do not trust a comment to classify the actual SHA:
                "affected_sha": "UNKNOWN_REQUIRES_UPSTREAM_RELEASE_VERIFICATION",
            })
    return {
        "schema_version": 1,
        "control": "BA-SEC-DEP-001/action-advisory-watch",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "GitHub Global Security Advisories, reviewed, ecosystem=actions",
        "status": "TRIAGE_REQUIRED" if matches else "NO_PACKAGE_MATCH_NOT_A_SECURITY_CLEARANCE",
        "advisory_count": len(advisories),
        "action_references": len(actions),
        "unique_action_packages": len({a["package"] for a in actions}),
        "unknown_version_annotations": sum(a["version_hint"] is None for a in actions),
        "inventory": actions,
        "matches": matches,
        "limitations": [
            "A package-name match does not establish that a pinned SHA is in the vulnerable range.",
            "A missing match does not prove a pinned SHA secure or its upstream repository trustworthy.",
            "Version hints in comments are unverified and must not resolve findings automatically.",
            "Private/unreviewed advisories, compromised releases and arbitrary workflows are not covered.",
            "This is surveillance and triage, not an independent consumer or production qualification.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--advisories-file", type=Path, help="Offline test/incident snapshot instead of GitHub public API")
    args = parser.parse_args(argv)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        if args.advisories_file is not None:
            advisories = json.loads(args.advisories_file.read_text(encoding="utf-8"))
        else:
            advisories = fetch_public_advisories(os.getenv("GITHUB_TOKEN"))
        if not isinstance(advisories, list):
            raise ValueError("advisories input must be a list")
        result = review(args.root.resolve(), advisories)
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Action advisory watch: {result['status']}; checked={result['action_references']}, "
              f"matching_advisory_instances={len(result['matches'])}")
        if result["matches"]:
            print("::warning::Action package advisories require manual affected-SHA verification; see JSON artifact.")
        return 0
    except (RuntimeError, OSError, ValueError) as exc:
        # Unavailable API / malformed data is UNKNOWN, not clean.
        failed = {
            "schema_version": 1,
            "control": "BA-SEC-DEP-001/action-advisory-watch",
            "status": "UNKNOWN_SOURCE_UNAVAILABLE",
            "error_type": type(exc).__name__,
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "limitations": ["No advisory clearance or vulnerability conclusion is possible."],
        }
        output.write_text(json.dumps(failed, indent=2) + "\n", encoding="utf-8")
        print(f"::error::Action advisory watch unavailable ({type(exc).__name__}); report UNKNOWN.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
