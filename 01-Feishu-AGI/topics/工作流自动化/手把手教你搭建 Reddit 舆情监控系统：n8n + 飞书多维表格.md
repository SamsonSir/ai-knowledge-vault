# 工作流自动化

## 10. [2026-01-23]

## 📚 文章 8


> 文档 ID: `Qz1dwWfbtitOJrk7Aptc29fOnmd`

**来源**: 手把手教你搭建 Reddit 舆情监控系统：n8n + 飞书多维表格 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 用 n8n + HTTP 伪装请求绕过 Reddit 风控，配合飞书多维表格 + DeepSeek AI，实现每日自动抓取指定板块热帖并完成中文情感分析、风险评分的全自动舆情监控流水线。

**核心逻辑**:

- **绕过 Reddit 风控的根本原因**：n8n 原生 RSS 节点和官方 Reddit 节点均会暴露机器人特征，触发风控。解决方案是用 HTTP 节点手动添加 `User-Agent` Header 伪装成 Chrome 浏览器请求，Reddit 无法区分真实用户与自动化脚本。
- **RSS URL 结构是核心变量**：`https://www.reddit.com/r/{板块名}/top/.rss?t=day`，其中 `{板块名}` 是唯一需要修改的部分；`/top/` 可换成 `/new/`；`?t=day` 限定过去 24 小时；`.rss` 让 Reddit 返回 XML 而非 HTML。
- **多板块合并监控**：URL 中用 `+` 连接多个板块名，如 `r/doggrooming+litterrobot+dropship/top/.rss?t=day`，一次请求抓取全部，无需多条工作流。
- **数据管道四步转换**：XML 原始数据 → XML to JSON 节点转换 → Split Out 节点按 `feed.entry` 拆分为独立条目 → Filter 节点用 `{{ $now.minus({hours: 24}) }}` 过滤 24 小时外帖子，确保数据新鲜度。
- **AI 分析输出严格结构化**：系统提示词强制 AI 只输出 Raw JSON（无 Markdown 包裹），字段固定为 `summary`/`sentiment`/`topic`/`risk_score`，避免后续解析失败。特别注明识别 Reddit 特有的 Sarcasm（阴阳怪气），反讽归为"负面"。
- **Code 节点做容错解析**：AI 偶尔会在 JSON 外包裹 ` ```json ``` `，Code 节点用 `.replace(/```json|```/g, "").trim()` 清理后再 `JSON.parse()`，并用 try/catch 跳过格式异常条目，防止整条流水线卡死。
- **飞书字段类型必须精确匹配**：`发布时间` 和 `获取日期` 必须是"日期"类型，`情感倾向` 和 `主题` 必须是"单选"类型且选项名称完全一致，`风险评分` 必须是"数字"类型，任何偏差都会导致写入失败。
- **Reddit ID 去重机制**：每条帖子的 `Reddit ID` 全局唯一，高频抓取（如每 30 分钟）时可在飞书多维表格中按此字段筛选，快速识别重复条目。
- **定时触发需配合时区设置**：n8n 工作流时区默认非本地时区，中国用户需在工作流设置中选择 `Asia/Shanghai`，否则"每天早上 8 点"实际执行时间会偏移。
- **工作流激活是自动运行的前提**：定时触发配置完成后必须点击"激活"开关，且 n8n 实例必须保持运行状态，工作流才会按时执行。

---

### 🎯 关键洞察

**为什么 HTTP 节点 + User-Agent 能绕过风控**：Reddit 的反爬机制主要识别请求头特征，原生 RSS 节点发出的请求头暴露了 n8n 的身份。通过在 HTTP 节点的 Headers 中注入标准 Chrome 浏览器的 User-Agent，请求特征与真实用户完全一致，Reddit 服务器无法区分。这是一个"最小成本绕过"方案，不需要代理或 Cookie。

**为什么用 RSS 而不是 Reddit 官方 API**：官方 API 申请周期长且不稳定，RSS 端点是 Reddit 公开提供的数据接口，无需认证，加上 `.rss` 后缀即可获取结构化 XML 数据，稳定性更高，适合长期运行的监控场景。

**风险评分设计逻辑**（原因 → 动作 → 结果）：
- 1-2 分：普通吐槽，无需介入
- 3 分：具体产品/服务缺陷，触发常规客诉处理流程
- 4-5 分：欺诈/安全事故/法律风险/病毒式传播，需立即人工介入

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| HTTP 节点 URL | `https://www.reddit.com/r/ArtificialInteligence/top/.rss?t=day` | 获取指定板块 24h 热帖 XML | Response Format 必须选 **Text**，否则解析失败 |
| HTTP 节点 Header | `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36` | 伪装浏览器，绕过风控 | 必须手动添加，不能省略 |
| XML to JSON 节点 | 默认配置即可 | XML → JSON 结构 | 转换后数据仍在 `feed` 对象内，需下一步拆分 |
| Split Out 节点 | Fields: `feed.entry` | 每条帖子变为独立 item | 字段路径必须是 `feed.entry`，不能是 `entry` |
| Filter 节点（时间过滤） | `published` 字段 > `{{ $now.minus({hours: 24}) }}` | 过滤 24h 外帖子 | 时区不对会导致过滤逻辑错误，先检查工作流时区 |
| AI Agent 用户提示词 | `分析这篇帖子：{{ $json.title }}{{ $json.content._ }}` | 传入标题+正文 | `content._` 是 XML 转 JSON 后正文的路径 |
| AI Agent 系统提示词 | 见下方完整 Prompt | 输出固定结构 JSON | 必须注明"不要包含 Markdown 标记"，否则 Code 节点解析失败 |
| Code 节点 | 见下方完整代码 | 提取 AI 输出字段 | 兼容 `output` 和 `text` 两种字段名 |
| 飞书节点包名 | `n8n-nodes-feishu-lite` | 支持飞书多维表格读写 | 中文搜索不到，必须用英文搜索 |
| 飞书写入请求体 | 见下方完整 JSON.stringify 代码 | 数据写入多维表格 | `风险评分` 必须用 `Number()` 强制转换，否则类型不匹配 |
| 定时触发 Cron | 每天早上 8 点对应的 Cron 表达式 | 自动定时执行 | 激活后 n8n 实例必须保持运行 |

---

### 🛠️ 操作流程

**1. 准备阶段：飞书配置**

1. 打开飞书开发平台：`https://open.feishu.cn/app?lang=zh-CN`，登录后创建企业自建应用，填写名称和描述
2. 进入应用权限管理，搜索"多维表格"，全选相关权限并确认开通
3. 创建应用版本（版本号随意），发布上线
4. 复制并保存 **App ID** 和 **App Secret**（后续 n8n 凭证需要）
5. 打开飞书客户端，新建多维表格，按以下字段严格配置：

| 字段名称 | 字段类型 | 补充说明 |
|---|---|---|
| 标题 | 文本 | — |
| Reddit ID | 文本 | — |
| 发布时间 | 日期 | — |
| 原帖链接 | 超链接 | — |
| AI摘要 | 文本 | — |
| 情感倾向 | 单选 | 选项：正面、中立、负面 |
| 风险评分 | 数字 | — |
| 主题 | 单选 | 选项：质量、物流、客服、价格、信任欺诈、其他 |
| 获取日期 | 日期 | — |

6. 删除表格中的空白记录
7. 在多维表格中添加应用，确保权限为**可编辑**

---

**2. 核心执行：n8n 工作流搭建**

**节点1：手动触发**（搭建阶段用，最后替换为定时触发）

**节点2：HTTP 请求节点（伪装请求数据）**
- Method: GET
- URL: `https://www.reddit.com/r/ArtificialInteligence/top/.rss?t=day`
- Headers 添加：
  ```
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36
  ```
- Response Format: **Text**

**节点3：XML to JSON**（默认配置）

**节点4：Split Out**
- Fields: `feed.entry`

**节点5：Filter（保留24小时之内的信息）**
- 字段：`published`
- 条件：大于 `{{ $now.minus({hours: 24}) }}`

**节点6：AI Agent**

用户提示词：
```
分析这篇帖子：{{ $json.title }}{{ $json.content._ }}
```

系统提示词：
```
# Role
电商舆情分析师 (Reddit 专攻)

# Task
分析用户评论，输出 JSON。

# Analysis Criteria
1.  **summary**: 中文摘要，由"对象+事件+评价"组成（例如："用户投诉蓝牙耳机无法连接"）。
2.  **sentiment**: 情感倾向，仅限输出：['正面', '中立', '负面']。
    * *注意：必须准确识别 Reddit 特有的阴阳怪气（Sarcasm），反讽应归为"负面"。*
3.  **topic**: 话题分类，仅限输出：['质量', '物流', '客服', '价格', '信任欺诈', '其他']。
    * *质量：产品损坏、功能缺陷、与描述不符。*
    * *物流：发货慢、丢件、包装破损。*
    * *客服：态度差、拒绝退款、无人回应。*
    * *信任欺诈：怀疑假货、诈骗网站 (Scam)、被盗刷、店铺消失。*
4.  **risk_score**:
    - 1-2分: 安全/普通吐槽（无实质风险）。
    - 3分: 具体的产品/服务缺陷反馈（常规客诉）。
    - 4-5分: 涉及欺诈、安全事故、法律风险或病毒式负面传播（高危）。

# Output Format
仅输出 Raw JSON (不要包含 Markdown 标记):
{"summary": "...", "sentiment": "...", "topic": "...", "risk_score": int}
```

AI 模型：DeepSeek（需在 `https://www.deepseek.com/` 注册并充值，创建 API Key，在 n8n 中创建 DeepSeek 凭证）

**节点7：Code 节点（数据提取）**
```javascript
for (const item of items) {
  try {
    const aiOutputString = item.json.output || item.json.text || "{}";
    const cleanJson = aiOutputString.replace(/```json|```/g, "").trim();
    const aiData = JSON.parse(cleanJson);
    Object.assign(item.json, aiData);
  } catch (error) {
    item.json.parse_error = "这一条数据格式不对，跳过";
  }
}
return items;
```

**节点8：飞书节点 - 解析多维表格地址**
- 安装社区节点包：`n8n-nodes-feishu-lite`（左下角齿轮 → 社区节点 → 下载）
- 操作：解析多维表格地址
- 凭证：填入 App ID 和 App Secret
- 粘贴多维表格 URL，测试获取 `app_token` 和 `table_id`

**节点9：飞书节点 - 新增记录**
- 操作：新增记录
- 填入上一步获取的 `app_token` 和 `table_id`
- 请求体：
```javascript
{{
  JSON.stringify({
    "fields": {
      "标题": $('保留24小时之内的信息').item.json.title,
      "Reddit ID": $('保留24小时之内的信息').item.json.id,
      "AI摘要": $('数据提取').item.json.summary,
      "情感倾向": $('数据提取').item.json.sentiment,
      "主题": $('数据提取').item.json.topic,
      "风险评分": Number($('数据提取').item.json.risk_score || 0),
      "原帖链接": {
        "text": "点击查看",
        "link": $('保留24小时之内的信息').item.json['media:thumbnail']?.url || "https://www.reddit.com"
      },
      "发布时间": $('保留24小时之内的信息').item.json.published ? new Date($('保留24小时之内的信息').item.json.published).getTime() : Date.now()
    }
  })
}}
```

---

**3. 验证与自动化**

1. 全流程手动测试，确认数据写入飞书多维表格
2. 将触发节点替换为**定时触发**，设置 Cron 为每天早上 8 点
3. 确认工作流时区设置为 `Asia/Shanghai`
4. 保存工作流，点击**激活**开关
5. 在执行历史中确认工作流状态正常

---

### 💡 具体案例/数据

**多板块监控 URL 示例**（宠物用品场景）：
```
https://www.reddit.com/r/doggrooming+litterrobot+dropship/top/.rss?t=day
```
- `r/doggrooming`：宠物美容工具（剪刀、电推剪、梳子）用户反馈
- `r/litterrobot`：自动猫砂盆标杆品牌板块，监控卡猫砂、除臭、耗材等投诉
- `r/dropship`：独立站选品情报，TikTok/Facebook 宠物爆品趋势

**更换监控板块示例**：
- 原 URL：`https://www.reddit.com/r/ArtificialInteligence/top/.rss?t=day`
- 替换为 PromptEngineering 板块：`https://www.reddit.com/r/PromptEngineering/top/.rss?t=day`
- 只需修改 HTTP 节点的 URL 字段，其余节点无需改动

**AI 输出示例**（期望格式）：
```json
{"summary": "用户投诉蓝牙耳机无法连接", "sentiment": "负面", "topic": "质量", "risk_score": 3}
```

---

### 📝 避坑指南

- ⚠️ **飞书字段名称零容错**：字段名必须与教程完全一致（包括中文字符），一个字的偏差都会导致写入失败，建议复制粘贴而非手动输入
- ⚠️ **单选字段选项必须预先创建**：`情感倾向` 的"正面/中立/负面"和 `主题` 的六个选项必须在建表时手动添加，AI 输出的值必须与选项完全匹配，否则写入报错
- ⚠️ **Response Format 必须选 Text**：HTTP 节点获取 RSS 数据时，如果不选 Text 格式，XML 数据无法正确传递给 XML to JSON 节点
- ⚠️ **Code 节点兼容两种字段名**：不同版本的 AI Agent 节点输出字段可能是 `output` 或 `text`，代码中已做兼容处理，不要删除
- ⚠️ **风险评分必须强制转 Number**：`Number($('数据提取').item.json.risk_score || 0)` 中的 `Number()` 不能省略，AI 输出的数字是字符串类型，飞书数字字段不接受字符串
- ⚠️ **工作流激活 ≠ 自动运行**：激活后 n8n 实例本身必须保持运行（本地部署需保持开机，云部署无此问题）
- ⚠️ **社区节点中文搜索无效**：搜索飞书节点必须输入英文关键词，中文搜索返回空结果
- ⚠️ **时区偏移导致定时不准**：工作流时区默认 UTC，中国用户必须在工作流设置中改为 `Asia/Shanghai`，否则"早上 8 点"实际是北京时间下午 4 点

---

### 🏷️ 行业标签

#n8n #Reddit舆情监控 #飞书多维表格 #DeepSeek #自动化工作流 #跨境电商 #情感分析 #RSS爬虫 #无代码自动化

---

---
