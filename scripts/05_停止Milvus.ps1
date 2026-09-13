$ErrorActionPreference = "Stop"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

# Compose 解析文件时仍要求变量存在，停止动作使用临时占位值即可。
$env:DAY3536_MINIO_USER = "stop_only"
$env:DAY3536_MINIO_PASSWORD = "stop_only_not_used"
docker compose -f compose.milvus.yml stop
Write-Host "已停止 Day35/Day36 Milvus；命名卷仍保留，没有删除数据。"
