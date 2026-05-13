param(
    [ValidateSet("codex", "claude", "both")]
    [string]$Target = "both"
)

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
