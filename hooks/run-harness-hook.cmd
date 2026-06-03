: << 'HARNESS_CMD'
@echo off
setlocal

set "EVENT=%~1"
if "%EVENT%"=="" (
    echo run-harness-hook.cmd: missing event name 1>&2
    exit /b 1
)

set "HOOK_DIR=%~dp0"
for %%I in ("%HOOK_DIR%..") do set "PLUGIN_ROOT=%%~fI"
set "RUNNER=%PLUGIN_ROOT%\skills\using-harness\hooks\harness_hook.py"

if not exist "%RUNNER%" (
    echo run-harness-hook.cmd: missing Harness runner: %RUNNER% 1>&2
    exit /b 1
)

python "%RUNNER%" --event "%EVENT%" --platform codex
exit /b %ERRORLEVEL%
HARNESS_CMD

# Unix fallback for shells that execute this file directly.
EVENT="$1"
if [ -z "$EVENT" ]; then
    echo "run-harness-hook.cmd: missing event name" >&2
    exit 1
fi

HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$HOOK_DIR/.." && pwd)"
RUNNER="$PLUGIN_ROOT/skills/using-harness/hooks/harness_hook.py"

if [ ! -f "$RUNNER" ]; then
    echo "run-harness-hook.cmd: missing Harness runner: $RUNNER" >&2
    exit 1
fi

exec python "$RUNNER" --event "$EVENT" --platform codex
