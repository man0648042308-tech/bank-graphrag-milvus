$ErrorActionPreference = "Stop"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

Write-Host "[1/4] 检查 Docker 引擎"
docker info --format "Docker Server version: {{.ServerVersion}}"
if ($LASTEXITCODE -ne 0) { throw "Docker 引擎未运行" }

$volumeNames = @(
    "day3536_neo4j_data",
    "day3536_neo4j_logs",
    "day3536_neo4j_plugins"
)
foreach ($volumeName in $volumeNames) {
    docker volume create $volumeName | Out-Null
}

$gdsVersion = "2.13.12"
$gdsJarName = "graph-data-science.jar"
$gdsUrl = "https://graphdatascience.ninja/neo4j-graph-data-science-$gdsVersion.jar"
$downloadDirectory = Join-Path $projectRoot "tmp"
$downloadPath = Join-Path $downloadDirectory "neo4j-graph-data-science-$gdsVersion.jar"
New-Item -ItemType Directory -Force -Path $downloadDirectory | Out-Null

docker run --rm --entrypoint sh `
    --mount "type=volume,source=day3536_neo4j_plugins,target=/plugins" `
    neo4j:5.26-community `
    -c "test -f /plugins/$gdsJarName && test `$(stat -c %s /plugins/$gdsJarName) -gt 60000000"
$gdsReady = $LASTEXITCODE -eq 0

if (-not $gdsReady) {
    if (-not (Test-Path -LiteralPath $downloadPath) -or
        (Get-Item -LiteralPath $downloadPath).Length -lt 60000000) {
        Write-Host "下载并校验 GDS $gdsVersion；只在插件卷缺失或损坏时执行"
        if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
            curl.exe -L --retry 3 --connect-timeout 20 --output $downloadPath $gdsUrl
            if ($LASTEXITCODE -ne 0) { throw "GDS 下载失败" }
        }
        else {
            Invoke-WebRequest -UseBasicParsing -Uri $gdsUrl -OutFile $downloadPath
        }
    }
    if ((Get-Item -LiteralPath $downloadPath).Length -lt 60000000) {
        throw "GDS 下载文件大小异常"
    }
    docker run --rm --entrypoint sh `
        --mount "type=volume,source=day3536_neo4j_plugins,target=/plugins" `
        --mount "type=bind,source=$downloadDirectory,target=/source,readonly" `
        neo4j:5.26-community `
        -c "cp /source/neo4j-graph-data-science-$gdsVersion.jar /plugins/$gdsJarName && chmod 644 /plugins/$gdsJarName"
    if ($LASTEXITCODE -ne 0) { throw "GDS 插件写入命名卷失败" }
}

Write-Host "[2/4] 启动本项目专用 Neo4j（端口 7475/7688）"
docker compose -f compose.neo4j.yml up -d
if ($LASTEXITCODE -ne 0) { throw "Neo4j 容器启动失败" }

Write-Host "[3/4] 查看容器状态"
docker compose -f compose.neo4j.yml ps

Write-Host "[4/4] 等待 Neo4j 就绪，并验证 APOC/GDS"
$deadline = (Get-Date).AddMinutes(5)
do {
    $status = docker inspect -f "{{.State.Health.Status}}" day3536-neo4j-gds 2>$null
    if ($status -eq "healthy") { break }
    Start-Sleep -Seconds 5
} while ((Get-Date) -lt $deadline)

if ($status -ne "healthy") {
    throw "Neo4j 未在 5 分钟内变为 healthy，请运行 docker logs day3536-neo4j-gds"
}

docker exec day3536-neo4j-gds cypher-shell `
    "RETURN apoc.version() AS apoc_version, gds.version() AS gds_version"
if ($LASTEXITCODE -ne 0) { throw "APOC/GDS 验证失败" }
