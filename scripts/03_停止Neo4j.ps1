$ErrorActionPreference = "Stop"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

docker compose -f compose.neo4j.yml stop
Write-Host "已停止 day3536-neo4j-gds；数据卷仍保留，没有删除数据。"
