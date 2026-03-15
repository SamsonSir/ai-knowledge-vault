# 大模型技术架构

## 10. [2026-01-26]

## 📕 文章 1


> 文档 ID: `B5cjw6Zxbi1tKfk6RUYcuOt5nHh`

**来源**: Qwen3-Max-Thinking：会想能干，比强更强 | **时间**: 2026-01-26 | **原文链接**: `https://mp.weixin.qq.com/s/tWpStpBN...`

---

### 📋 核心分析

**战略价值**: Qwen3-Max-Thinking 是阿里千问最新旗舰推理模型，通过自适应工具调用 + 测试时扩展两项核心创新，在19项基准上对齐 GPT-5.2-Thinking / Claude-Opus-4.5 / Gemini 3 Pro，并已开放 API 可直接替换 OpenAI / Anthropic 调用。

**核心逻辑**:

- **参数规模 + RL 算力双加码**：通过大幅增加模型参数规模，并投入大量强化学习训练算力，覆盖事实知识、复杂推理、指令遵循、人类偏好对齐、智能体能力五个维度。
- **19项基准对齐顶尖模型**：性能可媲美 GPT-5.2-Thinking、Claude-Opus-4.5、Gemini 3 Pro，具体强项见下方表格。
- **自适应工具调用（无需手动选择）**：模型在对话中自主决定是否调用搜索引擎、记忆、代码解释器，不需要用户手动切换工具。
- **工具训练流程两阶段**：先做工具使用微调（SFT），再在多样化任务上用基于规则 + 模型的反馈做进一步强化训练。
- **搜索 + 记忆工具解决幻觉问题**：搜索工具提供实时信息，记忆工具支持个性化回复，两者共同缓解幻觉。
- **代码解释器支持计算推理**：用户可直接执行代码片段，解决需要精确计算的复杂问题。
- **测试时扩展策略：经验累积式多轮迭代**：不是简单增加并行推理路径数量（那样会导致冗余推理），而是限制并行路径，把省下的算力用于迭代式自我反思。
- **"经验提取"机制避免重复推导**：从过往推理轮次中提炼关键洞见，让模型跳过已知结论，专注于未解决的不确定性，上下文利用效率高于直接引用原始推理轨迹。
- **相同 token 消耗下持续优于并行采样聚合**：GPQA 90.3→92.8、HLE 34.1→36.5、LiveCodeBench v6 88.0→91.4、IMO-AnswerBench 89.5→91.5、HLE(w/ tools) 55.8→58.3。
- **API 双协议兼容**：同时兼容 OpenAI API 和 Anthropic API，可无缝替换现有调用代码，也可直接搭配 Claude Code 使用。

---

### 🎯 关键洞察

**为什么"经验累积式迭代"优于"并行采样"？**

- 原因：并行采样增加路径数量，但多条路径往往推导出相同中间结论，属于算力浪费；上下文窗口被重复信息占满，新信息密度下降。
- 动作：限制并行路径数，将节省的算力投入"经验提取"——每轮推理结束后提炼关键洞见压缩进上下文，下一轮直接从洞见出发继续推理。
- 结果：相同 token 预算内，历史信息融合更充分，模型聚焦于真正未解决的问题，推理质量持续提升（见上方5项基准数据）。

**为什么自适应工具调用是关键差异点？**

- 早期方案要求用户手动选择工具，认知负担高，且用户往往不知道何时该用哪个工具。
- Qwen3-Max-Thinking 通过专门训练流程让模型自主判断，用户只需正常对话，模型按需调用搜索/记忆/代码解释器，体验接近"无感知工具使用"。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 搜索工具 | 模型自动调用，无需参数 | 实时信息获取，缓解幻觉 | 已上线 Qwen Chat，API 侧需确认是否默认开启 |
| 记忆工具 | 模型自动调用 | 个性化回复，跨轮次记忆 | 同上 |
| 代码解释器 | 模型自动调用 | 执行代码片段，精确计算推理 | 同上 |
| OpenAI 兼容 API | `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"` | 直接替换 OpenAI 调用 | 国际用户用 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| 开启思考模式 | `extra_body={"enable_thinking": True}` | 激活推理链输出 | 必须显式传入，否则默认不开启 |
| Anthropic 兼容 API | `ANTHROPIC_BASE_URL=https://dashscope.aliyuncs.com/apps/anthropic` | 搭配 Claude Code 使用 | 需同时设置 `ANTHROPIC_MODEL` 和 `ANTHROPIC_SMALL_FAST_MODEL` |
| 测试时扩展 | 模型内置，无需用户配置 | 推理质量提升（见基准数据） | 自动生效，token 消耗与标准模式大致相同 |

---

### 🛠️ 操作流程

**方案一：Python 调用（OpenAI 兼容模式）**

1. **准备阶段**：注册阿里云账号 → 开通 Model Studio 服务 → 进入控制台创建 API 密钥 → 设置环境变量 `API_KEY`

2. **核心执行**：
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # 国际用户请使用 https://dashscope-intl.aliyuncs.com/compatible-mode/v1
)

completion = client.chat.completions.create(
    model="qwen3-max-2026-01-23",
    messages=[
      {'role': 'user', 'content': 'Give me a short introduction to large language model.'}
    ],
    extra_body={"enable_thinking": True}  # 开启推理链
)

print(completion.choices[0].message)
```

3. **验证**：检查返回的 `message` 中是否包含思考过程，确认 `enable_thinking` 生效。

---

**方案二：搭配 Claude Code（Anthropic 兼容模式）**

1. **准备阶段**：同上，获取 DashScope API Key

2. **核心执行**：
```bash
# 安装 claude-code
npm install -g @anthropic-ai/claude-code

# 配置环境变量
export ANTHROPIC_MODEL="qwen3-max-2026-01-23"
export ANTHROPIC_SMALL_FAST_MODEL="qwen3-max-2026-01-23"
export ANTHROPIC_BASE_URL=https://dashscope.aliyuncs.com/apps/anthropic
export ANTHROPIC_AUTH_TOKEN=your-dashscope-apikey

# 启动
claude
```

3. **验证**：Claude Code 界面正常启动，模型响应来自 Qwen3-Max-Thinking。

---

### 💡 具体案例/数据

测试时扩展（经验累积式迭代 vs 标准并行采样）对比：

| 基准 | 标准并行采样 | 经验累积式迭代 | 提升 |
|------|------------|--------------|------|
| GPQA | 90.3 | 92.8 | +2.5 |
| HLE | 34.1 | 36.5 | +2.4 |
| LiveCodeBench v6 | 88.0 | 91.4 | +3.4 |
| IMO-AnswerBench | 89.5 | 91.5 | +2.0 |
| HLE (w/ tools) | 55.8 | 58.3 | +2.5 |

体验入口：
- Qwen Chat：`chat.qwen.ai`
- 阿里云百炼：`https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/detail/qwen3-max-2026-01-23`

---

### 📝 避坑指南

- ⚠️ **`enable_thinking` 必须显式传入**：调用 API 时若不在 `extra_body` 中传 `{"enable_thinking": True}`，推理链不会激活，退化为普通对话模式。
- ⚠️ **国内/国际 base_url 不同**：国内用 `dashscope.aliyuncs.com`，国际用 `dashscope-intl.aliyuncs.com`，混用会导致请求失败。
- ⚠️ **Claude Code 需同时设置两个模型变量**：`ANTHROPIC_MODEL` 和 `ANTHROPIC_SMALL_FAST_MODEL` 都要指向 `qwen3-max-2026-01-23`，漏设其中一个会导致部分请求走默认 Claude 端点报错。
- ⚠️ **模型名称带日期版本号**：正确名称为 `qwen3-max-2026-01-23`，不要用 `qwen3-max` 等不带版本号的别名，可能指向旧版本。

---

### 🏷️ 行业标签

#Qwen3 #推理模型 #测试时扩展 #自适应工具调用 #OpenAI兼容API #Anthropic兼容API #ClaudeCode #阿里云 #大模型API

---

---
