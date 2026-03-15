# 工作流自动化

## 25. [2026-04-22]

## 📗 文章 2


> 文档 ID: `O4lRw9ouaiJGQkkmOHEck7dJnQW`

**来源**: 扣子Coze接入豆包1.5深度思考模型保姆级教程（个人版可用） | **时间**: 2025-04-21 | **原文链接**: `https://mp.weixin.qq.com/s/d54Mz3v6...`

---

### 📋 核心分析

**战略价值**: 扣子个人版无法通过自定义推理接入点使用方舟模型，本文提供「HTTP请求节点 + 代码节点」两步绕过方案，适用于火山引擎上所有大模型。

**核心逻辑**:

- 扣子个人进阶版不支持「自定义推理接入点」推送方舟模型到大模型节点，只有团队版/企业版才支持，必须用 HTTP 请求节点替代
- 豆包1.5深度思考模型（Doubao-1.5-thinking-pro）在数学、编程、科学领域表现优于 DeepSeek-R1，速度更快，且支持图片的多模态深度思考
- 整个工作流只需两个有效节点：【HTTP请求】+ 【代码】，结构极简
- API Endpoint 为 `https://ark.cn-beijing.volces.com/api/v3/chat/completions`，模型 ID 为 `doubao-1-5-thinking-pro-250415`
- 鉴权方式为 Header：`Authorization: Bearer <API_KEY>`，API KEY 从火山方舟模型广场「快速接入测试」页面获取
- HTTP 请求节点返回的 body 是字符串而非对象，必须用代码节点 `JSON.parse` 解析后才能结构化使用
- 返回结构中有用字段只有两个：`choices[0].message.content`（最终回答）和 `choices[0].message.reasoning_content`（思考过程）
- 代码节点输入变量引用 HTTP 节点的 `body`，输出变量 `message` 类型为 Object，子项为 `content` 和 `reasoning_content`
- 该接入方式通用于火山引擎上所有大模型，只需替换 model ID 即可复用
- DeepSearch 是火山方舟另一产品，集成联网搜索、知识库、网页解析、Python 代码执行器等 MCP 服务，入口在应用广场：`https://console.volcengine.com/ark/region:ark+cn-beijing/application`

---

### 🛠️ 操作流程

**1. 准备阶段 — 获取 API KEY 和模型 ID**

1. 进入火山方舟模型广场：`https://console.volcengine.com/ark/region:ark+cn-beijing/model?vendor=Bytedance&view=LIST_VIEW`
2. 搜索并选择 `Doubao-1.5-thinking-pro`
3. 点击右上角【模型推理】→ 打开【快速接入测试】
4. 第一步获取 API KEY，记录备用
5. 第二步查看 API 调用示例，确认模型 ID 为 `doubao-1-5-thinking-pro-250415`

---

**2. 核心执行 — 配置 HTTP 请求节点**

| 字段 | 填写内容 |
|------|---------|
| 请求方式 | POST |
| URL | `https://ark.cn-beijing.volces.com/api/v3/chat/completions` |
| 请求头 Key | `Authorization` |
| 请求头 Value | `Bearer 你的API_KEY` |
| 请求体格式 | JSON |
| 请求体内容 | 见下方代码块 |

请求体 JSON：
```json
{
  "model": "doubao-1-5-thinking-pro-250415",
  "messages": [
    {
      "content": [
        {
          "text": "{{block_output_100001.input}}",
          "type": "text"
        }
      ],
      "role": "user"
    }
  ]
}
```

> `text` 字段的值通过花括号 `{` 呼出参数选择器，选择开始节点的输入参数 `input`（即 `{{block_output_100001.input}}`）

---

**3. 验证与优化 — 配置代码节点解析返回值**

HTTP 节点返回的 `body` 是一个 JSON 字符串，需新增代码节点处理：

- 输入变量：引用 HTTP 请求节点返回的 `body` 参数，命名为 `input`
- 输出变量：`message`，类型选 Object，新增子项 `content`（String）、`reasoning_content`（String）

代码节点代码：
```typescript
async function main({ params }: Args): Promise<Output> {
  let obj = JSON.parse(params.input)
  const ret = {
    "message": obj.choices[0].message
  };
  return ret;
}
```

完成后整体运行工作流，验证 `message.content` 和 `message.reasoning_content` 均有返回即接入成功。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| HTTP 请求节点 | POST + URL + Authorization Header + JSON Body | 调用豆包1.5深度思考模型并返回原始响应 | body 返回的是字符串，不是对象，不能直接取字段 |
| 代码节点 | `JSON.parse(params.input)` + 取 `choices[0].message` | 结构化输出 content 和 reasoning_content | 输出变量类型必须选 Object，并手动添加子项 |
| 模型 ID | `doubao-1-5-thinking-pro-250415` | 指定豆包1.5深度思考模型 | 替换此 ID 可复用整套流程接入方舟其他模型 |
| API KEY | 从火山方舟「快速接入测试」页面获取 | 鉴权通过 | 放在 Header 中，格式必须是 `Bearer <KEY>`，注意空格 |
| DeepSearch 入口 | `https://console.volcengine.com/ark/region:ark+cn-beijing/application` | 体验集成 MCP 服务的深度搜索应用 | 支持自定义 MCP 服务配置和问题拆解层数 |

---

### 📝 避坑指南

- ⚠️ 个人进阶版扣子无法用「自定义推理接入点」接入方舟模型，必须用 HTTP 请求节点方案，不要在设置里找那个入口浪费时间
- ⚠️ HTTP 节点返回的 `body` 是字符串类型，直接引用无法取到 `choices`，必须先 `JSON.parse`
- ⚠️ 代码节点输出变量 `message` 类型必须选 Object 并手动添加 `content`、`reasoning_content` 两个子项，否则下游节点无法引用
- ⚠️ 请求体中 `text` 字段的动态参数通过 `{` 花括号触发选择器，不要手动硬编码用户输入

---

### 🏷️ 行业标签

#扣子Coze #豆包1.5 #火山方舟 #AI工作流 #HTTP节点 #个人版适用 #DeepSearch #MCP

---

---
