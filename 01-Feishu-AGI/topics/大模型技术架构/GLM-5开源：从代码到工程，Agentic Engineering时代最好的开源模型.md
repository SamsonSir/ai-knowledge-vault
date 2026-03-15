# 大模型技术架构

## 18. [2026-02-12]

## 📙 文章 4


> 文档 ID: `HUYJwZ8U6i4MZkk6Qk7cEvbGnif`

**来源**: GLM-5开源：从代码到工程，Agentic Engineering时代最好的开源模型 | **时间**: 2026-02-12 | **原文链接**: `https://mp.weixin.qq.com/s/MVo6DIcG...`

---

### 📋 核心分析

**战略价值**: GLM-5 是智谱首个面向 Agentic Engineering 时代的旗舰开源模型，Coding + Agent 双维度达到开源 SOTA，真实使用体感对齐 Claude Opus 4.5，MIT License 完全开放。

**核心逻辑**:

- **参数规模跃升**：基座从 355B（激活 32B）扩展至 744B（激活 40B），预训练数据从 23T 增至 28.5T，算力规模提升直接拉高通用智能基线。
- **全新 Slime 强化学习框架**：支持更大模型规模与更复杂 RL 任务，提出异步智能体强化学习算法，使模型能从长程交互中持续学习，充分激发预训练潜力。
- **首次集成 DeepSeek Sparse Attention**：稀疏注意力机制在维持长文本效果无损的前提下，大幅降低部署成本，提升 Token Efficiency。
- **Coding 基准 SOTA**：SWE-bench-Verified 得分 77.8、Terminal Bench 2.0 得分 56.2，均为开源第一，性能超过 Gemini 3 Pro。
- **内部 Claude Code 评估集**：GLM-5 在前端、后端、长程任务上平均超越 GLM-4.7 超过 20%，能以极少人工干预自主完成 Agentic 长程规划、后端重构、深度调试。
- **Agent 基准全面开源第一**：BrowseComp（联网检索与信息理解）、MCP-Atlas（工具调用与多步骤任务执行）、τ²-Bench（复杂多工具规划执行）三项均取开源最佳。
- **Vending Bench 2 经营能力验证**：模拟一年期自动售货机经营，GLM-5 最终账户余额达 4432 美元，接近 Claude Opus 4.5，验证长期规划与资源管理能力。
- **Artificial Analysis 全球排名**：全球第四、开源第一。
- **国产芯片全栈适配**：已完成华为昇腾、摩尔线程、寒武纪、昆仑芯、沐曦、燧原、海光七大国产算力平台的深度推理适配，通过底层算子优化实现高吞吐、低延迟稳定运行。
- **MIT License 完全开源**：Hugging Face 与 ModelScope 同步发布，无商业限制。

---

### 🎯 关键洞察

**从 Vibe Coding → Agentic Engineering 的范式转变**：

- Vibe Coding 阶段：模型只需"会写代码"，输出片段即可。
- Agentic Engineering 阶段：模型需要端到端完成大型任务——拆解需求、多智能体并发执行、跑命令、调试、预览、提交，全程闭环，极少人工干预。
- GLM-5 的定位是"系统架构师"而非"代码补全器"：不为 Demo 而生，为稳定交付生产结果而生。

**长程任务一致性是核心壁垒**：Vending Bench 2 的设计逻辑揭示了这一点——模型需要在模拟一年期内持续做决策、管理资源、处理多步骤依赖，这与真实工程项目的复杂度高度吻合。GLM-5 以 4432 美元余额接近 Opus 4.5，说明其长程目标一致性已达到可用级别。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/入口 | 预期效果 | 注意事项 |
|----------|-------------|---------|---------|
| 官方 API | `https://docs.bigmodel.cn/cn/guide/models/text/glm-5` | 直接调用 GLM-5 | BigModel 开放平台 |
| Z.ai API | `https://docs.z.ai/guides/llm/glm-5` | 海外开发者入口 | — |
| OpenClaw 接入 | `https://docs.bigmodel.cn/cn/coding-plan/tool/openclaw` | 快速开启 Agent 工作流 | 官方适配，简单几步完成配置 |
| AutoGLM-OpenClaw | `https://autoglm.zhipuai.cn/?channel=AutoGLM_OpenClaw&redeem_modal_open=1` | 云端 AI 助手接入飞书，长任务执行 | Pro/Max 用户限量赠送 |
| Z Code | `https://zcode.z.ai/cn` | 全流程编程，多智能体并发，支持手机远程指挥桌面 Agent | — |
| GLM in Excel | 侧边栏自然语言交互 | 数据处理与表格工作流深度赋能 | Beta 期仅 Max 用户可享套餐抵扣 |
| 在线体验 | `https://chat.z.ai` / `https://chatglm.cn` | 直接对话体验 | — |
| GitHub | `https://github.com/zai-org/GLM-5` | 源码 | MIT License |
| Hugging Face | `https://huggingface.co/zai-org/GLM-5` | 模型权重下载 | MIT License |
| ModelScope | `https://modelscope.cn/models/ZhipuAI/GLM-5` | 国内镜像下载 | — |
| Blog | `https://z.ai/blog/glm-5` | 技术细节 | — |

---

### 🛠️ 操作流程

1. **快速上手 API**
   - 注册 BigModel 开放平台 → 进入 `https://docs.bigmodel.cn/cn/guide/models/text/glm-5` → 获取 API Key → 在 Claude Code / OpenCode 等主流开发工具中配置 GLM Coding Plan。

2. **部署 OpenClaw Agent 工作流**
   - 进入 `https://docs.bigmodel.cn/cn/coding-plan/tool/openclaw` → 按文档完成 OpenClaw 与飞书机器人一体化配置（官方适配，从数小时缩短至几分钟）→ 获得 7×24 小时智能助手，支持搜索网站、定时整理资讯、发布推文、编程等。

3. **Z Code 全流程编程**
   - 进入 `https://zcode.z.ai/cn` → 输入需求描述 → 模型自动拆解任务 → 多智能体并发完成代码编写、命令执行、调试、预览、提交全流程 → 可选：手机端远程指挥桌面 Agent。

4. **本地部署（开源权重）**
   - 从 Hugging Face（`https://huggingface.co/zai-org/GLM-5`）或 ModelScope（`https://modelscope.cn/models/ZhipuAI/GLM-5`）下载权重 → 参考 GitHub（`https://github.com/zai-org/GLM-5`）部署文档 → 按目标硬件选择适配方案（已支持七大国产芯片平台）。

---

### 💡 具体案例/数据

| 基准测试 | GLM-5 得分 | 对比 |
|---------|-----------|------|
| SWE-bench-Verified | 77.8 | 开源 SOTA，超 Gemini 3 Pro |
| Terminal Bench 2.0 | 56.2 | 开源 SOTA |
| BrowseComp | 开源第一 | — |
| MCP-Atlas | 开源第一 | — |
| τ²-Bench | 开源第一 | — |
| Vending Bench 2 | 4432 美元（模拟一年期余额） | 接近 Claude Opus 4.5，开源第一 |
| Artificial Analysis 全球榜 | 全球第四 | 开源第一 |
| 内部 Claude Code 评估集 | 平均超 GLM-4.7 超 20% | 前端/后端/长程任务全面提升 |

**真实开发者案例**（来自 OpenRouter 匿名 Pony 上线后）：
- 横版解谜游戏（已开放下载）
- Agent 交互世界
- 论文版"抖音"（已提交商店审核）
- 案例库：`showcase.z.ai`

---

### 📝 避坑指南

- ⚠️ **GLM Coding Plan 曾因爆量启动限售**：GLM-5 上线初期可能同样面临访问限制，建议提前申请 API 配额或关注官方扩容公告。
- ⚠️ **Pro 用户支持有延迟**：GLM-5 上线时优先纳入 Max 套餐，Pro 用户需等待约 5 天后才能使用，规划项目时注意时间窗口。
- ⚠️ **GLM in Excel 仍为 Beta**：Beta 期间仅 Max 用户可享套餐抵扣，功能稳定性待验证，生产环境谨慎依赖。
- ⚠️ **744B 全量模型本地部署硬件要求极高**：激活参数 40B，建议优先使用官方 API 或国产芯片适配集群，个人消费级 GPU 无法承载。
- ⚠️ **Sparse Attention 是新集成特性**：首次引入 DeepSeek Sparse Attention，长文本边界场景建议实测验证，不要默认与 Dense Attention 完全等效。

---

### 🏷️ 行业标签

#GLM-5 #AgenticEngineering #开源大模型 #智谱AI #SWEbench #CodeAgent #长程任务 #国产芯片 #MITLicense #ZCode

---

---
