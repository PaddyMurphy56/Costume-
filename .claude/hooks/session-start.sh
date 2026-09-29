#!/bin/bash
# SessionStart hook: installs Python dependencies so lint, tests and the
# validator work in every Claude Code on the web session.
set -euo pipefail

# Only needed in the remote (web) environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

if ! command -v uv >/dev/null 2>&1; then
  pip install --quiet uv
fi

# Idempotent: uv sync is a no-op when .venv already matches uv.lock.
uv sync --quiet

# Put the project venv first on PATH for the rest of the session.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$PWD/.venv/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi
