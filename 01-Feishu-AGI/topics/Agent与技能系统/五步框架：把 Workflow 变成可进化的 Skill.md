# Agent与技能系统

## 5. [2026-01-11]

## 📗 文章 2


> 文档 ID: `ORl1wdKrWitfxGk0XI6cwHYUnJH`

**来源**: 五步框架：把 Workflow 变成可进化的 Skill | **时间**: 2026-01-11 | **原文链接**: https://mp.weixin.qq.com/s/R0WNSWPk...

---

### 📋 核心分析

**战略价值**: 用「拆分→编排→存储→分摊→迭代」五步框架，将任何可视化 Workflow 重构为基于本地文件的 Agent + Skills 架构，获得可进化、可移植、可并行的自动化资产。

**核心逻辑**:

- **Workflow 的三大硬伤**：①表达能力有限，复杂逻辑难以用节点表达；②输入变化即崩溃，为 A 类文档设计的流程遇到 B 类文档直接卡死；③平台锁定，导出导入一通操作还得在对方环境重新调试。
- **Skill ≠ 单一技能**：大多数人把 skill 当翻译/总结这类原子操作，实际上 skill 应是「可组合模块」——用自然语言描述多个 skill 之间的协作关系，本质是「用自然语言编排工作流」。
- **第一步·拆分**：每个 skill/subagent 只做一件事。写作流程拆为：`article-analyzer`（分析素材→输出 analysis.md）、`outliner`（生成 2-3 个提纲方案）、`writer-agent`（根据提纲写草稿，可并行多个）、`polish`（润色定稿）。配图流程拆为：`generate-image`（原子技能，调用图像生成 API）、`article-illustrator`（组合技能，分析文章→识别配图位置→生成插图）、`cover-image`（组合技能，生成 2.35:1 封面图）。写作+配图再组合成完整写作工作流。
- **第二步·编排**：在主 skill 里用自然语言描述整个流程。示例——outliner 的编排描述："先调用 article-analyzer 分析素材，分析完成后保存 analysis.md，然后根据分析结果生成 2-3 个不同风格的提纲方案，为每个方案并行启动 writer-agent 写草稿。" article-illustrator 的编排描述："读取文章内容，识别需要配图的位置（概念抽象处、信息密集处、情感转折处），为每个位置生成图像描述，调用 generate-image 生成图片，最后将图片插入文章对应位置。" 条件分支、并行执行、错误处理均可用自然语言描述，Agent 能理解。
- **第三步·存储**：所有中间结果保存为本地文件。文件链路：`source.md → analysis.md → outline-a.md → draft-outline-a.md → final.md`。三大好处：①可追溯（每步输出有迹可循）；②可断点续传（中途停了下次从上次位置继续）；③可人工干预（手动修改某步结果后让 Agent 继续）。
- **第四步·分摊**：Subagent 之间只传文件路径，不传内容。直接传大段内容会撑满上下文窗口；只传路径则 subagent 自己读文件，上下文保持干净。writer-agent 启动只需三个参数：source 文件路径、analysis 文件路径、outline 文件路径，写完保存到指定路径，返回输出文件路径。此设计支持并行：三个 writer-agent 同时跑，各自处理一个提纲方案，互不干扰。
- **第五步·迭代**：Skill 是文

---

---
