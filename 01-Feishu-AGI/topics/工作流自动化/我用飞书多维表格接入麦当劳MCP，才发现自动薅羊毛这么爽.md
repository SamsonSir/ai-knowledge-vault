# 工作流自动化

## 3. [2026-01-12]

## 📙 文章 4


> 文档 ID: `NnOxwxrCtiqEm5kyvF7cE5gMnmb`

**来源**: 我用飞书多维表格接入麦当劳MCP，才发现自动薅羊毛这么爽 | **时间**: 2026-03-13 | **原文链接**: https://mp.weixin.qq.com/s/JPUQvMtPLLzUYlW1q-RTzg

---

### 📋 核心分析

**战略价值**: 通过 n8n 中转，将麦当劳官方 MCP 接入飞书多维表格，实现活动日历自动同步、优惠券状态监控、一键自动领券的全自动化薅羊毛流水线。

**核心逻辑**:
- 麦当劳已开放官方 MCP 服务，入口为 `open.mcd.cn`，手机号验证码登录后激活即可获取 Token，Token 是唯一身份凭证，需妥善保管
- 飞书多维表格原生 Agent 节点当前存在 Bug（预计 23 号修复），现阶段必须用 n8n 作为中转层绕过此限制
- 整体数据流为单向直线：`Trigger → AI Agent（调用 MCP）→ Code（数据清洗）→ Feishu（写入多维表格）`
- MCP Client 凭证格式严格：`Value` 必须为 `Bearer ` + Token（Bearer 后有一个空格），Server URL 为 `https://mcp.mcd.cn/mcp-servers/mcd-mcp`，Type 选 `HTTP Server SSE`
- Agent 模型推荐 DeepSeek（性价比高），三个场景对应三套独立 Prompt 和三张飞书表，职责完全分离
- Code 节点是必须存在的防御层：AI 输出经常携带 ` ```json ` Markdown 标记或 JSON 被截断，不清洗直接写入飞书 100% 报错
- 飞书节点配置有两个高频踩坑点：① 图片/链接字段必须选「文本类型」而非「超链接类型」；② 多维表格右上角必须手动「添加应用」，否则机器人无写入权限
- 飞书原生自动化承担通知职责：每日 09:00 推送活动情报，每日 17:20 扫描未领取券并推送含 Webhook URL 的一键领券消息卡片
- `auto-bind-coupons` 工具无需任何入参，调用即全量领取当前所有可用券，Prompt 中需明确告知 Agent 忽略任何传入参数
- 飞书开放平台创建企业自建应用后，必须在「版本管理与发布」创建并发布新版本，否则已开通的权限不会生效

---

### 🎯 关键洞察

**为什么要用 n8n 而不是直接用飞书 Agent 节点？**
原因：飞书多维表格原生 Agent 节点当前有 Bug，无法稳定调用外部 MCP。
动作：引入 n8n 作为中间层，n8n 负责 MCP 调用和数据清洗，飞书只负责接收写入结果。
结果：绕过 Bug 限制，现在就能跑通全流程，不必等官方修复。

**为什么 Code 节点不可省略？**
原因：LLM 输出天然不稳定，即使 Prompt 要求「只输出纯 JSON」，实际仍会出现 ` ```json ` 包裹、末尾截断、单引号替代双引号等问题。
动作：Code 节点用 `robustParse()` 函数做五层兜底解析（标准解析 → 去 Markdown 标记 → 修复截断数组 → JS 引擎执行 → 纯文本兜底封装）。
结果：任何格式的 AI 输出都能被安全转换为飞书可接受的 JSON 结构。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| MCP Token 获取 | 访问 `open.mcd.cn` → 登录 → 控制台 → 激活 → 一键复制 | 获得身份凭证 | Token 不要泄露，先存记事本 |
| MCP Client 凭证 | Name: `Authorization`，Value: `Bearer eyJhbGci...` | n8n 有权调用麦当劳 MCP | Bearer 后必须有一个空格，否则鉴权失败 |
| MCP Server URL | `https://mcp.mcd.cn/mcp-servers/mcd-mcp` | 连接麦当劳 MCP 服务 | Type 必须选 `HTTP Server SSE` |
| Agent 模型 | DeepSeek | 低成本驱动三个场景 | 也可替换其他模型 |
| 触发器-情报局长/钱包管家 | Schedule 节点，每天 09:00 | 定时自动运行 | 可按需调整时间 |
| 触发器-福利官 | Webhook 节点，URL 填入飞书按钮 | 点击飞书按钮即触发领券 | Webhook URL 需复制到飞书自动化消息卡片中 |
| Code 节点 | 见下方完整代码 | 清洗 AI 输出为干净 JSON | 必须放在 Agent 节点之后、Feishu 节点之前 |
| 飞书节点-Operation | 新增记录 | 写入一条新数据 | — |
| 飞书节点-数据映射 | 开启 Raw JSON 模式 | 避免字段格式报错 | 字符串变量必须用 `JSON.stringify()` 包裹 |
| 飞书表字段-图片/链接 | 选「文本类型」 | 正常写入 URL | 选「超链接类型」会导致写入报错 |
| 飞书应用权限 | 开启 `bitable:app:read` + `bitable:record:create` | 机器人有读写权限 | 开权限后必须发布新版本才生效 |
| 飞书表格添加应用 | 多维表格右上角 → 添加应用 | 机器人能写入该表 | 90% 的人会忘记这一步 |

---

### 🛠️ 操作流程

**1. 准备阶段：获取 MCP Token**
1. 浏览器访问 `open.mcd.cn`
2. 点击右上角「登录」，手机号验证码登录
3. 登录后点击「控制台」
4. 弹窗中点击「激活」
5. 勾选同意服务协议
6. 复制屏幕上出现的 MCP Token，粘贴至记事本备用

**2. 飞书多维表格搭建：新建「麦麦福利小助手」**

新建三张表，字段类型严格按下表配置：

| 表名 | 字段名 | 字段类型 |
|---|---|---|
| 优惠日历 | 活动日期 | 文本 |
| 优惠日历 | 活动标题 | 文本 |
| 优惠日历 | 活动内容 | 文本 |
| 优惠日历 | 原始图片链接 | 文本（⚠️ 不能选超链接） |
| 我的卡包 | 优惠券名称 | 文本 |
| 我的卡包 | 优惠价格 | 货币 |
| 我的卡包 | 当前状态 | 文本 |
| 我的卡包 | 优惠券图片 | 文本（⚠️ 不能选超链接） |
| 我的卡包 | 开始时间 | 文本 |
| 我的卡包 | 结束时间 | 文本 |
| 领券记录 | 执行时间 | 文本 |
| 领券记录 | 执行结果摘要 | 文本 |
| 领券记录 | 获得的券 | 文本 |
| 领券记录 | 成功数量 | 数字 |
| 领券记录 | 失败数量 | 数字 |

**3. 飞书开放平台：创建企业自建应用**
1. 登录飞书开放平台 → 创建企业自建应用
2. 在「凭证与基础信息」复制 App ID 和 App Secret
3. 在「权限管理」搜索并开启 `bitable:app:read` 和 `bitable:record:create`
4. 在「版本管理与发布」创建新版本并发布（⚠️ 必做，否则权限不生效）
5. 打开多维表格，右上角「添加应用」，添加刚创建的机器人（⚠️ 必做）

**4. n8n 工作流搭建：三条流水线**

每条流水线结构相同：`Trigger → Agent → Code → Feishu`

**Step 4.1 Agent 节点配置**
- 添加 AI Agent 节点
- Model：连接 DeepSeek
- Tools：添加 MCP Client，配置如下：
  - Name: `Authorization`
  - Value: `Bearer [你的Token]`（Bearer 后有空格）
  - Server URL: `https://mcp.mcd.cn/mcp-servers/mcd-mcp`
  - Type: `HTTP Server SSE`
- Prompt：按场景填入下方对应提示词

**Step 4.2 Code 节点（三条流水线通用）**

```javascript
const aiOutput = items[0].json.output || $node["Agent"].json.output;

function robustParse(input) {
    if (typeof input === 'object' && input !== null) return input;
    
    let str = String(input).trim();
    // 1. 去除 Markdown 代码块标记
    str = str.replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/\s*```$/, '');
    
    // 2. 尝试标准解析
    try { return JSON.parse(str); } catch (e) {}
    
    // 3. 修复被截断的 JSON 数组
    if (str.startsWith('[') && !str.endsWith(']')) {
        for (let i = str.length - 1; i >= 0; i--) {
            if (str[i] === '}') {
                const potentialJson = str.substring(0, i + 1) + ']';
                try {
                    const res = JSON.parse(potentialJson);
                    if (Array.isArray(res) && res.length > 0) return res;
                } catch (e) {}
            }
        }
    }
    
    // 4. JS 引擎执行
    try { return (new Function("return (" + str + ");"))(); } catch (e) {}
    
    // 5. 文本兜底：不以 { 或 [ 开头，封装为对象
    if (!str.startsWith('{') && !str.startsWith('[')) {
        return { "text_content": str };
    }

    return null;
}

try {
    if (!aiOutput) throw new Error("AI 没有返回 output 字段");
    
    const parsedData = robustParse(aiOutput);
    
    if (!parsedData) {
        const preview = aiOutput.length > 100 ? aiOutput.slice(0, 100) + "..." : aiOutput;
        throw new Error(`解析彻底失败，原始内容: ${preview}`);
    }

    const resultItems = Array.isArray(parsedData) ? parsedData : [parsedData];
    return resultItems.map(item => ({ json: item }));

} catch (error) {
    throw new Error(`JSON解析错误: ${error.message}`);
}
```

**Step 4.3 Feishu 节点配置**
- Operation：新增记录
- 开启 Raw JSON 模式
- App Token：浏览器链接中 `base/` 后的字符串（如 `bascnXXXXXXXX`）
- Table ID：链接中 `table=` 后的字符串（如 `tblXXXXXXXX`）
- Raw JSON 写法示例（以领券记录为例）：

```json
{
  "fields": {
    "执行时间": {{ $json["执行时间"] ? JSON.stringify($json["执行时间"]) : 'null' }},
    "执行结果摘要": {{ $json["执行结果摘要"] ? JSON.stringify($json["执行结果摘要"]) : 'null' }},
    "获得的券": {{ $json["获得的券"] ? JSON.stringify($json["获得的券"]) : 'null' }}
  }
}
```

**5. 飞书原生自动化配置**

**A. 每日活动推送（09:00）**
- 触发器：到达记录中的时间时 → 数据表「优惠日历」→ 时间字段「活动日期」→ 09:00
- 操作：发送站内信消息
- 消息内容：
```
☀️ 早安！今日麦麦福利情报：
🍟 {活动标题}
📝 {活动内容}
👉 点击查看海报: {原始图片链接}
```

**B. 未领券提醒 + 一键领取（17:20）**
- 触发器：定时触发 → 17:20 → 每天重复
- 操作1：查找记录 → 数据表「我的卡包」→ 筛选「当前状态 等于 未领取」
- 操作2（循环内）：发送消息卡片
- 消息内容：
```
⏰ 羊毛预警！这张券你还没领：
🎫 {优惠券名称}
💰 价值: {优惠价格} 元
👇 猛戳下方链接一键领取：
{n8n Webhook URL}
```

---

### 💡 具体案例/数据

**场景A Prompt — 麦麦情报局长（查活动日历）**

```
**角色设定**: 你是麦当劳总部的"麦麦情报局长"，负责掌握所有最新的营销活动信息。你的说话风格专业、热情，带有麦当劳特色（喜欢用🍟、🍔等emoji）。

**核心任务**:
1. **日期检查**: 首先必须调用 `now-time-info` 工具获取当前日期。
2. **判断逻辑**: 
   - 如果当前日期是每月 **1号**，或者用户明确要求"强制更新活动"，则调用 `campaign-calender` 获取活动日历。
   - 如果不是1号，且用户未强制要求，则**不调用**活动日历工具，直接返回空数组 `[]`。
3. **数据处理**: 
   - 将获取到的活动信息整理为 JSON 格式。
   - 必须包含字段: `活动日期`, `活动标题`, `活动内容`, `原始图片链接`。
   - **活动内容**: 必须生成为一段紧凑文本，严禁换行，模仿朋友圈/小红书文案风格，使用 Emoji 分割关键点。
   - 格式参考: "💥开年💥劲爆💥事件！㊙️某神秘巨星天团🛫空降常驻随心配1+1🌟「鱼酷玉咖牛」五大巨星🙋个个都是美味&品质担当👀连带着随心配也全面焕新💘红白配变蓝粉配，超养眼🔍记得来麦一探究竟！"
4. **输出要求**:
   - 仅输出纯 JSON 数组，不要包含 Markdown 代码块标记，也不要任何解释性文字。
   - 格式示例: `[{"活动日期": "...", "活动标题": "...", "活动内容": "💥开年...", "原始图片链接": "..."}]`
```

**场景B Prompt — 麦麦钱包管家（查优惠券）**

```
**角色设定**: 你是用户的贴身"麦麦钱包管家"，精打细算，帮你管理每一张优惠券和每一个积分。

**核心任务**:
1. **信息同步**: 调用 `now-time-info` 获取当前时间。
2. **资产盘点**: 调用 `my-coupons` 获取用户当前拥有的优惠券。
3. **数据整合**:
   - 将券包信息整理为 JSON 格式。
   - 必须包含字段: `优惠券名称`, `优惠价格`（数字）, `当前状态`（已领取/待使用）, `优惠券图片`, `开始时间`, `结束时间`。
   - `优惠券图片` 字段填入该优惠券的图片链接 URL。
4. **输出要求**: 仅输出纯 JSON 数组，无 Markdown。
```

**场景C Prompt — 麦麦福利官（领券）**

```
**角色设定**: 你是行动力超强的"麦麦福利官"，收到指令后立即执行领券操作。

**核心任务**:
1. **执行领券**: 
   - 直接调用 `auto-bind-coupons` 工具。
   - 该工具会自动领取所有当前可用的优惠券，**无需任何入参**（不需要 couponId）。
   - 即使接收到参数，也请忽略，直接执行全量领取。
2. **结果反馈**: 调用 `now-time-info` 记录执行时间，输出领券结果。
3. **输出要求**:
   - 必须输出符合飞书表格要求的 JSON 对象，包含以下五个字段:
     - `执行时间`: 使用 `now-time-info` 获取的时间
     - `执行结果摘要`: 例如 "✅ 成功领取 2 张优惠券" 或 "⚠️ 暂无新券可领"
     - `获得的券`: 详细列出领到的券名称（多个用逗号分隔）
     - `成功数量`: 数字，成功领取的优惠券数量
     - `失败数量`: 数字，领取失败的优惠券数量
   - 严禁输出 Markdown 代码块，只输出纯 JSON 字符串。
   - 格式示例: `{"执行时间": "2026-01-12 10:00:00", "执行结果摘要": "✅ 领券成功", "获得的券": "麦辣鸡腿堡买一送一, 薯条(中)免费", "成功数量": 2, "失败数量": 0}`
```

---

### 📝 避坑指南

- ⚠️ MCP Client 的 `Authorization` Value 中，`Bearer` 和 Token 之间必须有一个空格，格式为 `Bearer eyJhbGci...`，少了空格鉴权直接失败
- ⚠️ 飞书表格中所有存放 URL 的字段（原始图片链接、优惠券图片）必须选「文本类型」，选「超链接类型」写入必报错
- ⚠️ 飞书开放平台开通权限后，必须在「版本管理与发布」创建并发布新版本，否则权限不生效
- ⚠️ 多维表格右上角必须手动「添加应用」，将机器人加入该表，否则 n8n 写入时会报权限错误（高频遗漏步骤）
- ⚠️ Feishu 节点的 Raw JSON 中，所有字符串类型变量必须用 `JSON.stringify()` 包裹，否则飞书返回 `Unexpected token` 错误
- ⚠️ `auto-bind-coupons` 工具不需要传 couponId，Prompt 中必须明确告知 Agent 忽略任何入参，否则 Agent 可能自行构造错误参数导致领券失败
- ⚠️ Code 节点不可省略，即使 Prompt 已要求输出纯 JSON，AI 仍有概率输出带 Markdown 标记或截断的内容，跳过 Code 节点直接写入飞书必报错

---

### 🏷️ 行业标签
#飞书多维表格 #MCP #n8n #自动化工作流 #AI落地实战 #薅羊毛 #DeepSeek #低代码

---

---
