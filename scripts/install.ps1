param(
    [ValidateSet("codex", "claude", "both")]
    [string]$Target = "both"
)

# Installs Skills only. Hook examples, including the OpenCode plugin example,
# are bundled under using-agentmentor/hooks/ and are copied with the Skills.
$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function Install-AgentMentorSkills {
    param([string]$Destination)

    New-Item -ItemType Directory -Force $Destination | Out-Null
    $RemovedSkillDirs = @(
        "using-harness",
        "harness-start-gate",
        "harness-delegation-gate",
        "harness-knowledge-retrieval",
        "harness-doc-lifecycle",
        "harness-incident-learning",
        "harness-vision-gate",
        "harness-readiness-dashboard",
        "harness-change-narrative",
        "harness-knowledge-capture",
        "harness-project-rules",
        "ai-coding-harness",
        "ai-coding-harness-start-gate",
        "ai-coding-harness-delegation-gate",
        "ai-coding-harness-knowledge-retrieval",
        "ai-coding-harness-doc-lifecycle",
        "ai-coding-harness-incident-learning",
        "ai-coding-harness-vision-gate",
        "ai-coding-harness-readiness-dashboard",
        "ai-coding-harness-change-narrative",
        "ai-coding-harness-knowledge-capture",
        "ai-coding-harness-project-rules"
    )
    foreach ($SkillDir in $RemovedSkillDirs) {
        $Target = Join-Path $Destination $SkillDir
        if (Test-Path $Target) {
            Remove-Item -LiteralPath $Target -Recurse -Force
        }
    }
    Copy-Item (Join-Path $RepoRoot "skills\*") $Destination -Recurse -Force
    Write-Host "Installed AgentMentor skills to $Destination"
}

switch ($Target) {
    "codex" {
        Install-AgentMentorSkills (Join-Path $HOME ".codex\skills")
    }
    "claude" {
        Install-AgentMentorSkills (Join-Path $HOME ".claude\skills")
    }
    "both" {
        Install-AgentMentorSkills (Join-Path $HOME ".codex\skills")
        Install-AgentMentorSkills (Join-Path $HOME ".claude\skills")
    }
}

Write-Host "Restart your agent so it can reload Skill metadata."
