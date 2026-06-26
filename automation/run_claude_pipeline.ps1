# Claude Code CLI 流水线入口（PowerShell）
# 用法: .\automation\run_claude_pipeline.ps1
# 需已安装 claude CLI 并完成 anthropic 登录

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "== 1. Docker 服务检查 ==" -ForegroundColor Cyan
docker compose ps 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "启动 Docker Compose..." -ForegroundColor Yellow
    docker compose up -d --build
}

Write-Host "== 2. Python 流水线 ==" -ForegroundColor Cyan
python automation/pipeline.py @args

Write-Host "== 3. Claude Code 汇总（可选）==" -ForegroundColor Cyan
if (Get-Command claude -ErrorAction SilentlyContinue) {
    $prompt = Get-Content -Raw (Join-Path $PSScriptRoot "CLAUDE_PROMPT.md")
    claude -p $prompt
} else {
    Write-Host "未检测到 claude CLI，跳过 Claude 汇总。可手动: claude -p (Get-Content automation/CLAUDE_PROMPT.md -Raw)" -ForegroundColor Yellow
}

Write-Host "完成。outbox: automation/outbox | 日志: automation/logs/pipeline.log" -ForegroundColor Green
