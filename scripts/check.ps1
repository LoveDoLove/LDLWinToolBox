# LDLWinToolBox -- unified lint & format check
# Requires: uv
# Usage: .\scripts\check.ps1 [-Fix]

param(
    [switch]$Fix = $false
)

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$global:ExitCode = 0

Write-Host "=== ruff format check ===" -ForegroundColor Cyan
if ($Fix) {
    uv run -- ruff format .
} else {
    uv run -- ruff format --check .
}
if (-not $?) { $global:ExitCode = 1 }

Write-Host "=== ruff lint check ===" -ForegroundColor Cyan
if ($Fix) {
    uv run -- ruff check --fix .
} else {
    uv run -- ruff check .
}
if (-not $?) { $global:ExitCode = 1 }

Write-Host "=== ruff isort check ===" -ForegroundColor Cyan
if ($Fix) {
    uv run -- ruff check --select I --fix .
} else {
    uv run -- ruff check --select I .
}
if (-not $?) { $global:ExitCode = 1 }

if ($global:ExitCode) {
    Write-Host "FAILED - run with -Fix to auto-fix" -ForegroundColor Red
} else {
    Write-Host "ALL CHECKS PASSED" -ForegroundColor Green
}
exit $global:ExitCode
