$ErrorActionPreference = "Stop"
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$projectRoot = Split-Path -Parent $PSScriptRoot
$cypherFiles = @(
    "cypher\01_初始化银行图数据.cypher",
    "cypher\02_Cypher全部练习答案.cypher",
    "cypher\03_Dijkstra_PageRank_Louvain.cypher",
    "cypher\04_验收断言.cypher"
)

Set-Location -LiteralPath $projectRoot

foreach ($relativePath in $cypherFiles) {
    $absolutePath = Join-Path $projectRoot $relativePath
    Write-Host "正在执行：$absolutePath"
    $cypher = Get-Content -Raw -Encoding UTF8 -LiteralPath $absolutePath
    $cypher | docker exec -i day3536-neo4j-gds cypher-shell --format plain
    if ($LASTEXITCODE -ne 0) {
        throw "执行失败：$absolutePath"
    }
}

Write-Host "四份 Cypher 脚本均已执行。请向上查看 Dijkstra、PageRank、Louvain 和断言输出。"
