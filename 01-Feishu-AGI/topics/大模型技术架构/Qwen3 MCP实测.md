# 大模型技术架构

## 39. [2026-05-05]

## 📘 文章 3


> 文档 ID: `MKT8wy6tMiWNjDkzO2IcmZmPn1g`

**来源**: Qwen3 MCP实测 | **时间**: 2025-05-01 | **原文链接**: `https://mp.weixin.qq.com/s/0FwcPrKj...`

---

### 📋 核心分析

**战略价值**: Qwen3 原生支持 MCP 协议，通过微调阶段内置协议规范，配合 Qwen-Agent 框架实现开箱即用的稳定工具调用，解决了提示词强制适配方案的不确定性问题。

**核心逻辑**:

- **非原生 MCP 的根本缺陷**：传统方案靠系统提示词强制规范模型输出，一旦模型输出不合规范，工具调用直接失败，这是企业不敢上生产的核心原因。
- **原生支持的本质**：模型在微调阶段使用了 MCP 协议相关数据训练，模型天然知道协议规范，无需额外适配层或中间件，出错概率大幅降低。
- **Qwen3 发布时间**：2025年4月29日凌晨，阿里开源。
- **模型矩阵**：2个MoE模型（Qwen3-235B-A22B、Qwen3-32B）+ 6个Dense模型（30B-A3B、14B、8B、4B、1.7B、0.6B），覆盖从边缘到云端全场景。
- **双模式融合**：单模型同时具备推理模式（原QwQ，适合数学/代码/逻辑）和非推理模式（原instruct，适合通用对话），通过 `enable_thinking` 参数切换。
- **Agent 能力**：在两种模式下均达到业界领先，工具调用精准，配合 Qwen-Agent 框架封装了工具调用模板和解析器。
- **MCP 本质**：MCP 是 Function Call 的一种特殊形式，Agent 框架内部处理流程与 Function Call 完全一致（判断→调用→返回→综合回答）。
- **Qwen-Agent 集成方式**：通过 `mcpServers` 字段直接在 `function_list` 中声明 MCP Server URL，支持 SSE 协议连接远程 MCP Server。
- **流式限制**：Qwen3 只支持流式返回，调用时必须用 `for responses in bot.run(...)` 遍历，取最后一次结果。
- **responses 结构**：一次完整调用返回 5 条结果，依次对应：用户提问→判断工具→function_call+参数→工具返回→最终回答。

---

### 🛠️ 操作流程

**1. 准备阶段：创建工程**

```bash
# 用 uv 创建 Python 3.12 工程
uv init qwen3-mcp-test -p 3.12
cd qwen3-mcp-test

# 创建虚拟环境
uv venv

# 安装依赖（含 MCP、RAG、GUI、代码解释器）
uv add qwen-agent[code-interpreter,gui,mcp,rag]
```

**2. 配置阶段：创建 `.env` 文件**

```env
API_KEY=你的密钥
BASE_URL=你的模型服务地址
MODEL=qwen3-xxx
```

**3. 核心执行：测试代码**

```python
from qwen_agent.agents import Assistant
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

# 配置 LLM
llm_cfg = {
    'model': MODEL,
    'model_server': BASE_URL,
    'api_key': API_KEY,
    'enable_thinking': False  # False=非推理模式，True=推理模式
}

# 配置工具：MCP Server（SSE协议）+ 内置工具
tools = [
    {
        "mcpServers": {
            "time-sse": {
                "url": "https://time.mcp.minglog.cn/sse",  # 替换为你自己的 MCP Server URL
                "name": "time-sse"
            }
        }
    },
    'code_interpreter'  # 内置工具
]

# 初始化 Agent
bot = Assistant(llm=llm_cfg, function_list=tools)

# 发起对话（必须流式遍历）
messages = [{'role': 'user', 'content': '现在几点了？'}]
for responses in bot.run(messages=messages):
    ...  # Qwen3 只支持流式，取最后一次

print(responses)
```

**4. 验证阶段：理解 responses 结构**

完整调用链路返回 5 条结果，顺序如下：

| 序号 | 内容 | 说明 |
|------|------|------|
| 1 | 用户提问 | 原始 user message |
| 2 | 工具判断 | 模型决定是否调用工具 |
| 3 | function_call + 参数 | 携带工具名称和入参 |
| 4 | 工具返回结果 | MCP Server 执行后的输出 |
| 5 | 最终回答 | 模型综合工具结果给用户的答复 |

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 推理模式切换 | `enable_thinking: True/False` | True=深度推理，False=快速对话 | 生产中通用对话建议关闭，节省 token |
| MCP Server 声明 | `mcpServers` 字段嵌入 `function_list` | 直接连接远程 MCP Server | URL 必须是 SSE 协议端点（`/sse` 结尾） |
| 流式返回处理 | `for responses in bot.run(...)` | 获取完整调用链路 | 不能用同步方式调用，否则拿不到结果 |
| 内置工具 | `'code_interpreter'` 字符串直接加入列表 | 代码执行能力 | 与 MCP 工具可以混用 |
| 环境变量 | `.env` 文件 + `python-dotenv` | 密钥安全隔离 | 不要把密钥硬编码进代码 |

---

### 📝 避坑指南

- ⚠️ **流式强制要求**：Qwen3 只支持流式返回，必须用 `for responses in bot.run(messages=messages)` 遍历，直接调用无法获取结果。
- ⚠️ **MCP Server URL 格式**：必须是 SSE 协议端点，通常以 `/sse` 结尾，普通 HTTP 接口不能直接用。
- ⚠️ **非原生模型的隐患**：如果换用非原生支持 MCP 的模型，需要在系统提示词中强制规范输出，存在调用失败的不确定性，不建议生产使用。
- ⚠️ **responses 取值**：遍历结束后 `responses` 变量保存的是最后一次迭代值（即最终回答），中间过程需要在循环内打印调试。

---

### 🏷️ 行业标签

#Qwen3 #MCP协议 #原生工具调用 #Qwen-Agent #FunctionCall #Agent开发 #开源大模型 #阿里云

---

---
