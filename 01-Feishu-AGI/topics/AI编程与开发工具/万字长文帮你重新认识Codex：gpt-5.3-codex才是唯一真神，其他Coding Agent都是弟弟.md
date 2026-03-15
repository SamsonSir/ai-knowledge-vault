# AI编程与开发工具

## 33. [2026-02-21]

## 📗 文章 2


> 文档 ID: `EvItwlooTiJ8g4kcaZTcpMscnWd`

**来源**: 万字长文帮你重新认识Codex：gpt-5.3-codex才是唯一真神，其他Coding Agent都是弟弟 | **时间**: 2026-02-21 | **原文链接**: `https://mp.weixin.qq.com/s/cCMCpUnY...`

---

### 📋 核心分析

**战略价值**: gpt-5.3-codex 通过模型与框架协同训练实现"一击必杀"，彻底改变 Vibe Coding 工作流——用 10 分钟换来零返工的生产级代码。

**核心逻辑**:

- **模型与框架 Native 共训**：gpt-5.3-codex 不是"通用模型+代码微调"，而是与 Codex 框架一同训练，模型理解框架内部机制，框架理解模型输出模式，结果是更少误解、更准确输出、更少迭代。
- **一击必杀的代价是时间**：每个任务 10 分钟起步，复杂任务几小时，但换来的是几乎零屎山风险，其他所有模型（含 Opus）需要多次迭代才能搞定的问题，gpt-5.3-codex（推理强度=high）全部一次搞定。
- **三层架构协同**：模型层（gpt-5.3-codex 提供智能）+ 框架层（Harness 用 compaction 技术管理上下文窗口，真正执行文件操作/命令/测试）+ 界面层（App/CLI/IDE/Mini 四种 Surface）。
- **四种 Surface 各司其职**：Codex App（macOS 并行主力）、CLI（全平台最完整功能）、IDE 扩展（编辑器内无缝集成）、Cloud（后台云端执行，可关机）。
- **Worktree 隔离是并行开发的核心**：每个任务独立 Git worktree，互不干扰，4天或超过10个时自动清理，支持 Overwrite（完全覆盖）和 Apply（补丁方式保留历史）两种同步策略。
- **配置系统六层优先级**：CLI 标志 > Profile > 项目 .codex/config.toml > 用户 ~/.codex/config.toml > 系统 /etc/codex/config.toml > 内置默认值，支持 TOML 格式全量覆盖。
- **推理强度是质量的关键旋钮**：minimal/low/medium/high/xhigh 五档，复杂架构设计用 xhigh，简单任务用 low，直接影响 token 消耗和输出质量。
- **AGENTS.md 是项目级上下文注入**：放在项目根目录，Codex 每次会话自动读取，相当于给模型注入项目架构、编码规范、测试命令等持久化上下文。
- **Automations 实现无人值守**：将 Skills 与定时任务结合，App 保持运行即可后台执行代码审查、文档更新、Bug 修复、自我改进等任务，Git 项目每次运行在新 worktree 中。
- **MCP 扩展第三方能力**：通过 config.toml 配置 Context7（文档搜索）、Figma（设计稿）、Playwright（浏览器自动化）、GitHub、Sentry 等服务器，一行配置接入。

---

### 🎯 关键洞察

**为什么 Native 训练是决定性优势**：

Gabriel Chua 的核心观点："The model and the harness aren't separate pieces assembled later — they're co-designed."（模型和框架不是后来拼凑的，而是一起设计的）。

其他 Coding Agent 的本质是"通用模型 + 工具调用层"，模型不理解工具的内部状态，工具也不理解模型的推理模式，导致大量"翻译损耗"。Codex 的 compaction 技术（上下文窗口压缩管理）是框架层的核心，模型天然理解何时压缩、压缩什么，这是外部 Agent 无法复制的。

**推理时间换质量的心理模型转变**：

传统 Vibe Coding 心态：快速迭代 → 频繁返工 → 累积屎山。
Codex 心态：一次深度思考 → 一次性生产级输出 → 零返工。适应这个节奏后，你的工作流从"监视 Agent 防止出错"变成"提交任务去做别的事"。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 默认模型 | `model = "gpt-5.3-codex"` | 最强编程能力 | 每任务10分钟起步 |
| 推理强度 | `model_reasoning_effort = "high"` | 一击必杀 | xhigh 消耗 token 极多 |
| 推理摘要 | `model_reasoning_summary = "detailed"` | 可见推理过程 | auto/concise/detailed/none |
| 上下文压缩 | `model_auto_compact_token_limit = 32000` | 自动管理上下文 | 超过阈值自动压缩 |
| 审批策略 | `approval_policy = "on-request"` | 外部/网络操作需确认 | never=全自动，谨慎使用 |
| 沙盒模式 | `sandbox_mode = "workspace-write"` | 可写工作区，限制其他 | read-only最安全 |
| 网页搜索 | `web_search = "cached"` | 使用缓存结果 | live=实时但需更多权限 |
| 多智能体 | `[features] multi_agent = true` | 并行多 Agent 协作 | 实验性功能 |
| Worktree 自动清理 | 4天或超过10个 | 自动释放空间 | 未提交的更改会丢失 |
| 历史记录 | `max_bytes = 104857600` | 保留100MB历史 | persistence = "none" 关闭 |

---

### 🛠️ 操作流程

#### Codex App 安装与配置

1. **安装**: 下载 `https://persistent.oaistatic.com/codex-app-prod/Codex.dmg`，用 ChatGPT 账号或 OpenAI API Key 登录
2. **选择模式**: Local（快速原型）/ Worktree（推荐，隔离开发）/ Cloud（后台执行）
3. **项目级配置**: 在项目根目录创建 `.codex/config.toml`

```toml
model = "gpt-5.3-codex"
model_reasoning_effort = "high"
approval_policy = "on-request"
developer_instructions = """
这是一个 Python 项目，使用 FastAPI 框架。
请始终使用 async/await 模式。
测试使用 pytest。
"""
```

4. **Local Environments 配置**: 创建 `.codex/local-env.toml`

```toml
[setup]
commands = ["npm install", "npm run build"]

[setup.macos]
commands = ["brew install ffmpeg"]

[setup.linux]
commands = ["apt-get install ffmpeg"]

[actions]
run = "npm start"
test = "npm test"
lint = "npm run lint"

[actions.deploy]
command = "npm run deploy"
icon = "rocket"
```

5. **AGENTS.md 注入项目上下文**: 项目根目录创建

```markdown
# 项目说明
## 架构
- 使用 Clean Architecture
- 领域层在 src/domain/
- 应用层在 src/application/

## 编码规范
- 所有函数必须有类型注解
- 使用 black 格式化
- 提交前运行 pre-commit

## 测试
- 单元测试：pytest tests/unit/
- 集成测试：pytest tests/integration/
```

#### CLI 安装与使用

1. **安装**:

```bash
npm install -g @openai/codex
codex login
# 或
codex login --with-api-key
```

2. **常用命令**:

```bash
# 交互模式
codex
codex "帮我重构这个函数"
codex --full-auto "修复所有 bug"

# 指定模型和推理强度
codex --model gpt-5.3-codex --config model_reasoning_effort=high "复杂架构设计"

# 图片输入
codex -i screenshot.png "把这个 UI 实现出来"
codex --image design1.png,design2.png "对比这两个设计"

# 非交互脚本化
codex exec --json "分析这个文件" > result.json
codex exec --output-last-message result.txt "生成报告"
codex exec --ephemeral "临时任务"

# 会话管理
codex resume --last
codex resume <SESSION_ID>
codex fork --last

# 代码审查
/review
/review against main
/review uncommitted

# MCP 管理
codex mcp add context7 -- npx -y @upstash/context7-mcp
codex mcp list
codex mcp remove context7

# 功能标志
codex features enable multi_agent
codex features list
```

#### Cloud 模式配置

1. 访问 `https://chatgpt.com/codex`
2. 连接 GitHub 账号，授权仓库访问
3. 在 Issue/PR 评论中 `@codex 修复这个 bug` 触发自动 PR

```toml
# Cloud 环境配置
dependencies = ["python", "nodejs", "docker"]
setup_commands = [
    "pip install -r requirements.txt",
    "npm install"
]
```

#### 完整配置文件示例

```toml
#:schema https://developers.openai.com/codex/config-schema.json

model = "gpt-5.3-codex"
model_reasoning_effort = "high"
model_verbosity = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"

[features]
multi_agent = false
shell_tool = true

[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.playwright]
command = "npx"
args = ["-y", "@executeautomation/playwright-mcp-server"]

[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"

[tui]
notifications = true
animations = true

[history]
persistence = "save-all"
max_bytes = 104857600

[profiles.fast]
model = "gpt-5-codex"
model_reasoning_effort = "low"

[profiles.deep]
model = "gpt-5.3-codex"
model_reasoning_effort = "xhigh"
approval_policy = "on-request"

[agents]
max_threads = 4
```

---

### 💡 具体案例/数据

**提示词公式实战**：

```
【目标】写一个批量处理 Excel 文件的工具
【技术栈】Python + pandas + openpyxl
【输入】./input 目录下的所有 .xlsx 文件
【输出】汇总到 summary.xlsx，生成 report.txt
【约束】
  - 只读取每个文件的 B 列
  - 跳过空文件并记录日志
  - 处理大文件时分块读取
【质量要求】
  - 添加类型注解
  - 每个函数有文档字符串
  - 异常处理要具体
```

**迭代式提问（FastAPI 认证接口）**：

- 第一轮：`写一个 FastAPI 用户认证接口`
- 第二轮：`加上 JWT token 生成和验证，用 HS256 算法`
- 第三轮：`再添加 refresh token 机制，access token 15 分钟过期，refresh token 7 天`
- 第四轮：`登录接口需要速率限制，每分钟最多 10 次请求`

**调试提示词模板**：

```
代码运行报错：

```
Traceback (most recent call last):
  File "main.py", line 42, in <module>
    result = process_data(data)
  File "main.py", line 28, in process_data
    return data.groupby('category').sum()
ValueError: No numeric types to aggregate
```

数据文件格式：
```csv
id,category,value
1,A,100
2,B,200
```

帮我分析问题原因并修复
```

**Automations 典型用例**：

1. 代码审查自动化：每次提交后自动运行 `/review`
2. 文档更新：监控代码变更，自动更新 API 文档
3. Bug 修复：从遥测数据中检测错误并提交修复
4. 自我改进：扫描会话文件，基于问题更新 skills

**管理员安全策略（requirements.toml）**：

```toml
allowed_approval_policies = ["on-request", "never"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["disabled", "cached"]

[mcp_servers.allowed]
context7 = { identity = { command = "npx -y @upstash/context7-mcp" } }

[rules]
prefix_rules = [
    {
        pattern = [{ token = "rm" }, { token = "-rf" }],
        decision = "forbidden",
        justification = "禁止强制删除文件"
    }
]
```

---

### 📦 形态选择速查

| 场景 | 推荐组合 |
|------|---------|
| 主力开发 | App（主力）+ IDE 扩展（快速编辑） |
| 团队协作 | Cloud（后台任务）+ App（代码审查） |
| CI/CD 集成 | CLI（自动化脚本）+ Cloud（并行测试） |
| 快速原型 | IDE 扩展（实时迭代） |
| 大型重构 | App（Worktree 隔离）+ Cloud（长时间运行） |

| 形态 | 平台 | 核心优势 |
|------|------|---------|
| Codex App | macOS (Apple Silicon) | 并行多任务、Worktree、自动化 |
| CLI | macOS/Linux/Windows | 功能最完整、开源、可编程 |
| IDE 扩展 | VS Code/Cursor/Windsurf/JetBrains | 编辑器内直接交互、上下文感知 |
| Cloud | Web | 云端执行、不占本地资源、自动 PR |

**IDE 扩展快捷键**：

| 快捷键 | 功能 |
|--------|------|
| `Cmd+Shift+A` | 打开 Codex 面板 |
| `Cmd+Enter` | 发送消息 |
| `Shift+Enter` | 换行 |
| `@` | 引用文件 |

**Codex App 快捷键**：

| 快捷键 | 功能 |
|--------|------|
| `Cmd+J` | 切换终端 |
| `Cmd+数字` | 切换项目 |
| `Ctrl+M` | 语音输入 |
| `Cmd+Shift+N` | 新建线程 |

---

### 📝 避坑指南

- ⚠️ **不要把 gpt-5.3-codex 塞进 Claude Code**：模型和 Codex 框架是 Native 共训的，脱离 Codex 框架使用会损失核心能力，应配合 Codex App/CLI/IDE 扩展使用。
- ⚠️ **approval_policy = "never" 要谨慎**：全自动模式下 Codex 会直接执行所有操作，建议生产环境保持 `on-request`。
- ⚠️ **Worktree 未提交更改会丢失**：4天或超过10个 worktree 时自动清理，重要工作及时 `Create branch here` 转为正式分支。
- ⚠️ **Codex 写的代码仍需 review**：一击必杀不等于零错误，它是工具不是魔法，生产上线前必须人工审查。
- ⚠️ **Cloud 模式需要 GitHub 授权**：Cloud 任务通过 GitHub 访问本地文件，需提前在 `https://chatgpt.com/codex` 完成授权。
- ⚠️ **多 Agent 是实验性功能**：`multi_agent = true` 目前不稳定，生产环境谨慎启用。
- ⚠️ **xhigh 推理强度 token 消耗极大**：日常开发用 high，只在最复杂的架构设计任务才用 xhigh。
- ⚠️ **Automations 需要 App 保持运行**：自动化任务在本地执行，关闭 App 则停止，长时间任务改用 Cloud 模式。

---

### 🏷️ 行业标签

#Codex #VibeCoding #gpt-5.3-codex #CodingAgent #OpenAI #提示词工程 #GitWorktree #MCP #AI编程

---

---
