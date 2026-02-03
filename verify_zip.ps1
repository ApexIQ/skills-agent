$ErrorActionPreference = "Stop"

function Test-Command {
    param(
        [string]$Name,
        [scriptblock]$ScriptBlock,
        [scriptblock]$CheckBlock
    )
    Write-Host "Running Test: $Name..." -NoNewline
    try {
        & $ScriptBlock
        if ($CheckBlock) { & $CheckBlock }
        Write-Host " [PASS]" -ForegroundColor Green
    } catch {
        Write-Host " [FAIL]" -ForegroundColor Red
        Write-Host "Error: $_"
        exit 1
    }
}

if (Test-Path "test_zip_env") { Remove-Item "test_zip_env" -Recurse -Force }
New-Item -ItemType Directory -Path "test_zip_env" | Out-Null
Set-Location "test_zip_env"

# Test 1: List Categories (Should read JSON, ignoring zip)
Test-Command "List Categories" `
    { uv run skills-agent list --list-categories } `
    { }

# Test 2: Init Category (Should extract from zip)
Test-Command "Init Category (Security)" `
    { uv run skills-agent init --category security } `
    {
        if (!(Test-Path ".agents/skills/burp_suite_testing")) { throw "Extraction failed: burp_suite_testing missing" }
        if (Test-Path ".agents/skills/react_best_practices") { throw "Extraction leaking: react_best_practices present" }
    }

Set-Location ..
Remove-Item "test_zip_env" -Recurse -Force
Write-Host "`nZip Verification Completed."
