param(
    [ValidateSet("codex", "claude", "both")]
    [string]$Target = "both"
)

# Installs Skills only. Hook examples, including the OpenCode plugin example,
# are bundled under using-harness/hooks/ and are copied with the Skills.
$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function Install-HarnessSkills {
    param([string]$Destination)

    New-Item -ItemType Directory -Force $Destination | Out-Null
    Copy-Item (Join-Path $RepoRoot "skills\*") $Destination -Recurse -Force
    Write-Host "Installed Harness skills to $Destination"
}

switch ($Target) {
    "codex" {
        Install-HarnessSkills (Join-Path $HOME ".codex\skills")
    }
    "claude" {
        Install-HarnessSkills (Join-Path $HOME ".claude\skills")
    }
    "both" {
        Install-HarnessSkills (Join-Path $HOME ".codex\skills")
        Install-HarnessSkills (Join-Path $HOME ".claude\skills")
    }
}

Write-Host "Restart your agent so it can reload Skill metadata."
