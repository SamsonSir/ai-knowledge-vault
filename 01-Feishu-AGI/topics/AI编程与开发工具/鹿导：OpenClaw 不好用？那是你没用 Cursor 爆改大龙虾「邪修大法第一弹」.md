# AI编程与开发工具

## 27. [2026-02-12]

## 📚 文章 8


> 文档 ID: `RN55w9JIKiwEMVkhxbGcazJfnOf`

**来源**: 鹿导：OpenClaw 不好用？那是你没用 Cursor 爆改大龙虾「邪修大法第一弹」 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: OpenClaw（大龙虾）的本地向量记忆系统（QMD）默认未启用，导致记忆失效；用 Cursor 作为外部手术刀，4 步手动触发模型下载与索引构建，一次性激活后即可全自动运转。

**核心逻辑**:

- **记忆失效的根本原因**：OpenClaw 2.9 之前的老版本或升级用户，配置文件 `~/.openclaw/openclaw.json` 里 `memory.backend` 默认不是 `qmd`，系统跑在「无记忆模式」，且不会有任何提示。
- **两代记忆架构的本质差异**：v2.2 以前是 MEMORY.md 纯文本全量读取（每次对话消耗大量 Token，文件越大越慢，超出上下文直接截断）；v2.2 之后引入 RAG 向量检索，只取相关片段，效率质变。
- **QMD vs Embedding 两条路的选择逻辑**：官方默认走 Google 云端 Embedding API（快准但收费、数据上云）；QMD 是 GitHub 独立开源项目，全本地运行，三个模型全部开源，下载后断网可用，零费用。
- **QMD 哑火的直接原因**：第一次启动时需要下载约 2.2GB 本地模型，默认超时设置太短，下载未完成就超时报错，系统自动降级到效果差的备用方案（`switching to builtin index`），此后记忆检索形同虚设。
- **为什么不能让 OpenClaw 自己修自己**：在对话框里贴报错让它自修，相当于「喝醉的外科医生给自己做开颅手术」，它没有稳定的外部视角，越修越坏。必须用外部工具（Cursor）站在上帝视角操作。
- **Cursor 的角色定位**：不需要懂代码，Cursor Pro + Claude Sonnet 4.5 替你操作终端、改文件，是对非程序员最友好的外科手术工具。
- **QMD 三模型分工**：`embeddinggemma-300M`（文本向量化）+ `qmd-query-expansion-1.7B`（理解搜索意图）+ `qwen3-reranker-0.6b`（对结果重排序），三者协同才能完整跑通一次搜索。
- **自动更新机制的触发条件**：索引新文件每 5 分钟一次，生成向量每 60 分钟一次，防抖保护 15 秒。手动跑通一次后，后续全自动，无需人工干预。
- **记忆文件是人类可读的 Markdown**：存于 `~/.openclaw/workspace/memory/`，可直接用文本编辑器查看和手动写入，5 分钟后 QMD 自动索引。
- **模型只下载一次，全 Agent 共用缓存**：2.9 版本修复了重复下载问题，所有 Agent 复用 `~/.cache/qmd/models/` 下的缓存。

---

### 🎯 关键洞察

**为什么「升级用户」是重灾区**：从 v2.9 以前升级上来的用户，配置文件是老版本生成的，不包含 QMD 相关字段。新安装时如果没有手动勾选，同样缺失。OpenClaw 不会主动检测并提示你「记忆系统未激活」，这是一个静默失效的设计缺陷。

**RAG 的本质**：不是「更聪明的 AI」，而是「更聪明的信息检索」。向量化把文字转成数学坐标，语义相近的内容在坐标空间里距离近，搜索时找的是「距离最近的坐标」而不是「关键词匹配」，所以能理解「上周那个项目」和「2026-02-10 的会议记录」是同一件事。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 记忆后端切换 | `~/.openclaw/openclaw.json` 中 `memory.backend: "qmd"` | 启用本地向量检索 | 老版本升级用户配置文件里可能根本没有这个字段 |
| 搜索结果数量 | `"qmd": { "limits": { "maxResults": 8 } }` | 返回更多相关记忆片段 | 默认值偏小，可调大 |
| 搜索超时 | `"qmd": { "limits": { "timeoutMs": 5000 } }` | 防止搜索超时 | 电脑慢建议调到 `10000` |
| 索引数据库 | `~/.cache/qmd/index.sqlite` | 存储文件索引 | 体积小（几 MB），可安全保留 |
| 本地模型缓存 | `~/.cache/qmd/models/` | 三个模型共约 2.2GB | 唯一占空间的部分，删除后下次重新下载 |
| 日常记忆文件 | `~/.openclaw/workspace/memory/*.md` | 每次对话自动写入 | 可直接用文本编辑器手动添加内容 |
| 核心记忆文件 | `~/.openclaw/workspace/MEMORY.md` | 长期核心记忆 | Markdown 格式，人类可读 |

---

### 🛠️ 操作流程

**准备阶段**:
1. 确认 OpenClaw 已更新至 2.9 版本并完成 onboard
2. 打开 Cursor
3. 在 Cursor 中打开文件夹：`~/.openclaw`
4. 确认使用 Cursor Pro，模型选 Claude Sonnet 4.5

**核心执行**:

**第一步：检查 QMD 状态**

将以下内容发给 Cursor AI：

```
帮我检查一下 QMD 记忆检索的状态：
1. 运行 qmd status 看看索引情况
2. 检查 ~/.openclaw/openclaw.json 里的 memory 配置
3. 看看 ~/.openclaw/logs/gateway.err.log 里有没有 qmd 相关的错误
```

中招判断标准（出现任意一条即需继续）：

| 报错信息 | 含义 |
|---|---|
| `Total: 0 files indexed` | 无索引，记忆失效根本原因 |
| `qmd query failed: timed out` | 超时，模型未下载完 |
| `switching to builtin index` | 已降级到效果差的备用方案 |

---

**第二步：构建索引**

将以下内容发给 Cursor AI：

```
帮我执行 qmd update 构建文本索引，然后执行 qmd embed 生成向量。
第一次运行会自动下载本地模型（大约 2GB），请耐心等待。
```

预期输出：

```
Updating 3 collection(s)...
[1/3] memory-root (MEMORY.md)
Indexed: 1 new
[2/3] memory-alt (memory.md)
Indexed: 1 new
[3/3] memory-dir (**/*.md)
Indexed: 36 new
✓ All collections updated.

Embedding 37 documents (111 chunks, 210.8 KB)
Model: embeddinggemma
██████████████████████████████ 100%
✓ Done! Embedded 111 chunks from 37 documents in 9s
```

---

**第三步：触发完整搜索（下载剩余模型）**

将以下内容发给 Cursor AI：

```
帮我运行 qmd query "测试记忆搜索" -n 3
第一次搜索会下载查询扩展模型（约 1.3GB）和重排序模型（约 640MB），请等它下完。
```

三个模型下载详情：

| 模型名 | 大小 | 用途 | 下载时机 |
|---|---|---|---|
| embeddinggemma-300M | ~300MB | 文本向量化 | 第二步已下 |
| qmd-query-expansion-1.7B | ~1.3GB | 理解搜索意图 | 本步骤下载 |
| qwen3-reranker-0.6b | ~640MB | 搜索结果重排序 | 本步骤下载 |

成功标志（看到搜索结果即成功）：

```
qmd://memory-dir/2026-02-10-1548.md
Title: Session: 2026-02-10 15:48 UTC
Score: 72%
...相关内容片段...
```

---

**第四步：验证**

将以下内容发给 Cursor AI：

```
运行 qmd status 确认索引状态
```

预期输出：

```
Documents
  Total:    38 files indexed    ← 不再是 0 了！
  Vectors:  111 embedded        ← 有向量了！
  Updated:  刚才

Collections
  memory-root: 1 file
  memory-alt:  1 file
  memory-dir:  36 files
```

**验证与优化**:

激活后的自动运转机制：

| 动作 | 频率 | 说明 |
|---|---|---|
| 索引新文件 | 每 5 分钟 | 自动发现新的记忆文件 |
| 生成向量 | 每 60 分钟 | 自动给新文件生成搜索向量 |
| 防抖保护 | 15 秒 | 频繁写入时不会反复触发 |

完整数据流：
```
你跟大龙虾聊天
    ↓
大龙虾自动写入 ~/.openclaw/workspace/memory/2026-xx-xx.md
    ↓
5 分钟后 QMD 自动扫描到新文件，加入索引
    ↓
60 分钟后自动生成向量
    ↓
下次提问时 QMD 搜索相关记忆，大龙虾带着上下文回答
```

---

### 💡 具体案例/数据

- 实测搜索耗时：约 2-5 秒（MacBook Air CPU，无需显卡）
- 最大模型参数量：1.7B（qmd-query-expansion），MacBook Air 可跑
- 模型总占用空间：约 2.2GB，仅下载一次
- 索引数据库体积：几 MB（`index.sqlite`）
- 向量化示例：37 个文档，111 个 chunks，210.8KB，耗时 9 秒

---

### 📝 避坑指南

- ⚠️ 不要在 OpenClaw 对话框里贴报错让它自己修，会越修越坏，最终宕机
- ⚠️ 第三步的搜索命令必须跑，不跑的话 `qmd-query-expansion` 和 `qwen3-reranker` 两个模型不会下载，后续搜索质量大打折扣
- ⚠️ 电脑慢或网络差时，务必将 `timeoutMs` 调到 `10000`，否则搜索会持续超时降级
- ⚠️ 硬盘空间不足时，`~/.cache/qmd/models/`（2.2GB）是唯一可以删除的部分，删后下次自动重新下载，索引数据库（几 MB）不建议删
- ⚠️ 手动新建记忆文件后，索引更新有 5 分钟延迟，向量生成有 60 分钟延迟，不是实时生效

---

### 🏷️ 行业标签

#OpenClaw #大龙虾 #RAG #本地向量检索 #QMD #Cursor #AI记忆系统 #零代码邪修 #本地模型

---

---
