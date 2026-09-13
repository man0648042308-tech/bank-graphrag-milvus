$ErrorActionPreference = "Stop"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

# 凭据只存在于当前进程和容器环境，不写入项目文件，也不打印。
$env:DAY3536_MINIO_USER = "day3536_" + [Guid]::NewGuid().ToString("N").Substring(0, 12)
$env:DAY3536_MINIO_PASSWORD = [Guid]::NewGuid().ToString("N")

foreach ($volumeName in @(
    "day3536_milvus_etcd",
    "day3536_milvus_minio",
    "day3536_milvus_data"
)) {
    docker volume create $volumeName | Out-Null
}

Write-Host "[1/3] 启动本作业专用 Milvus 2.6.17（宿主机端口 19531）"
docker compose -f compose.milvus.yml up -d
if ($LASTEXITCODE -ne 0) { throw "Milvus 容器启动失败" }

Write-Host "[2/3] 等待 Milvus 健康检查，首次下载镜像可能需要数分钟"
$deadline = (Get-Date).AddMinutes(10)
do {
    $status = docker inspect -f "{{.State.Health.Status}}" day3536-milvus-standalone 2>$null
    if ($status -eq "healthy") { break }
    Start-Sleep -Seconds 10
} while ((Get-Date) -lt $deadline)

if ($status -ne "healthy") {
    throw "Milvus 未在 10 分钟内变为 healthy，请运行 docker logs day3536-milvus-standalone"
}

Write-Host "[3/3] Milvus 已就绪"
docker compose -f compose.milvus.yml ps
