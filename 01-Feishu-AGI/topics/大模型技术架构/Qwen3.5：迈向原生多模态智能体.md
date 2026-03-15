# 大模型技术架构

## 19. [2026-02-16]

## 📕 文章 1


> 文档 ID: `TPopwaEnWi68EvkhmDhc892Cn9d`

**来源**: Qwen3.5：迈向原生多模态智能体 | **时间**: 2026-02-16 | **原文链接**: `https://mp.weixin.qq.com/s/AAanKh5u...`

---

### 📋 核心分析

**战略价值**: Qwen3.5-397B-A17B 以混合稀疏架构实现「原生多模态 + 高效推理 + 原生 Agent」三合一，在参数激活量仅 17B 的前提下对标 1T+ 参数的 Qwen3-Max-Base，是当前开放权重多模态 Agent 基座的最强竞争者。

**核心逻辑**:

- **架构创新**：采用 Gated Delta Networks（线性注意力）+ Gated Attention 混合注意力 + 稀疏 MoE，总参数 397B，每次前向传播仅激活 17B，实现高能力低激活的极致效率比。
- **吞吐量飞跃**：在 32k 上下文下解码吞吐是 Qwen3-Max 的 8.6 倍，256k 上下文下是 19.0 倍；相比 Qwen3-235B-A22B 分别为 3.5 倍/7.2 倍——长上下文场景收益尤为显著。
- **预训练能力对齐**：Qwen3.5-397B-A17B（397B 总参/17B 激活）与参数量超过 1T 的 Qwen3-Max-Base 性能相当，证明稀疏架构的参数效率已达到跨代对齐。
- **原生多模态**：通过早期文本-视觉融合（early fusion）+ 扩展视觉/STEM/视频数据实现，而非后期拼接，在相近规模下优于 Qwen3-VL。上下文窗口扩展至 1M tokens，可直接处理长达 2 小时的视频。
- **多语言扩展**：语言/方言支持从 119 种扩展至 201 种；词表从 15 万扩展至 25 万，在多数语言上带来约 10–60% 的编码/解码效率提升。
- **Post-training 策略转变**：RL 训练重点从「针对特定指标优化」转向「RL 环境难度与可泛化性」，在 BFCL-V4、VITA-Bench、DeepPlanning、Tool-Decathlon、MCP-Mark 五个 Agent 基准的平均排名上随 RL Environment Scaling 持续提升。
- **FP8 原生训练流水线**：对激活、MoE 路由、GEMM 运算采用低精度，敏感层运行时自动回退 BF16，实现约 50% 激活显存降低 + 超过 10% 加速，稳定扩展至数万亿 token。
- **异步 RL 框架**：训推分离架构，支持全尺寸模型 + 文本/多模态/多轮场景；配合 FP8 训推、Rollout 路由回放、投机采样、多轮 Rollout 锁定，端到端加速 3×–5×，可扩展至百万级 Agent 脚手架与环境。
- **训练吞吐接近 100%**：通过视觉与语言组件解耦并行策略 + 稀疏激活跨模块计算重叠，在混合文本-图像-视频数据上相比纯文本基线达到近 100% 训练吞吐。

---

### 🎯 关键洞察

**为什么混合注意力架构是关键**：
传统 Dense Transformer 在长上下文下 KV Cache 显存随序列长度二次增长，而 Gated DeltaNet（线性注意力）将复杂度压至线性，配合稀疏 MoE 只激活 17B/397B 参数，使得 256k 上下文下吞吐是 Dense 模型的 19 倍——这不是调参优化，而是架构层面的根本性突破。

**为什么 RL Environment Scaling 比模型规模 Scaling 更重要**：
Qwen3.5 的 Post-training 性能提升主要来自 RL 环境的难度与可泛化性扩展，而非针对特定 benchmark 刷分。五个 Agent 基准（BFCL-V4、VITA-Bench、DeepPlanning、Tool-Decathlon、MCP-Mark）的平均排名随 RL 环境规模单调提升，说明「环境多样性」是 Agent 能力的核心驱动力，而非参数量。

**为什么 early fusion 原生多模态优于后期拼接**：
早期融合让视觉 token 与文本 token 在预训练阶段就共享同一表示空间，模型天然学会跨模态推理；后期拼接（如 LLaVA 式）视觉编码器与语言模型是独立优化的，跨模态对齐依赖有限的微调数据，泛化能力受限。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 推理模式 | `enable_thinking: True` | 开启链式思考（CoT），适合复杂推理 | 消耗额外 thinking token，延迟增加 |
| 联网搜索 + Code Interpreter | `enable_search: True` | 模型可实时搜索并执行代码 | 与 `enable_thinking` 可同时开启 |
| 快速模式 | `enable_thinking: False` + `enable_search: False` | 直接回答，不消耗 thinking token | 复杂推理任务准确率可能下降 |
| API Base URL（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 国内低延迟 | 需设置 `DASHSCOPE_API_KEY` |
| API Base URL（新加坡） | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | 东南亚/国际用户 | 同上 |
| API Base URL（美国弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | 北美用户 | 同上 |
| 模型名称 | `qwen3.5-plus` | 旗舰模型 Qwen3.5-Plus | 通过环境变量 `DASHSCOPE_MODEL` 覆盖 |
| 上下文窗口 | 1M tokens | 可处理长达 2 小时视频 | 长上下文下建议使用 256k 以上配置以充分发挥 19× 吞吐优势 |
| 词表大小 | 25 万（vs. 旧版 15 万） | 多数语言编解码效率提升 10–60% | 旧版 tokenizer 不兼容，需更新 |

---

### 🛠️ 操作流程

**1. 准备阶段**

设置环境变量：
```bash
export DASHSCOPE_API_KEY='your-api-key'
# 可选，默认北京节点
export DASHSCOPE_BASE_URL='https://dashscope.aliyuncs.com/compatible-mode/v1'
export DASHSCOPE_MODEL='qwen3.5-plus'
```

API Key 申请入口：`https://bailian.console.aliyun.com`

**2. 核心执行**

完整可运行代码：
```python
from openai import OpenAI
import os

api_key = os.environ.get("DASHSCOPE_API_KEY")
if not api_key:
    raise ValueError(
        "DASHSCOPE_API_KEY is required. "
        "Set it via: export DASHSCOPE_API_KEY='your-api-key'"
    )

client = OpenAI(
    api_key=api_key,
    base_url=os.environ.get(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
)

messages = [{"role": "user", "content": "Introduce Qwen3.5."}]

model = os.environ.get("DASHSCOPE_MODEL", "qwen3.5-plus")

completion = client.chat.completions.create(
    model=model,
    messages=messages,
    extra_body={
        "enable_thinking": True,   # 开启链式思考
        "enable_search": False     # 是否开启联网搜索
    },
    stream=True
)

reasoning_content = ""  # 完整推理链
answer_content = ""     # 完整回答
is_answering = False    # 是否已进入回答阶段

print("\n" + "=" * 20 + "Reasoning" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 收集推理内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 进入回答阶段
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "Answer" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

**3. 第三方工具集成**

可将百炼 API（OpenAI 兼容接口）直接接入以下工具，无需额外适配：
- Qwen Code
- Claude Code
- Cline
- OpenClaw
- OpenCode

配置方式：将上述工具的 API Base URL 替换为百炼节点地址，API Key 填入 `DASHSCOPE_API_KEY`，模型名填 `qwen3.5-plus`。

**4. Chat 界面直接体验**

访问 `https://chat.qwen.ai/`，选择三种模式：
- 「自动」：自适应思考 + 工具调用（搜索、代码解释器）
- 「思考」：强制深度 CoT，适合复杂推理
- 「快速」：直接回答，零 thinking token 消耗

---

### 💡 具体案例/数据

**Agent 能力基准（RL Environment Scaling 验证）**：
- 评估基准：BFCL-V4、VITA-Bench、DeepPlanning、Tool-Decathlon、MCP-Mark
- 结论：随 RL 环境规模扩大，五个基准平均排名单调提升，验证环境多样性驱动 Agent 泛化能力

**吞吐量对比数据**：

| 对比对象 | 32k 上下文吞吐倍数 | 256k 上下文吞吐倍数 |
|---------|-----------------|------------------|
| vs. Qwen3-Max | 8.6× | 19.0× |
| vs. Qwen3-235B-A22B | 3.5× | 7.2× |

**FP8 训练收益**：
- 激活显存降低：约 50%
- 训练速度提升：超过 10%
- 稳定扩展规模：数万亿 token

**异步 RL 框架端到端加速**：3×–5×

**视觉编程示例 Prompt**（可直接复用）：
```
Create a homepage of OpenQwen, a virtual assistant personal agent that can help 
with coding, office works, shopping and so on. Generate high-quality images as 
the website's resources, including an avatar and demos of its use cases.
```

**多语言编解码效率提升**：词表 15 万 → 25 万，多数语言提升 10–60%

---

### 📝 避坑指南

- ⚠️ `enable_thinking: True` 会产生额外 thinking token 消耗，实时性要求高的场景建议关闭或使用「快速」模式
- ⚠️ 旧版 Qwen tokenizer（15 万词表）与新版（25 万词表）不兼容，升级时需同步更新 tokenizer
- ⚠️ 流式输出中需同时处理 `reasoning_content` 和 `content` 两个字段，漏处理 `reasoning_content` 会导致推理链丢失
- ⚠️ 256k 以上长上下文场景才能充分发挥 19× 吞吐优势，短上下文场景收益相对有限（32k 下为 8.6×）
- ⚠️ 第三方工具（Cline/Claude Code 等）集成时，模型名必须填写 `qwen3.5-plus`，不能使用旧版模型名
- ⚠️ 训推分离的异步 RL 框架需严格控制样本陈旧性（staleness），否则会影响训练曲线稳定性

---

### 🏷️ 行业标签

#Qwen3.5 #原生多模态 #MoE稀疏架构 #GatedDeltaNet #线性注意力 #Agent #RL环境扩展 #FP8训练 #阿里云百炼 #开放权重 #视觉语言模型 #长上下文

---

---
