# 工作流自动化

## 7. [2026-01-20]

## 📓 文章 6


> 文档 ID: `AxrnwCEf7ish8bk6ceScv3BUnje`

**来源**: 饼干哥哥：我用n8n+AI记忆系统 MemOS，给SHEIN 搭了个销售Agent | **时间**: 2026-01-20 | **原文链接**: `https://mp.weixin.qq.com/s/qm4Av7Ki...`

---

### 📋 核心分析

**战略价值**: 用 n8n + MemOS 2.0 构建一套「身份锚定 + 双重检索 + 记忆闭环」的跨境电商邮件销售 Agent，让 AI 客服从无状态问答升级为持续自进化的用户关系管理系统。

**核心逻辑**:

- 传统 RAG 客服是无状态的：每轮对话结束后记忆清零，无法跨会话识别"上次买了 M 码觉得紧"这类用户历史，只能冷回复"请提供订单号"
- MemOS 2.0 解决三层问题：① 静态知识库（SOP/尺码表/物流政策，支持 PDF/Markdown/TXT 上传）② 动态用户画像（自动抓取身高体重、偏好、历史行为存为长期记忆）③ 自动演化（对话中直接触发记忆更新，无需手动插入）
- 身份锚定机制：用 Gmail 的 `threadId` 作为 `conversation_id`，用发件人邮箱正则提取作为 `user_id`，两者合力锁定"是谁在哪个会话里说了什么"
- 双路并行检索：上路调 `/search/memory`（静态文档 + 用户长期画像），下路调 `/get/message`（最近 10 条对话短期上下文），两路 Merge 后一起喂给大模型
- 记忆闭环写回：每次 AI 回复后调 `/add/message`，把 User Query + AI Output 一次性存回 MemOS，系统自动提取新偏好（如"用户觉得 M 码紧"），下次对话自动规避
- 邮件判断分流：在主流程前接一个小模型（gpt-4o-mini 或 Qwen）做意图识别，只有判断为客户咨询才进入后续流程，过滤垃圾邮件
- Prompt 注入灵魂：禁止说"根据数据库显示"，要求显式引用用户身体数据（"考虑到您 170cm 的高挑身材..."），加 Emoji，输出 HTML 富文本格式邮件正文
- 数据资产沉淀逻辑：客服离职不带走记忆，所有用户偏好/习惯全部沉淀在 MemOS 记忆层，换 10 批运营 AI 依然记得那个"喜欢宽松牛仔裤、住深圳、对运费敏感"的老客户
- 可扩展场景：同套逻辑接 WhatsApp Business API 做私域（高客单价品类如假发/珠宝/3D打印机），或接独立站 Chatbot 做主动导购（"这件大衣和你上次买的靴子超搭"）
- MemOS 已全面开源：`github.com/MemTensor/MemOS`，API 文档：`https://memos-docs.openmem.net/cn/api_docs/core/add_message`

---

### 🎯 关键洞察

**为什么传统 RAG 在跨境电商场景必然失效**：
RAG 的本质是"文档检索 + 生成"，它解决的是"知识在哪里"的问题，但跨境电商客服的核心问题是"这个人是谁、他之前说过什么"。两者根本不在同一个维度。用户问"我上次买的 M 码穿着紧，这次该换 L 吗"，RAG 能检索到尺码表，但检索不到"这个用户上次反馈 M 码紧"这条动态事实。

**MemOS 的核心差异点**：不是更好的向量数据库，而是把"企业静态知识"和"用户动态记忆"统一在同一个系统里，并且记忆会随对话自动演化。用户说"最近搬去上海了" → 系统自动更新地区字段，无需任何手动操作。这解决了以前需要熬夜手动维护记忆更新流程的问题。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| MemOS 知识库创建 | 后台地址：`https://memos-dashboard.openmem.net/cn/knowledgeBase`，右上角「添加知识库」，输入名称，上传 PDF/Markdown/TXT 文件 | 静态文档可被 `/search/memory` 检索 | 默认配置即可，无需额外调参 |
| 知识库 ID 获取 | 在知识库列表页对应条目位置直接复制 | 后续 API 调用必须传此 ID | 创建后立即记录，后续 n8n 节点要用 |
| Gmail Trigger | Poll Times: 每分钟一次；Filters: Label=INBOX + UNREAD | 只处理未读收件箱邮件 | 避免重复处理已读邮件 |
| Set Context Variables | `user_id`: `{{ $json.from.match(/<(.+)>/)?.[1] \|\| $json.To }}`；`conversation_id`: `{{ $json.threadId }}` | 唯一身份锚定 + 多轮会话串联 | threadId 是 Gmail 原生字段，同一邮件线程 ID 不变 |
| 检索记忆（上路） | HTTP 请求节点，调用 `/search/memory`，传 user_id + query | 返回静态文档片段 + 用户长期画像 | 同时检索两类数据，无需分两次调用 |
| 获取上下文（下路） | HTTP 请求节点，调用 `/get/message`，传 conversation_id，limit=10 | 返回最近 10 条对话记录 | limit 建议不超过 10，避免 token 超限 |
| Merge 节点 | Combine By: Position | 将长期记忆与短期上下文合并为单一 JSON 输出给 AI | 必须用 Position 模式，否则数据对不上 |
| AI 回复生成 | 模型建议 GPT-4o 或同级；Prompt 见下方完整版 | 输出 HTML 格式富文本邮件正文 | 意图识别节点用小模型（gpt-4o-mini/Qwen）省成本 |
| 存入记忆（写回） | HTTP 请求节点，调用 `/add/message`，body 包含 user_id + conversation_id + user_query + ai_output | MemOS 自动提取新偏好并更新记忆层 | user_query 和 ai_output 必须同时传，缺一不可 |
| Gmail Send | 开启 HTML 模式，正文字段映射 AI 输出 | 客户收到富文本排版邮件 | 不开 HTML 模式会把标签原样发出去 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 注册 MemOS 账号，进入 `https://memos-dashboard.openmem.net/cn/knowledgeBase`
- 创建知识库，上传客服相关文档（尺码表、退换货政策、物流说明、洗护指南等 PDF/Markdown/TXT）
- 记录知识库 ID
- 准备好 MemOS API Key（用于 n8n HTTP 请求节点鉴权）
- 确保 n8n 已连接 Gmail OAuth

**2. 核心执行（三模块搭建）**

模块一：监听邮件与智能识别
```
Gmail Trigger
  → Poll: 每分钟
  → Filter: INBOX + UNREAD

AI Agent（小模型：gpt-4o-mini 或 Qwen）
  System Prompt:
    我们是电商公司，你是邮件内容判断助手。
    请判断当前邮件内容是否为客户的售前、售后咨询。
    如果是，回复 {"客户邮件":"是"}；否则回复 {"客户邮件":"否"}。

If 节点
  → 条件：客户邮件 == 是
  → 否则：终止流程
```

模块二：知识库 + 记忆 + 上下文检索
```
Set Context Variables
  user_id:          {{ $json.from.match(/<(.+)>/)?.[1] || $json.To }}
  conversation_id:  {{ $json.threadId }}
  user_query:       {{ $json.text }}（邮件正文）

并行执行：
  上路 HTTP Request → POST /search/memory
    body: { user_id, query: user_query, knowledge_base_id: "你的KB_ID" }

  下路 HTTP Request → GET /get/message
    params: { conversation_id, limit: 10 }

Merge 节点
  Combine By: Position
```

模块三：AI 回复生成 + 记忆写回 + 发送
```
AI Agent（大模型：GPT-4o 或同级）
  System Prompt:
    # Role
    你不是机器人，你是 SHEIN 专属时尚顾问 (Style Bestie)。
    目标：用温暖、专业且带时尚感的语气解决问题。

    # Context Data
    1. 记忆与知识库: {{ $('检索记忆').item.json.data.memory_detail_list }}
    2. 对话历史: {{ $('获取历史').item.json.data.message_detail_list }}

    # Guidelines
    - 拒绝机械感：禁止说"根据数据库显示"。
    - 显式记忆：如果发现用户身高体重（如 170cm），必须在回复中显式提及（"考虑到您 170cm 的高挑身材..."）。
    - 情绪价值：适当夸赞用户眼光，使用 Emoji 😊。

    # Output
    必须输出 HTML 格式的邮件正文，使用 <p> 和 <strong> 标签排版。

HTTP Request → POST /add/message
  body: {
    user_id: "{{ $('Set Context Variables').item.json.user_id }}",
    conversation_id: "{{ $('Set Context Variables').item.json.conversation_id }}",
    messages: [
      { role: "user", content: "{{ $('Set Context Variables').item.json.user_query }}" },
      { role: "assistant", content: "{{ $json.output }}" }
    ]
  }

Gmail Send
  To: {{ $('Gmail Trigger').item.json.from }}
  Subject: Re: {{ $('Gmail Trigger').item.json.subject }}
  Body (HTML): {{ $json.output }}
  ✅ 开启 HTML 模式
```

**3. 验证与优化**

- 发一封测试邮件，包含身高体重等个人信息，验证知识库检索是否命中
- 发第二封邮件（同 thread），不重复身材数据，验证 `conversation_id` 是否成功串联上下文
- 发第三封邮件，直接说"还是以前的身材数据"，验证长期记忆是否从 MemOS 正确读取
- 用 Gemini 或 GPT-4o 对回复内容做精准度评估（把知识库文档和回复一起扔进去让它打分）

---

### 💡 具体案例/数据

**测试一：知识库 + 短期记忆**
- 第一封邮件：用户提供身高体重，问尺码推荐（售前咨询）
- 结果：AI 正确命中知识库尺码表，给出精准推荐，Gemini 评分：优秀

**测试二：多轮对话串联**
- 第二封邮件（同 threadId）：追问上一封提到的产品细节
- 结果：通过 `conversation_id` 成功获取前序对话记录，两封独立邮件被串联为连续对话，Gemini 评分：满分

**测试三：长期记忆跨会话调用**
- 第三封邮件（新话题）：直接说"还是以前的身材数据没变，这款牛仔裤选什么码？担心卡裆或腰太紧"
- 结果：AI 从 MemOS 长期记忆中读取历史身材数据，结合尺码表和用户担忧点给出针对性建议，Gemini 评分：发挥稳定

**扩展场景 ROI 对比**：
- WhatsApp 私域：记住"用户上月说想给女儿买生日礼物" → 生日前一周自动推送新品，转化率比群发广告高约 100 倍（作者估算）
- 独立站 Chatbot：主动提示"这件大衣和你上次买的靴子超搭"，替代只会弹优惠券的静态弹窗

---

### 📝 避坑指南

- ⚠️ `user_id` 提取正则 `$json.from.match(/<(.+)>/)?.[1] || $json.To` 中的 `||` 后备值必须保留，部分邮件 from 字段格式不含尖括号会导致提取失败
- ⚠️ Merge 节点必须选 `Combine By: Position`，用其他模式会导致上下两路数据错位
- ⚠️ Gmail Send 节点必须手动开启 HTML 模式，否则 `<p><strong>` 等标签会以纯文本形式发出
- ⚠️ `/add/message` 写回时 user_query 和 ai_output 必须同时传入，只传其中一个 MemOS 无法正确提取偏好
- ⚠️ 意图识别节点用小模型（gpt-4o-mini/Qwen）即可，不要用大模型，这一步只做二分类判断，用大模型纯属浪费
- ⚠️ 知识库文档上传后默认配置即可，不需要手动调向量化参数，过度配置反而可能影响检索效果
- ⚠️ `limit: 10` 是短期上下文拉取的建议上限，超过 10 条容易导致 token 超限，尤其是邮件正文本身就较长时

---

### 🏷️ 行业标签

#n8n #MemOS #AI记忆系统 #跨境电商 #邮件Agent #RAG #用户画像 #销售自动化 #私域运营 #AI客服

---

---
