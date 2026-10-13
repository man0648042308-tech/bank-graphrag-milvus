> 本仓库为个人作品集公开版：AI 大模型应用开发课程实战项目，模拟数据，非生产系统。更多项目见作品集主页。

# & 银行 GraphRAG 作业

这是一个可提交、可运行、可测试、可逐步复现的学习工程，覆盖原题 8 项要求：

1. Dijkstra、PageRank 学习总结与真实 GDS 运行；
2. Louvain 社区发现；
3. LangGraph + Neo4j GraphRAG，以及社区检索、解释、方法对比；
4. Milvus 2.6 稠密向量 + BM25 稀疏向量 + RRF 混合检索；
5. RAG 混合检索 10 道面试题；
6. Cypher 全部练习；
7. 带安全闸门的 NL2SQL；
8. 带安全闸门和参数化的 NL2Cypher。

## 先看哪个文件

- 交作业：`&作业_提交版.md`
- 不知道从哪里读：`docs/00_项目全景与阅读索引.md`
- 从零运行：`docs/01_逐步复现操作手册.md`
- 基础概念：`docs/02_核心概念逐词讲解.md`
- 面试题：`docs/03_RAG混合检索面试题10道.md`
- 报错处理：`docs/04_常见报错与排查.md`
- 闭卷训练：`docs/05_独立复现训练.md`
- 提交前检查：`docs/06_提交清单.md`
- AI 验收证据：`evidence/验收记录.md`

## 最短运行路径

在 PowerShell 中：

```powershell
Set-Location "./_Day36_GraphRAG_project"
$env:PYTHONIOENCODING = "utf-8"
uv sync --python 3.12
uv run python -m pytest -q
uv run python -m _project.main
```

预期：27 项测试通过；主程序输出 `P005、P001、P002`，不出现 `P003、P004`。

真实数据库：

```powershell
& ".\scripts\01_启动Neo4j_GDS.ps1"
& ".\scripts\02_导入并验收Neo4j.ps1"
uv run python ".\tests\verify_neo4j_integration.py"

& ".\scripts\04_启动Milvus.ps1"
uv run python ".\tests\verify_milvus_integration.py"
```

## 重要边界

- 数据全部为虚构教学数据，不是真实客户数据。
- `.env`、密码、Token 不进入仓库。
- NL2SQL/NL2Cypher 采用“生成 → AST/规则校验 → 白名单 → LIMIT → 执行”，不允许模型文本直接进入数据库。
- 删除仅允许作用于以 `_` 开头的 Milvus collection；Neo4j 只清理带 `dataset_id:''` 的节点。
- AI 已完成工程和验证，不等于学习者已经掌握；独立能力以闭卷复现、故障恢复和口述证据为准。

