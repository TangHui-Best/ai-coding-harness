param(
    [Parameter(Position = 0)]
    [ValidateSet("codex", "claude", "both")]
    [string]$Target = "both",
    [switch]$Verify
)

# Installs Skills only. Hook examples, including the OpenCode plugin example,
# are bundled under using-agentmentor/hooks/ and are copied with the Skills.
$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

$FormalSkills = @(
    "using-agentmentor",
    "start-gate",
    "delegation-gate",
    "knowledge-retrieval",
    "spec-drift",
    "doc-lifecycle",
    "incident-learning",
    "vision-gate",
    "readiness-dashboard",
    "change-narrative",
    "knowledge-capture",
    "project-rules"
)

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

$RequiredBundledResources = @(
    "using-agentmentor\scripts\knowledge_check.py",
    "using-agentmentor\scripts\closeout_check.py",
    "using-agentmentor\scripts\hook_diagnostics.py",
    "using-agentmentor\hooks\agentmentor_hook.py",
    "using-agentmentor\assets\templates\AGENTS.md"
)

function Get-AgentMentorDestination {
    param([ValidateSet("codex", "claude")] [string]$Name)

    if ($Name -eq "codex" -and $env:AGENTMENTOR_CODEX_SKILLS_DIR) {
        return $env:AGENTMENTOR_CODEX_SKILLS_DIR
    }
    if ($Name -eq "claude" -and $env:AGENTMENTOR_CLAUDE_SKILLS_DIR) {
        return $env:AGENTMENTOR_CLAUDE_SKILLS_DIR
    }
    if ($Name -eq "codex") {
        return (Join-Path $HOME ".codex\skills")
    }
    return (Join-Path $HOME ".claude\skills")
}

function Test-AgentMentorInstall {
    param(
        [string]$Destination,
        [string]$Label
    )

    $Errors = New-Object System.Collections.Generic.List[string]
    if (-not (Test-Path $Destination)) {
        $Errors.Add("destination does not exist: $Destination")
    }

    foreach ($Skill in $FormalSkills) {
        $SkillFile = Join-Path $Destination (Join-Path $Skill "SKILL.md")
        if (-not (Test-Path $SkillFile)) {
            $Errors.Add("missing $Skill/SKILL.md in $Destination")
        }
    }

    foreach ($SkillDir in $RemovedSkillDirs) {
        $Path = Join-Path $Destination $SkillDir
        if (Test-Path $Path) {
            $Errors.Add("removed legacy skill still exists: $Path")
        }
    }

    foreach ($Resource in $RequiredBundledResources) {
        $Path = Join-Path $Destination $Resource
        if (-not (Test-Path $Path)) {
            $Errors.Add("missing bundled resource: $Path")
        }
    }

    if ($Errors.Count -gt 0) {
        foreach ($Message in $Errors) {
            [Console]::Error.WriteLine("Verification error: $Message")
        }
        throw "Verification: failed for $Label with $($Errors.Count) error(s)."
    }

    Write-Host "Verification: passed for $Label at $Destination"
}

function Install-AgentMentorSkills {
    param(
        [string]$Destination,
        [string]$Label
    )

    New-Item -ItemType Directory -Force $Destination | Out-Null
    foreach ($SkillDir in $RemovedSkillDirs) {
        $Target = Join-Path $Destination $SkillDir
        if (Test-Path $Target) {
            Remove-Item -LiteralPath $Target -Recurse -Force
        }
    }
    Copy-Item (Join-Path $RepoRoot "skills\*") $Destination -Recurse -Force
    Write-Host "Installed AgentMentor skills to $Destination"
    Test-AgentMentorInstall $Destination $Label
}

function Invoke-AgentMentorVerify {
    param(
        [string]$Destination,
        [string]$Label
    )

    Write-Host "Verify-only: no files were copied for $Label."
    Test-AgentMentorInstall $Destination $Label
}

function Write-AgentMentorNextSteps {
    Write-Host "Restart your agent so it can reload Skill metadata."
    Write-Host "Use ``using-agentmentor`` as the entrypoint after restart."
    Write-Host "Hooks are optional. To check Codex Stop hook runtime after hook setup, run:"
    Write-Host "  python <skills-root>/using-agentmentor/scripts/hook_diagnostics.py codex --project-root <project>"
}

switch ($Target) {
    "codex" {
        $Destination = Get-AgentMentorDestination "codex"
        if ($Verify) {
            Invoke-AgentMentorVerify $Destination "Codex"
        } else {
            Install-AgentMentorSkills $Destination "Codex"
        }
    }
    "claude" {
        $Destination = Get-AgentMentorDestination "claude"
        if ($Verify) {
            Invoke-AgentMentorVerify $Destination "Claude Code"
        } else {
            Install-AgentMentorSkills $Destination "Claude Code"
        }
    }
    "both" {
        $CodexDestination = Get-AgentMentorDestination "codex"
        $ClaudeDestination = Get-AgentMentorDestination "claude"
        if ($Verify) {
            Invoke-AgentMentorVerify $CodexDestination "Codex"
            Invoke-AgentMentorVerify $ClaudeDestination "Claude Code"
        } else {
            Install-AgentMentorSkills $CodexDestination "Codex"
            Install-AgentMentorSkills $ClaudeDestination "Claude Code"
        }
    }
}

Write-AgentMentorNextSteps
