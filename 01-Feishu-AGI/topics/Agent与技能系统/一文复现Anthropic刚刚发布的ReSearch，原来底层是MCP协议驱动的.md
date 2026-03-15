# Agent与技能系统

## 129. [2026-04-23]

## 📙 文章 4


> 文档 ID: `ODeewxeWKiYratkC7xicbWkmn8c`

**来源**: 一文复现Anthropic刚刚发布的ReSearch，原来底层是MCP协议驱动的 | **时间**: 2025-04-16 | **原文链接**: `https://mp.weixin.qq.com/s/Jenytho4...`

---

### 📋 核心分析

**战略价值**: Claude Research 本质是 MCP 协议驱动的多轮 Agent 工具调用链，可用 Dify + Zapier 完整复现其「搜索+工作区读写」能力。

**核心逻辑**:

- **Research 的运作机制**：Claude 以 Agent 方式执行多轮相互依赖的搜索，每轮动态决定下一步调查方向，而非一次性检索，本质是 ReAct 循环。
- **Google Workspace 集成原理**：Claude 通过 MCP 协议将 Gmail、Google Calendar、Google Drive 注册为工具，实现读取邮件、查看日程、检索文档，无需用户手动上传文件。
- **Google 文档编目（Cataloging）**：企业版专属，底层是 RAG（检索增强生成），为组织文档建立专用索引，支持跨文件、跨长文档的语义检索，无需指定具体文件名。
- **MCP 协议是底层驱动**：Dify 复现实验证明，Claude Research 的工具调用结构与 MCP 协议的 tool_call 格式完全一致，工具名称、入参均由大模型动态决定。
- **三轮执行逻辑**：round1 查当前时间（时间插件）→ round2 并行调用 Gmail/Calendar/Drive 三个工具 → round3 综合所有工具返回结果生成最终回复。
- **工具入参由 LLM 自主生成**：模型自行决定调用哪些工具、每个工具传什么参数，无硬编码路由逻辑。
- **Zapier 作为 MCP Server**：在 Zapier 中逐一添加 Gmail、Calendar、Drive 的 Action，暴露为 MCP 服务地址，供 Dify Agent 调用。
- **Dify 作为 MCP Client**：在 Dify 工作流中选用「MCP Agent 策略」，填入 Zapier 暴露的 MCP 服务地址，配置模型和工具（含一个海外搜索 API）。
- **Research 功能当前使用门槛**：Beta 阶段仅限美国、日本、巴西；套餐要求 Max/Team/Enterprise；用户需在聊天界面手动切换「Research」开关。
- **企业级安全保障**：编目功能在提供跨文档检索的同时，确保数据不出组织边界，维护知识机密性。

---

### 🎯 关键洞察

**MCP 协议正在成为 Claude 产品的基础设施层**。从 Dify 复现实验的 tool_call 结构可以直接看出，Claude Research 的工具调用 JSON 格式与标准 MCP 协议完全对齐：

```json
{
  "tool_call_id": "call_0_e7378500-091b-4e93-b548-4bc9408b99b2",
  "tool_call_input": { "query": "out of office" },
  "tool_call_name": "gmail_find_email",
  "tool_response": "[{'type': 'text', 'text': '[{\"_zap_search_was_found_status\": false}]'}]"
}
```

这意味着任何支持 MCP 协议的工具，理论上都可以被 Claude Research 调用，产品边界由 MCP Server 的覆盖范围决定，而非 Claude 本身的硬编码集成。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Zapier Gmail Action | 在 Zapier 中手动添加 `gmail_find_email` Action | 支持按 query 检索邮件 | 每个 Action 需单独手动添加，不能批量导入 |
| Zapier Calendar Action | 添加 `google_calendar_find_multiple_` Action，参数 `calendarid: "primary"` | 检索主日历事件 | calendarid 默认填 primary |
| Zapier Drive Action | 添加 `google_drive_find_a_file` Action，参数 `title: "..."` | 按文件名检索云盘文件 | 云盘为空时返回空结果，不报错 |
| Dify Agent 策略 | 选择「MCP Agent 策略」，填入 Zapier MCP 服务地址 | Dify 作为 MCP Client 调用 Zapier 工具 | 需要额外配置一个海外搜索 API（需自行注册获取 API Key）|
| 海外搜索工具 | 在 Dify Agent 工具列表中添加，填入 API Key | 支持联网搜索 | 需自行注册，具体服务商文中未指定 |
| MCP 服务地址 | Zapier 生成的 MCP endpoint URL | 统一入口供 Dify 调用所有 Workspace 工具 | 地址需在 Dify Agent 配置页填入 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 注册 Zapier 账号，连接 Google 账号（Gmail + Calendar + Drive 授权）
- 注册一个海外搜索服务，获取 API Key（用于 Dify 联网搜索工具）
- 准备 Dify 实例（本地部署或云端均可）

**2. Zapier 配置（MCP Server 搭建）**

- 进入 Zapier，逐一手动添加以下三个 Action：
  - `gmail_find_email`（Gmail 邮件检索）
  - `google_calendar_find_multiple_`（Google 日历多事件检索）
  - `google_drive_find_a_file`（Google Drive 文件检索）
- 获取 Zapier 生成的 MCP 服务地址（endpoint URL）

**3. Dify 工作流配置（MCP Client 搭建）**

- 在 Dify 中新建工作流，添加 Agent 节点
- Agent 节点配置：
  - Agent 策略：选择「MCP Agent 策略」
  - 模型：选择支持工具调用的模型（文中使用 Claude）
  - 工具：添加海外搜索工具（填入 API Key）
  - MCP 服务地址：填入 Zapier 生成的 endpoint URL
- 工作流结构保持简单：输入节点 → Agent 节点 → 输出节点

**4. 测试执行**

- 使用官方测试 Prompt：
  ```
  Hey, I'm planning to take a 3-month sabbatical to hike the Appalachian Trail on May 1. 
  Draft an out of office plan using info from my email, calendar, and docs. 
  Can you please also search for spots where I'll have good service to check in with my colleagues?
  ```
- 或使用自定义 Prompt（发邮件示例）：
  ```
  我是[姓名]，帮我向[邮箱地址]发一个主题为claude+research的邮件，
  介绍https://www.anthropic.com/news/research的信息
  ```
- 在 Dify 工作流中运行，观察 Agent 策略面板中的多轮执行日志

**5. 验证执行逻辑**

观察三轮 round 的执行情况：
- round1：调用时间插件，获取当前时间
- round2：并行调用 `gmail_find_email`、`google_calendar_find_multiple_`、`google_drive_find_a_file`，入参由模型自主生成
- round3：综合三个工具的返回结果，生成最终回复

---

### 💡 具体案例/数据

**round2 实际调用的 tool_input JSON**（由大模型自主生成）：
```json
{
  "output": "",
  "tool_input": {
    "gmail_find_email": {
      "query": "out of office"
    },
    "google_calendar_find_multiple_": {
      "calendarid": "primary"
    },
    "google_drive_find_a_file": {
      "title": "out of office"
    }
  },
  "tool_name": "gmail_find_email;google_calendar_find_multiple_;google_drive_find_a_file"
}
```

**单个工具调用返回结构**：
```json
{
  "output": {
    "tool_call_id": "call_0_e7378500-091b-4e93-b548-4bc9408b99b2",
    "tool_call_input": {
      "query": "out of office"
    },
    "tool_call_name": "gmail_find_email",
    "tool_response": "[{'type': 'text', 'text': '[{\"_zap_search_was_found_status\": false}]'}]"
  }
}
```

`_zap_search_was_found_status: false` 表示 Gmail 中未找到匹配邮件，属于正常空结果返回，不影响后续 round3 的综合回复。

---

### 📝 避坑指南

- ⚠️ Zapier Action 必须逐一手动添加，没有批量导入方式，三个工具（Gmail/Calendar/Drive）需分别操作
- ⚠️ Google Drive 和 Google Calendar 为空时，工具返回空结果而非报错，模型会在 round3 中说明「未找到相关信息」，这是正常行为
- ⚠️ 海外搜索工具需自行注册第三方服务获取 API Key，文中未指定具体服务商，需自行选择（如 Tavily、Serper 等）
- ⚠️ Research Beta 功能目前仅限美国、日本、巴西地区，且需要 Max/Team/Enterprise 套餐，普通 Pro 用户暂不可用
- ⚠️ Google Workspace 集成的 Beta 版对 Team/Enterprise 用户，管理员需先在全公司范围内启用，个人用户才能在个人资料设置中看到入口
- ⚠️ MCP 服务地址填写错误会导致 Agent 无法发现工具，需确认 Zapier 生成的 endpoint URL 格式正确

---

### 🏷️ 行业标签

#MCP协议 #Claude #Research #Dify #Zapier #GoogleWorkspace #Agent #RAG #工作流自动化 #企业AI

---

---
