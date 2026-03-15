# 工作流自动化

## 27. [2026-04-24]

## 📘 文章 3


> 文档 ID: `E6u4wbCwwiR1L4kXspBckbORnEy`

**来源**: 彬子：Trae，Coze，MCP 梦幻联动，打造超好用小红书封面生成器 | **时间**: 2025-04-24 | **原文链接**: `https://mp.weixin.qq.com/s/g67gxbhkY85kRfGMQzypYA`

---

### 📋 核心分析

**战略价值**: 用 Trae 原生 MCP + 自定义 Agent + Coze 工作流三层联动，将「输入笔记内容 → 自动提炼文案风格 → 生成可下载封面 HTML」全流程打通，实现小红书封面零手工设计。

**核心逻辑**:
- **旧方案痛点**：Trae AI Coding 写 MCP Server 代码，但调用 MCP 时需切换到 Cline 对话界面，两个交互面来回切换不流畅。
- **新方案升级点**：新版 Trae 原生支持 MCP，同时支持自定义 Rules 和 Agents，三者在同一界面无缝衔接。
- **整体架构分三层**：① 用户在 Trae 对话框输入笔记内容并 @Builder with MCP → ② Builder 调用自建 MCP Server，MCP Server 背后通过 Coze API 触发工作流 → ③ 工作流返回文案+风格后，@小红书封面设计师 Agent 生成封面 HTML。
- **Coze 工作流双并行节点**：一个大模型节点专门提炼封面主副标题、账号名、标语；另一个大模型节点根据笔记内容 few-shots 创作匹配的风格描述（设计风格/文字排版/视觉元素三段式），两节点并行执行提升效率。
- **Trae Rules 的核心价值**：将 Coze API 三步调用逻辑（发起对话 → 轮询状态 → 获取消息）写入 `.trae/rules/project_rules.md`，后续每次让 Builder 创建 MCP Server 时无需重复说明，只需输入变化的业务需求部分，大幅减少沟通成本和返工。
- **MCP Server 创建方式**：通过 `npx @modelcontextprotocol/create-server` 命令脚手架创建，使用 TypeScript + axios，入参只有一项（传入文本），只使用 MCP 的 Tools 功能，Builder 基于 Rules 一步到位生成完整代码目录和 `src/index.ts`。
- **调试验证路径**：MCP Server 创建完成后执行 `npm run inspector`，打开 `https://127.0.0.1:6274`，点击 Connect → List Tools 找到 `generate_redbook_cover_style`，输入测试内容验证返回结果是否与 Coze 工作流直接执行一致。
- **小红书封面设计师 Agent 的提示词来源**：直接使用歸藏老师结构化提示词中「不变的部分」（尺寸/排版/技术实现要求），不含 MCP 调用逻辑，专注封面 HTML 生成。
- **封面提示词核心约束**：比例严格 3:4，文字占页面至少 70% 空间，主标题字号比副标题大三倍以上，主标题提取 2-3 个关键词做特殊处理（描边/高亮/不同颜色），使用 html2canvas 实现一键保存，保存图片不含界面元素。
- **风格描述为 few-shots 泛化生成**：不是固定风格库，而是让大模型根据笔记内容的主题、情感、目标受众，从色彩/构成/设计形式/美学规范/细节处理等维度现场创作匹配风格，保证任意笔记内容都能泛化处理。

---

### 🎯 关键洞察

**Rules 是降低 AI 协作摩擦的核心杠杆**：将项目中「不变的约定」（如 Coze API 三步调用顺序、数据结构解析逻辑）沉淀进 Rules，等于给 Agent 装了长期记忆。每次新建 MCP Server 只需输入「变的部分」（业务需求），Builder 自动结合 Rules 生成完整代码，避免每次首轮对话写超长说明。

**双 Agent 分工的设计逻辑**：Builder with MCP 负责「调用外部服务获取数据」，小红书封面设计师负责「基于数据生成产物」。两者职责边界清晰，提示词互不干扰，且可以在同一对话流中通过 @ 无缝切换，不需要离开 Trae 界面。

**Coze 工作流的 few-shots 风格生成是泛化关键**：如果风格是固定的（如只有「现代商务风」），则只能处理特定类型笔记。通过让大模型参考示例格式现场创作风格描述，任何主题的笔记（科技/生活/活动/知识）都能得到匹配的视觉风格，系统具备真正的泛化能力。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| Trae Rules | 路径：`.trae/rules/project_rules.md`，写入 Coze API 三步调用逻辑和数据结构 | Builder 创建 MCP Server 时自动参考，无需重复说明 | 点击右侧对话面板 ⚙️ → 规则 → 项目规则中添加，Trae 自动创建文件 |
| Coze 工作流 | 工作流名：`ReadBook_Style`，两个并行大模型节点 | 并行输出文案提炼结果 + 风格描述 | 需提前记录 Bot ID 和 API Key |
| MCP Server 创建 | `npx @modelcontextprotocol/create-server`，项目名：`mcp-server-coze-redbook_cover_style`，TS + axios | 生成完整代码目录和 `src/index.ts` | 入参只有一项（传入文本），只用 Tools 功能 |
| MCP Server 调试 | `npm run inspector` → 打开 `https://127.0.0.1:6274` → Connect → List Tools | 看到 `generate_redbook_cover_style` 工具，输入测试内容验证返回 | 若 Builder 未自动执行，告诉它「阅读 README.md 来完成调试」或手动在终端执行 |
| Trae MCP 配置 | ⚙️ → MCP → 添加 → 手动配置，命令用 `node`，参数填项目路径下 `build/index.js` 的绝对路径 | `mcp-server-coze-redbook_cover_style` 关联到 Builder with MCP Agent | 路径可在 Trae 中右击文件 → 复制路径获取 |
| 小红书封面设计师 Agent | ⚙️ → 智能体 → 创建智能体，提示词使用歸藏老师封面提示词「不变部分」，取消 MCP 关联 | 专项封面 HTML 生成，可通过 @ 调用 | 提示词不含 MCP 调用逻辑，与 Builder 职责分离 |

---

### 🛠️ 操作流程

**1. 准备阶段：Coze 工作流搭建**

- 在 Coze 创建工作流 `ReadBook_Style`
- 添加两个并行大模型节点：

节点一（文案提炼）提示词：
```
# 角色
你是一位专业的小红书封面文案师，擅长精准提炼用户输入的内容，转化为吸引人的小红书封面文案。

## 技能
### 技能 1: 生成小红书封面文案
1. 当用户输入内容后，根据内容主题、亮点等元素，提炼出主副标题和点缀文案。
2. 将生成的文案按照规定结构整理。
===回复示例===
- 封面文案：[主副标题],[点缀的文案]
- 账号名称：[如果有]
- 标语：[如果有]
===示例结束===
```

节点二（风格创作）提示词：
```
# 角色
你是一位专业的小红书封面设计风格顾问，擅长根据用户输入的内容，精准提炼并返回与之适配的最佳风格描述。

## 技能
1. 仔细研读用户输入的内容主题、情感、目标受众等关键要素。
2. 依据输入信息的特点，从色彩、构成、设计形式、美学规范、细节处理等多方面构思与之契合的风格描述。
3. 参考以下示例格式分别阐述设计风格、文字排版风格、视觉元素风格：
[此处放入「现代商务资讯卡片风」完整示例作为 few-shots 参考]
```

- 发布工作流和 Bot，记录 Bot ID 和 API Key

**2. Trae Rules 配置：写入 Coze API 三步调用逻辑**

路径：`.trae/rules/project_rules.md`，写入以下内容：

```markdown
# Coze API 调用的说明文档
## 第一步
### 先通过
curl --location --request POST 'https://api.coze.cn/v3/chat' \
--header 'Authorization: Bearer pat_dGstyY6RZxxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
  "bot_id": "指定的bot的id",
  "user_id": "12345678",
  "stream": false,
  "auto_save_history": true,
  "additional_messages": [{
    "role": "user",
    "content": "内容描述",
    "content_type": "text"
  }]
}'
### 返回数据结构
{ data: { "id": "Chat ID", "conversation_id": "...", "status": "completed", ... } }

## 第二步
### 发送查询请求，以 1500ms 频率轮询，不超过 30 次
curl --location --request GET 'https://api.coze.cn/v3/chat/retrieve?chat_id=id&conversation_id=conversation_id' \
--header 'Authorization: Bearer pat_dGstyY6RZxxxxx'
### 返回数据结构
{ data: { "status": "completed", ... } }

## 第三步
### 查看 status 直到 completed 时调用
curl --location --request GET 'https://api.coze.cn/v3/chat/message/list?chat_id=id&conversation_id=conversation_id' \
--header 'Authorization: Bearer pat_OYDacMzM3WyOWV3Dtj2bHRMymzxP****'
### 返回数据结构
{ data: [{ "role": "assistant", "content": "回复内容", "type": "answer" }] }
### 获取 data 数组中第一个的 content，返回给 Client 端
```

**3. 创建 MCP Server**

在 Trae 中 @Builder，输入：
```
我需要通过 npx @modelcontextprotocol/create-server 命令创建一个使用 Coze API 来输入内容获取小红书封面风格的 MCP 服务：mcp-server-coze-redbook_cover_style。
1. 入参只有一项：传入的文本
2. 只使用 MCP 的 Tools 功能
3. 通过 API 的方式调用 Coze 的指定的 Bot 生成返回小红书封面的描述
4. 使用 TS 代码，网络请求使用 axios 库
```

- 等待 Builder 完成，期间点击「接受全部」
- Builder 完成后自动执行 `npm run inspector`，或手动执行
- 打开 `https://127.0.0.1:6274` → Connect → List Tools → 找到 `generate_redbook_cover_style`
- 输入测试笔记内容，验证返回风格描述符合预期

**4. 配置 MCP Server 到 Trae**

- ⚙️ → MCP → 添加 → 手动配置
- 命令：`node`
- 参数：`/你的项目路径/mcp-server-coze-redbook_cover_style/build/index.js`（右击文件复制路径）
- 保存，MCP 自动关联到 Builder with MCP Agent

**5. 创建小红书封面设计师 Agent**

- ⚙️ → 智能体 → 创建智能体，命名：`小红书封面设计师`
- 提示词使用歸藏老师封面提示词不变部分（核心约束如下）：

```
你是一位优秀的网页和营销视觉设计师...
## 基本要求
- 比例严格为 3:4（宽:高）
- 设计一个边框为 0 的 div 作为画布，确保生成图片无边界
- 最外面的卡片需要为直角
- 将提供的文案提炼为 30-40 字以内的中文精华内容
- 文字必须成为视觉主体，占据页面至少 70% 的空间
- 运用 3-4 种不同字号创造层次感，关键词使用最大字号
- 主标题字号需要比副标题和介绍大三倍以上
- 主标题提取 2-3 个关键词，使用特殊处理（描边/高亮/不同颜色）
## 技术实现
- 使用现代 CSS 技术（flex/grid 布局、变量、渐变）
- 添加一个不影响设计的保存按钮
- 使用 html2canvas 实现一键保存为图片功能
- 保存的图片只包含封面设计，不含界面元素
- 使用 Google Fonts 或其他 CDN 加载适合的现代字体
- 可引用在线图标资源（如 Font Awesome）
```

- 取消 MCP 关联，保存

**6. 验证：从笔记到封面一气呵成**

- 新建小红书封面专用文件夹
- 在 Trae 对话框输入笔记内容，@Builder with MCP，格式：`帮我设计小红书封面 --- [笔记内容]`
- Builder 调用 `mcp-server-coze-redbook_cover_style` 获取风格描述（如「科技活力派对风」）
- 在同一对话框 @小红书封面设计师，传入文案 + 风格描述
- 等待生成本地 HTML 文件（如 `xiaohongshu_cover.html`），浏览器打开，点击「保存封面图片」下载

---

### 💡 具体案例/数据

测试输入：WaytoAGI 社区两周年 X2050 活动笔记（3 天 2 夜、4 月 25-27 日、杭州云栖小镇、含拔河破冰/AI 大咖论坛/灵感派对等活动）

MCP 返回风格：**科技活力派对风**

最终产物：`xiaohongshu_cover.html` → 点击保存 → `WaytoAGI社区两周年小红书封面.png`

---

### 📝 避坑指南

- ⚠️ Builder 完成 MCP Server 创建后若未自动执行 `npm run inspector`，需手动告诉它「阅读 README.md 来完成调试」，或自己在终端执行 `npm run inspector`
- ⚠️ Trae MCP 手动配置时，`build/index.js` 路径必须是绝对路径，推荐在 Trae 中右击文件 → 复制路径获取，避免路径错误导致 MCP 无法启动
- ⚠️ 小红书封面设计师 Agent 的提示词不要加入 MCP 调用逻辑，否则会与 Builder 的职责产生混淆，两个 Agent 职责边界要清晰
- ⚠️ Coze 工作流轮询逻辑：间隔 1500ms，最多轮询 30 次，超出则视为超时，需在 MCP Server 代码中严格实现此逻辑
- ⚠️ 封面效果不满意时，优化方向是提示词（风格描述的 few-shots 示例质量），而非架构本身，架构已跑通

---

### 🏷️ 行业标签

#Trae #MCP #Coze #AI工作流 #小红书封面 #AI编码 #Agent #自动化设计 #提示词工程

---

---
