"""Foundation regression: BXS packages must be audited and scanned, never waived.

These checks intentionally inspect the actual reusable workflows that product
repositories pin by full SHA. Credentials must come only from github.token in
short-lived, permission-scoped jobs; no caller-authenticated project npmrc.
"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2] / ".github" / "workflows"

def load(name):
    source = (ROOT / name).read_text()
    return yaml.safe_load(source), source

entry, _ = load("foundation-repository-gates.yml")
security, _ = load("reusable-foundation-security.yml")
adapters, adapters_text = load("reusable-foundation-dependency-adapters.yml")
container, container_text = load("reusable-foundation-container.yml")

for workflow in (entry, security, adapters, container):
    assert workflow["permissions"]["packages"] == "read"
    assert workflow["permissions"]["contents"] == "read"

assert entry["jobs"]["security"]["permissions"]["packages"] == "read"
assert security["jobs"]["native-deps"]["permissions"]["packages"] == "read"

configure = next(
    x for x in adapters["jobs"]["adapters"]["steps"]
    if x.get("name") == "Configure trusted GitHub Packages authentication"
)
assert configure["env"]["NODE_AUTH_TOKEN"] == "${{ github.token }}"
assert "pull_request.head.repo.full_name" in configure["run"]
assert 'github.repository' in configure["run"]
assert 'HOME/.npmrc' in configure["run"]
assert "@baobab-platform:registry=https://npm.pkg.github.com" in configure["run"]

node_audit = next(
    x for x in adapters["jobs"]["adapters"]["steps"]
    if x.get("name") == "Node dependency audit"
)
assert "pnpm install --frozen-lockfile" in node_audit["run"]
assert "pnpm audit --audit-level high" in node_audit["run"]
assert "|| true" not in node_audit["run"]

build = next(
    x for x in container["jobs"]["container"]["steps"]
    if x.get("name") == "Build container"
)
assert build["env"]["NODE_AUTH_TOKEN"] == "${{ github.token }}"
assert "--secret id=npm_token,env=NODE_AUTH_TOKEN" in build["run"]
assert "pull_request.head.repo.full_name" in build["run"]
assert "docker build" in build["run"]
assert "--build-arg NODE_AUTH_TOKEN" not in container_text
assert "--build-arg npm_token" not in container_text
assert "container-scan" in container_text
