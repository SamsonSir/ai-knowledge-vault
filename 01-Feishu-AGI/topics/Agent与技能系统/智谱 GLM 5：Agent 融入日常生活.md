# Agent与技能系统

## 57. [2026-02-12]

## 📓 文章 6


> 文档 ID: `W7UlwlzY1igc77kZ8AzcK398nRh`

**来源**: 智谱 GLM 5：Agent 融入日常生活 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: GLM-5 是专为多阶段、长步骤 Agentic 任务设计的开源模型，本文通过聚会选点、资讯日报两个生活场景，提供可直接复刻的 Agent 配置 SOP。

**核心逻辑**:

- **GLM-5 参数规模**：总参数从 GLM-4.7 的 355B（激活 32B）扩展至 744B（激活 40B），预训练数据从 23T 提升至 28.5T
- **三项关键技术升级**：① 异步强化学习框架「Slime」提升后训练效率；② 引入 DeepSeek Sparse Attention 机制，长文本效果无损且降低部署成本；③ 更大规模预训练算力提升通用智能
- **基准测试表现**：Coding 和 Agent 跑分进入开源模型前列，多个榜单基本对齐 Claude Opus 4.5
- **可用入口**：Z.ai、智谱清言、BigModel 均已上线，Z.ai 官网提供免费 Agent 模式体验
- **开源协议**：MIT 协议，已纳入 GLM Coding Plan，兼容 Claude Code、Opencode、OpenClaw 等主流 Agent 工具；订阅地址：`https://bigmodel.cn/glm-coding`
- **聚会选点任务实测**：4 分钟内无人干预，自主调用高德地图工具 40 次，交错思考 25 轮，输出含每人出行方案的综合选点结果，并生成可在浏览器查看的 HTML 可视化路线图
- **资讯日报任务实测**：一条指令完成多信源抓取→去重→摘要→排版→网站部署全流程，Agent 自适应三级抓取策略（RSS / WebFetch / Browser MCP）
- **当前限制**：GLM-5 为纯文本模型，不支持多模态视觉输入，"贴图让 AI 照着做"类任务受限，官方采用 GLM-4.6v 联用方式兼容
- **2026 年 Agent 趋势**：Agentic 模型 + MCP 连接现实服务 + Skill 定义 SOP + Memory 沉淀偏好，Personal Agent 拼图初具雏形，将从 IDE 走向每个人的日常

---

### 🎯 关键洞察

**为什么聚会选点是好的 Agent Benchmark？**
原因：需要拆解任务（解析多人出发地为经纬坐标）→ 调用工具（批量查询候选点、交叉计算通勤方案）→ 多步自主执行（无人干预推进 25 轮思考）。
动作：GLM-5 主动查询大量不同点位、不同交通方式的耗时，用一次性路径规划接口交叉计算。
结果：输出每人出行方案（起点、路线、交通方式、预计时长），并生成 HTML 可视化地图，与高德 APP 实际导航结果近乎一致。

**为什么资讯日报是 Agent 的"Hello World"？**
原因：多信源、多工具、流水线处理，规则明确，重复性高，人工执行成本极大（每天打开十几个网站逐个翻阅）。
动作：Agent 自行判断每个信源的抓取策略，逐一执行后统一去重、摘要、排版。
结果：一条指令完成信源抓取→入库→分条摘要→合并日报→网站更新全过程。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 高德地图 MCP | `{"mcpServers":{"amap-maps-streamableHTTP":{"url":"https://mcp.amap.com/mcp?key=【你的Key】"}}}` | Agent 可查询地点、规划路线 | Key 需在高德开放平台申请，个人开发者每月 15w 次额度 |
| 高德 MCP Key 申请 | 注册地址：`https://console.amap.com/dev/key/app`，参考文档：`https://lbs.amap.com/api/mcp-server/create-project-and-key` | 获取 MCP Key | 需注册开发者身份并创建应用 |
| GLM Coding Plan | `https://bigmodel.cn/glm-coding` | 在 Claude Code 等工具中接入 GLM-5 | 发布当日因大量用户涌入，API 速率出现短期波动 |
| eze-skills（日报 Skill） | `https://github.com/eze-is/eze-skills` | 获取 Daily-news 等全部公开 Skill | 多信源并行抓取策略仍在迭代，主流程已可用 |
| Z Code 工具 | Z.ai 官网 | 手机远程指挥桌面端 Agent，处理代码、生活办公复杂任务 | — |

---

### 🛠️ 操作流程：多人聚会选点 Agent

1. **准备阶段：安装 Claude Code**
   参考「Agent Skills 终极指南」历史文章，在「第二部分：Skill 完全教程」中完成安装。

2. **获取高德 MCP Key**
   - 访问 `https://console.amap.com/dev/key/app`
   - 注册开发者身份 → 创建应用 → 获取 Key
   - 个人开发者每月免费额度：15w 次地图服务

3. **配置高德地图 MCP（让 Claude Code 自动完成）**
   在 Claude Code 对话界面发送以下 Prompt：
   ```
   添加 MCP：
   {
     "mcpServers": {
       "amap-maps-streamableHTTP": {
         "url": "https://mcp.amap.com/mcp?key=【此处替换为你的 MCP Key】"
       }
     }
   }
   ```
   Agent 自动完成剩余配置，完成后重启 Claude Code。

4. **核心执行：发送任务 Prompt**
   将以下信息发给配好 MCP 的 GLM-5 / Claude Code（对参与者信息稍作调整）：
   - 每个人的出发地
   - 每个人的交通偏好（地铁/开车/步行等）
   - 优化目标（如：让路程最远的人耗时最短）

5. **验证与可视化**
   任务完成后，追加发送：
   ```
   给我做一个浏览器能看的 HTML 地图，用地图可视化标点体现出来他们的起点和最终的终点以及大致的路线。用于让参会者一眼明白自己的路线建议方案。
   ```
   可进一步要求切换地图风格（如 Apple Map 风格）。

6. **人工验证**
   手动与高德 APP 实际导航建议比对，验证出行方案与用时的真实性。

---

### 🛠️ 操作流程：资讯日报 Agent

1. **获取 Skill**
   从 `https://github.com/eze-is/eze-skills` 下载 `daily-news` Skill。

2. **配置信源**
   告知 Agent 想关注的信源（如 OpenAI 官网 News、Anthropic 官网 News、X 特定关注者、海外科技资讯网站等）。

3. **核心执行**
   发送一条 Skill 调用指令，Agent 自动执行：
   - Level 1：RSS 源 → 直接解析 feed
   - Level 2：普通网页 → WebFetch 抓取
   - Level 3：需登录或 JS 渲染页面 → Browser MCP 操作浏览器，绕过反爬机制

4. **输出结果**
   Agent 自动完成：信源抓取 → 入库 → 去重 → 分条摘要 → 合并日报 → 部署为结构化网页

---

### 💡 具体案例/数据

**聚会选点实测数据**：
- 参与人数：6-7 人，各自从不同地点出发
- 执行时长：4 分钟
- 工具调用次数：40 次（高德地图 MCP）
- 思考轮次：25 轮
- 人工干预：0 次
- 验证结果：与高德 APP 实际导航建议近乎一致 ✅

**资讯日报实测范围**：
- 信源类型：OpenAI 官网 News、Anthropic 官网 News、X 特定关注者、部分海外科技资讯网站
- 处理时间跨度：最近 3 天
- 全流程：一条指令完成，无需人工介入

---

### 📝 避坑指南

- ⚠️ GLM-5 是纯文本模型，不支持图片输入，前端风格迁移、"贴图照着做"等视觉提示场景效果差，官方建议联用 GLM-4.6v
- ⚠️ 发布初期 API 速率出现短期波动，高并发场景下需预留重试机制
- ⚠️ 高德 MCP Key 配置完成后必须重启 Claude Code 才能生效
- ⚠️ `daily-news` Skill 的多信源并行抓取策略仍在迭代，主流程可用但并行性能未完全优化
- ⚠️ 高德个人开发者每月 15w 次额度，多人高频使用需注意用量

---

### 🏷️ 行业标签

#GLM5 #智谱AI #AgenticAI #MCP #ClaudeCode #PersonalAgent #多步工具调用 #日报自动化 #开源模型

---

---
