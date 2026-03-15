# Agent与技能系统

## 43. [2026-01-31]

## 📓 文章 6


> 文档 ID: `TwqDwO8f1inNlGkdqwQcMIL6nxc`

**来源**: 谈谈Agent Skills的底层原理 | **时间**: 2026-01-18 | **原文链接**: `https://mp.weixin.qq.com/s/YFQtx9QJ...`

---

### 📋 核心分析

**战略价值**: Agent Skills 本质是 Context Offloading 策略在文件系统上的工程落地——通过三层按需加载机制，让 LLM 只在需要时才把知识加载进上下文，从而在能力扩展与上下文效率之间取得最优平衡。

**核心逻辑**:

- **ReAct 是现代 Agent 的基础范式**：将 LLM 推理（Reasoning）与工具调用（Acting）交替执行，Agent 反复"思考→调用工具→观察结果→再思考"，直到完成目标。Function Calling 的引入是 ReAct 效果从"不理想"跃升到"可靠高效"的关键转折点。

- **Claude Code 的特殊性在于其工具集**：与天气查询等普通 Agent 不同，Claude Code 的几乎所有工具都围绕**文件系统 + Shell 命令**展开（`Bash`、`Read`、`Write` 等），这是理解 Skills 的前提。

- **LLM 上下文有两个硬约束**：①窗口大小有上限（早期 GPT-3 仅 2048 token，Claude Sonnet 4.5 已达百万 token 但仍有上限）；②上下文过载会导致性能显著下降，包括 Lost in the Middle、Context Poisoning（上下文污染）、Context Confusion（上下文混淆）三类问题。

- **Context Offloading 的定义**：将信息存到 LLM 上下文之外，通过能管理数据的工具按需取回。与 RAG、Context Summarization、Context Quarantine 并列为四大上下文管理策略。

- **Skills 的第一性原理推导**：Claude Code 基于文件系统，因此 Context Offloading 的自然实现路径是：①信息存文件系统而非预塞进上下文；②系统提示词中记录文件位置；③用户提问时 Agent 按需用 `Read` 工具取回；④取回内容动态注入上下文辅助完成任务。

- **Skills 三层加载机制**（核心架构）：
  - **第一层 Metadata（元数据）**：可用 Skills 的名称、描述、文件路径，**预先写入系统提示词**，确保 Agent 知道有哪些 Skill 可用。
  - **第二层 Instructions（指令）**：每个 Skill 对应一个 `SKILL.md` 文件，含详细描述、使用方法、示例。Agent 需要某 Skill 时，调用 `Read` 工具**动态加载**该文件内容到上下文。
  - **第三层 Resources（资源）**：Skill 目录下的其他资源文件（配置、文档等），Agent 需要更具体信息时**进一步按需读取**。

- **三层设计的目的是最大化减少上下文负担**：只有真正用到的 Skill 内容才会进入上下文，且是分层渐进加载，而非一次性全量注入。

- **Skills 完整能力还涉及两个维度**：①**Code Execution（代码执行）**：Skill 可包含代码片段，Agent 也可动态生成代码并执行；②**Virtual Machine（虚拟机）**：文件系统管理、Shell 命令、代码运行均在隔离沙盒（VM）中进行，保障安全性。

- **Skills 与 `resources/` 目录的等价关系**：将示例中的 `resources/` 重命名为 `skills/`，`frontend-design.md` 本质上就是一个 Skill，对应 `anthropics/skills/frontend-design/SKILL.md`。

---

### 🎯 关键洞察

**为什么三层加载比"全量预加载"更优**：

原因 → 动作 → 结果的链条：
- LLM 上下文过载 → 性能下降（Lost in the Middle 等问题）→ 需要减少无关内容进入上下文
- 但 Agent 需要知道"有什么可用" → 只把 Metadata（名称+路径）放进系统提示词 → 上下文占用极小
- Agent 判断需要某 Skill → 用 `Read` 读取 `SKILL.md` → 只有相关 Skill 的指令进入上下文
- 需要更细节的资源 → 再次 `Read` 具体资源文件 → 精准注入，零冗余

这与 RAG 的思路一脉相承，但 Skills 的实现更轻量：不需要向量数据库，直接依赖文件系统 + LLM 的路径理解能力。

---

### 📦 配置/工具详表

| 层级 | 内容 | 存放位置 | 加载时机 | 加载方式 |
|------|------|---------|---------|---------|
| Metadata | Skill 名称、描述、路径 | 系统提示词（System Prompt） | 会话开始时预加载 | 直接写入 System Prompt |
| Instructions | 详细描述、用法、示例 | `skills/<name>/SKILL.md` | Agent 判断需要该 Skill 时 | `Read` 工具读取 |
| Resources | 配置文件、文档等 | `skills/<name>/` 目录下 | Agent 需要更具体信息时 | `Read` 工具读取 |
| Code Execution | 代码片段 / 动态生成代码 | Skill 文件或运行时生成 | 任务执行阶段 | `Bash` 工具执行 |
| Virtual Machine | 沙盒隔离环境 | 底层基础设施 | 全程 | 系统级隔离 |

---

### 🛠️ 操作流程

**以"生成博客前端页面"为例，完整复刻 Skills 的工作流：**

1. **准备阶段：创建 Skill 文件**

   将设计指南存入文件系统，而非塞进系统提示词：
   ```
   # 文件路径: skills/frontend-design/SKILL.md
   
   # Frontend Aesthetics Guidelines
   
   Focus on:
   
   **Typography**: Choose fonts that are beautiful, unique, and interesting...
   
   **Color & Theme**: Commit to a cohesive aesthetic...
   ```

2. **核心执行：在系统提示词中注册 Metadata**

   只写路径引用，不写全文内容：
   ```
   You are Claude Code...
   
   You have access to the following resources:
   - `skills/frontend-design/SKILL.md`: Guidelines for designing the frontend UI.
   ```

3. **运行时按需加载（Context 完整流）**：

   ```
   System: You are Claude Code...\n\nYou have access to the following resources:\n- `skills/frontend-design/SKILL.md`: Guidelines for designing the frontend UI.
   
   User: Generate a blog frontend UI.
   
   Assistant: ToolCall(name="Read", args={"file_path": "skills/frontend-design/SKILL.md"})
   
   User: ToolOutput(result="Choose fonts that are beautiful, unique, and interesting...")
   
   Assistant: ToolCall(name="Write", args={"file_path": "app/index.html", "content": "<html>...</html>"})
   
   User: ToolOutput(result="Created file `app/index.html`.")
   
   Assistant: ToolCall(name="Write", args={"file_path": "app/styles.css", "content": "..."})
   
   User: ToolOutput(result="Created file `app/styles.css`.")
   
   Assistant: I've generated a simple blog frontend UI based on the guidelines.
   ```

4. **验证与优化**：
   - 确认 Agent 只在用户请求前端相关任务时才触发 `Read` 调用（按需加载验证）
   - 若 Agent 未主动读取 SKILL.md，检查系统提示词中的 Metadata 描述是否足够清晰
   - 若上下文仍过大，将 SKILL.md 中的资源文件拆分到 `skills/frontend-design/resources/` 子目录，实现第三层按需加载

---

### 💡 具体案例/数据

**ReAct Agent 天气查询完整 Context 示例**：
```
System: You are a helpful weather assistant.
User: What is the weather like in Chengdu?
Assistant: ToolCall(name="get_weather", args={"location": "Chengdu"})
User: ToolOutput(result={"weather": "Sunny", "temperature": "22°C"})
Assistant: The weather in Chengdu is Sunny with a temperature of 22°C.
```

**Claude Code 文件操作完整 Context 示例**：
```
System: You are Claude Code, Anthropic's official CLI for Claude.
User: What files are there?
Assistant: ToolCall(name="Bash", args={"command": "ls"})
User: ToolOutput(result="[README.md]")
Assistant: There is only one file named README.md.
User: Create a hello world function in Python.
Assistant: ToolCall(name="Write", args={"file_path": "hello_world.py", "content": "def hello_world():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    hello_world()"})
User: ToolOutput(result="Created `hello_world.py` with a simple hello world function.")
Assistant: I've created a simple Python file with a "Hello, World!" function.
```

**上下文窗口演进数据**：GPT-3 早期 2048 token → Claude Sonnet 4.5 百万 token，增长约 500 倍，但上下文过载问题依然存在。

**官方 Skill 参考实现**：`https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md`

---

### 📝 避坑指南

- ⚠️ **Metadata 描述不清会导致 Agent 不知道何时调用 Skill**：系统提示词中的 Skill 描述必须精准反映其适用场景，否则 Agent 不会主动触发 `Read`。
- ⚠️ **上下文过载不只是"超出窗口"**：即使未超出 token 上限，过多无关内容也会导致 Lost in the Middle、Context Poisoning、Context Confusion，三层加载的意义正在于此。
- ⚠️ **Skills 不等于 RAG**：Skills 不依赖向量检索，而是依赖 LLM 对路径描述的语义理解来决定是否读取，适合结构化、有明确边界的专业知识，不适合海量非结构化文档。
- ⚠️ **代码执行必须在 VM 沙盒中进行**：Skill 中的代码片段或 Agent 动态生成的代码，若直接在宿主机执行存在安全风险，必须通过虚拟机隔离。
- ⚠️ **`think` 工具与 Skills 的区别**：`think` 工具用于处理"刚发现的新信息"的聚焦推理，是 Context Offloading 的另一种形式，但不涉及文件系统，两者互补而非替代。

---

### 🏷️ 行业标签

#AgentSkills #ReAct #ContextOffloading #ClaudeCode #LLM上下文管理 #三层加载 #Function Calling #沙盒安全

---

**参考链接（原样保留）**：
- `https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills`
- `https://arxiv.org/abs/2210.03629`
- `https://platform.openai.com/docs/guides/function-calling`
- `https://russellluo.com/2025/09/demystifying-claude-code-agentic-coding`
- `https://arxiv.org/abs/2307.03172`
- `https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html`
- `https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html`
- `https://www.anthropic.com/engineering/claude-think-tool`
- `https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md`
- `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`

---

---
