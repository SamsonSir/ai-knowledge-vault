# Agent与技能系统

## 45. [2026-02-01]

## 📔 文章 5


> 文档 ID: `PrkywkqSJiQ9XOk7Oj2cABAgnuc`

**来源**: [译]OpenClaw 技术架构深度解析 | **时间**: 2026-02-01 | **原文链接**: `https://mp.weixin.qq.com/s/qc9rrceC...`

---

### 📋 核心分析

**战略价值**: OpenClaw 是一个 TypeScript CLI 进程，通过 lane 队列串行化、混合记忆检索、Playwright 语义快照三大机制，实现可靠的本地 AI 助手架构——理解它的设计决策，能直接指导你构建自己的 agentic 系统。

**核心逻辑**:

- **技术本质是 TypeScript CLI 进程，不是 Web App**：它在本地运行，暴露 Gateway Server 处理 Telegram/WhatsApp/Slack 等渠道连接，调用 Anthropic/OpenAI/本地模型 API，并在本地执行工具。
- **消息流经 6 层处理**：Channel Adapter（标准化消息）→ Gateway Server（会话协调）→ Agent Runner（拼装 prompt）→ LLM API Call（流式调用）→ Agentic Loop（工具执行循环）→ Response Path（回写渠道 + 持久化 JSONL）。
- **Lane-based 命令队列是串行化的核心设计**：一个 session 独占一条 lane，默认串行执行；只有低风险可并行任务（如 cron）才显式开并行 lane。这直接规避了 async/await 乱麻和共享状态竞态条件问题。
- **Agent Runner 动态拼装 system prompt**：每次调用前实时组合可用 tools + skills + memory，再追加 session 历史（从 .jsonl 读取），然后过 Context Window Guard 检查剩余空间，快满时压缩 session 或优雅失败。
- **API Key 管理有 cooldown 机制**：某个 key 不可用时自动标记 cooldown 并切换下一个，主模型失败时 fallback 到备用模型，保证可用性。
- **记忆系统双轨并行**：JSONL 会话转录（逐行记录用户消息/工具调用/工具结果/模型回复）+ Markdown 记忆文件（存于 `MEMORY.md` 或 `memory/` 目录），agent 通过普通"写文件"工具自主生成记忆，无专用 memory-write API。
- **记忆检索用 SQLite 双引擎混合方案**：向量检索（SQLite 存储 embedding）+ FTS5 全文检索，同时命中语义相似（"auth issues" → "authentication bug"）和精确关键词，embedding provider 可配置。
- **新对话开始时有 hook 自动生成上一段对话的 Markdown 摘要**，但没有记忆合并、没有按周/月压缩，旧记忆与新记忆权重相同，无遗忘曲线。
- **Computer Use 执行环境三选一**：sandbox（默认，Docker 容器）、宿主机直接执行、远程设备执行，通过 exec 工具运行 shell 命令。
- **浏览器工具基于 Playwright + 语义快照**：优先用 ARIA accessibility tree 的文本化表示而非截图，一张截图约 5MB，语义快照不到 50KB，token 成本差距极大。

---

### 🎯 关键洞察

**为什么 Lane 队列比 async/await 更可靠**：

多 agent 系统最常见的工程事故是：日志交错不可读 + 共享状态竞态。Lane 队列把"串行"设为默认值，开发者的心智模型从"我需要加什么锁？"变成"哪些东西是安全可并行的？"——这是架构层面的认知负担转移，而不是运行时补丁。Cognition 的博文《不要构建多代理系统》也印证了这一判断。

**为什么语义快照比截图更适合 agent 浏览器操作**：

浏览网页本质上不是视觉任务，而是结构化交互任务。截图的 token 成本远高于文本，且 LLM 处理图像的精度不如处理结构化文本。语义快照直接给出可操作的 ref 引用（`button "Sign In" [ref=1]`），agent 可以精确定位元素，无需视觉推理。

**记忆系统"简单"是有意为之的权衡**：

没有记忆合并、没有遗忘曲线，意味着系统行为可预测、可调试。复杂的记忆压缩系统会引入"记忆失真"风险，而 Markdown 文件 + JSONL 的方案让用户可以直接打开文件查看和手动修改记忆内容。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| exec 命令白名单 | `~/.clawdbot/exec-approvals.json`，见下方配置块 | 用户可选"允许一次/永久允许/拒绝" | lastUsedAt 是 Unix 时间戳 |
| 预批准安全命令 | `jq, grep, cut, sort, uniq, head, tail, tr, wc` | 无需用户确认直接执行 | 仅限这些只读/无副作用命令 |
| 默认拦截的危险构造 | 命令替换 `$(...)`、重定向 `>`、逻辑或链 `\|\|`、子 shell `(...)` | 执行前直接拒绝 | 见下方示例 |
| 记忆向量检索 | SQLite 存储 embedding，provider 可配置 | 语义相似匹配 | embedding provider 需单独配置 |
| 记忆关键词检索 | SQLite FTS5 全文检索扩展 | 精确短语命中 | 与向量检索混合使用 |
| 浏览器工具 | Playwright + ARIA accessibility tree | 语义快照 <50KB vs 截图 ~5MB | 对无障碍属性差的页面效果下降 |
| 上下文窗口守卫 | Context Window Guard，上下文快满时触发 | 压缩 session 或优雅失败 | 默认最大轮数约 20 轮 |
| 并行执行 | Lane-based queue，cron 等低风险任务可开并行 lane | 规避竞态条件 | 默认串行，并行需显式声明 |

**exec-approvals.json 配置示例**：
```json
// ~/.clawdbot/exec-approvals.json
{
  "agents": {
    "main": {
      "allowlist": [
        { "pattern": "/usr/bin/npm", "lastUsedAt": 1706644800 },
        { "pattern": "/opt/homebrew/bin/git", "lastUsedAt": 1706644900 }
      ]
    }
  }
}
```

**默认拦截的危险 shell 构造**：
```bash
npm install $(cat /etc/passwd)  # 命令替换，拦截
cat file > /etc/hosts           # 重定向，拦截
rm -rf / || echo "failed"       # 逻辑或链式执行，拦截
(sudo rm -rf /)                 # 子 shell，拦截
```

---

### 🛠️ 操作流程

1. **消息接收阶段**: Channel Adapter 接收消息 → 标准化处理 + 提取附件 → 传入 Gateway Server → 分配到对应 session 的 lane 队列
2. **Prompt 拼装阶段**: Agent Runner 动态组合 system prompt（tools + skills + memory）→ 追加 .jsonl session 历史 → Context Window Guard 检查剩余空间 → 空间不足则压缩或失败
3. **LLM 调用阶段**: 选择模型 + 可用 API Key（cooldown 机制自动切换）→ 流式调用 LLM API → 支持 extended thinking（模型支持时）→ 主模型失败自动 fallback
4. **Agentic Loop 阶段**: LLM 返回工具调用 → 本地执行工具（exec/文件系统/浏览器/进程管理）→ 结果追加回对话 → 重复直到输出最终文本或达到 max turns（约 20）
5. **持久化阶段**: 回复写回渠道 → session 持久化到 JSONL 文件（每行一个 JSON 对象）→ 新对话开始时 hook 触发，生成上一段对话的 Markdown 摘要写入 memory/

---

### 📦 浏览器语义快照示例

agent 实际看到的页面结构（非截图）：
```
- button "Sign In" [ref=1]
- textbox "Email" [ref=2]
- textbox "Password" [ref=3]
- link "Forgot password?" [ref=4]
- heading "Welcome back"
- list
  - listitem "Dashboard"
  - listitem "Settings"
```

---

### 📝 避坑指南

- ⚠️ **记忆无遗忘曲线**：旧记忆与新记忆权重相同，长期使用后旧的错误记忆不会自动淡出，需手动清理 `memory/*.md` 文件。
- ⚠️ **没有记忆合并机制**：同一主题的多条记忆不会自动合并，可能出现矛盾记忆共存的情况。
- ⚠️ **max turns 约 20 轮**：复杂任务可能在完成前被截断，需要合理拆分任务粒度。
- ⚠️ **语义快照依赖页面无障碍属性**：ARIA 属性缺失的页面（大量自定义 UI 组件）会导致快照质量下降，此时才需要回退到截图模式。
- ⚠️ **并行 lane 需显式声明**：默认串行，不要假设任务会自动并行执行，cron 等任务需要明确配置并行 lane。
- ⚠️ **sandbox 是默认执行环境**：直接在宿主机执行需要显式配置，误操作风险高，生产环境务必确认执行环境设置。

---

### 🏷️ 行业标签

#AGI架构 #TypeScript #AIAgent #LLM工程 #记忆系统 #ComputerUse #浏览器自动化 #串行化架构 #工具调用

---

---
