#!/usr/bin/env bash
# Runs the complete Foundation fixture suite. Used by CI and locally:
#   python3 -m pip install -r .github/foundation-tests/requirements.txt
#   scripts/test-foundation.sh
set -euo pipefail
cd "$(dirname "$0")/.."

for runtime in python3 ruby; do
  command -v "$runtime" >/dev/null || { echo "missing required runtime: $runtime" >&2; exit 1; }
done
python3 -c "import jsonschema, yaml" 2>/dev/null || {
  echo "missing Python dependencies; install .github/foundation-tests/requirements.txt" >&2
  exit 1
}

python3 .github/foundation-tests/test_contracts.py
python3 .github/foundation-tests/test_workflow_wiring.py
python3 .github/foundation-tests/test_caller_template.py
python3 .github/foundation-tests/test_org_conformance.py
ruby .github/foundation-tests/test_policy.rb
