# AI编程与开发工具

## 51. [2026-04-22]

## 📙 文章 4


> 文档 ID: `WzPUwlaS5i05iTkbxWkcb5H7nxh`

**来源**: 体验后惊呼牛逼！字节AI编程工具Trae更新重磅功能，一句话调用多MCP完成超复杂工作流，完全免费！ | **时间**: 2025-04-22 | **原文链接**: `https://mp.weixin.qq.com/s/m8AB9qsr...`

---

### 📋 核心分析

**战略价值**: Trae 国内版正式支持 MCP + 智能体，成为首个支持 MCP 的国产 AI IDE，完全免费，可用一句话驱动多 MCP 串联完成复杂自动化工作流。

**核心逻辑**:

- **Trae 双版本定位**：国内版内置 Deepseek R1/V3/v3-0324 + Doubao 1.5 Pro；海外版内置 Claude 3.5/3.7 Sonnet、Gemini 2.5 Pro、GPT-4o/4.1，均支持自定义模型，且完全免费。
- **MCP 安装入口**：右上角设置图标 → MCP → 添加，进入 MCP 应用市场。带"轻松配置"标签的 MCP 只需填 Token 即可完成安装，其余需手动粘贴 JSON 配置。
- **第三方 MCP 市场备选**：官方市场找不到时，可去 `https://mcp.so/`、`https://smithery.ai/`、`https://www.pulsemcp.com/`、`https://mcps.live/` 手动配置。
- **MCP 手动配置标准格式**：从第三方市场复制 JSON → 替换 API Key 及本地路径 → 粘贴到 Trae「手动配置」。以 Minimax 为例（见下方配置详表）。
- **智能体机制**：类似字节 Coze，选定一组 MCP 工具 + 写入 Prompt 定义工作流，之后只需 `@智能体名称` + 自然语言指令，AI 自动串联所有 MCP 完成任务，无需人工干预中间步骤。
- **上下文强化**：新增联网搜索、文档集（支持 URL 或本地上传）。可直接丢 GitHub 仓库 URL 让 AI 读代码再写代码，极大降低陌生技术栈的上手成本。
- **Rules 功能上线**：类似给 AI 定"工作手册"，将命名规范、接口规范等写入 Rules，可有效减少函数名/接口名不一致的低级错误，提升一次运行成功率。
- **智能体 Prompt 设计要点**：步骤要编号、每步明确调用哪个 MCP、指定输出格式（文件名、文件夹结构、音频命名等），AI 会严格按顺序执行。
- **MarsCode 更名**：原 MarsCode 编程助手更名为「Trae 插件」，支持 Builder 模式，可与 Trae IDE 结合使用。
- **七牛云 MCP 开源**：作者已用 AI 写了七牛云 MCP，支持自然语言控制上传音频/图片/网页，已开源：`https://github.com/joeseesun/qiniu-mcp-joe`

---

### 🎯 关键洞察

**为什么「智能体 + MCP」比直接调用 MCP 更优？**

直接在对话中调用多个 MCP，AI 容易在步骤间丢失上下文、调用顺序混乱。智能体把工作流固化在 Prompt 里，每次 `@` 唤起时 AI 拿到的是完整的执行蓝图，而不是临时拼凑的指令链。结果是：稳定性更高、可复用、用户只需关心输入和最终输出。

**为什么 MCP 普及难？**

安装门槛是核心障碍——大多数 MCP 需要用户理解 JSON 配置、uvx 命令、API Key 管理。Trae 的「轻松配置」标签方向正确，但覆盖的 MCP 数量还有限。真正普及的临界点是：用户完全不需要知道 MCP 是什么，一键安装，只看结果。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| Minimax MCP | 见下方代码块 | 文本转语音，生成 MP3 | 需充值付费；`MINIMAX_MCP_BASE_PATH` 必须填本地绝对路径 |
| Fetch MCP | `{"mcpServers":{"fetch":{"command":"uvx","args":["mcp-server-fetch"]}}}` | 抓取网页内容转 Markdown | 免费；部分反爬网站可能失败 |
| Filesystem MCP | 标准配置，无需额外参数 | 读写本地文件、创建文件夹 | 免费；注意路径权限 |
| EdgeOne Pages MCP | 官方市场直接添加 | 部署网页到腾讯服务器，返回临时 URL | 免费；URL 为临时地址 |
| Amap Maps MCP | 申请高德 API Key 后配置 | 查餐厅、咖啡厅、交通路线 | 申请 API 免费用 |
| Sequential Thinking | 官方市场直接添加 | 将复杂任务分解为顺序步骤执行 | 免费；适合多步骤推理任务 |
| Firecrawl MCP | 申请 Key 后配置 | 内容搜索+抓取 | 有免费额度；类似工具：Brave Search、Tavily |
| Puppeteer MCP | 标准配置 | 自动化控制 Chrome，模拟真人操作 | 免费；类似工具：微软 Playwright |
| 七牛云 MCP | `https://github.com/joeseesun/qiniu-mcp-joe` | 自然语言控制上传音频/图片/网页 | 开源；需配置七牛云 API |

**Minimax MCP 完整配置代码**：
```json
{
  "mcpServers": {
    "MiniMax": {
      "command": "uvx",
      "args": [
        "minimax-mcp"
      ],
      "env": {
        "MINIMAX_API_KEY": "你的API key",
        "MINIMAX_MCP_BASE_PATH": "本地存储位置，如/Users/[你的用户名]/Desktop",
        "MINIMAX_API_HOST": "https://api.minimax.chat",
        "MINIMAX_API_RESOURCE_MODE": "local"
      }
    }
  }
}
```

---

### 🛠️ 操作流程：搭建「英语学习网页生成」智能体

**1. 准备阶段**
- 安装以下 4 个 MCP：Fetch、Filesystem、Minimax、EdgeOne（可选）
- Minimax 需充值并获取 API Key，填入上方配置
- 确认 `MINIMAX_MCP_BASE_PATH` 路径存在且有写入权限

**2. 创建智能体**
- Trae 中新建智能体，命名为「网页生成」
- 勾选已安装的 MCP：Fetch、Filesystem、Minimax（+ EdgeOne 可选）
- 输入以下 Prompt：

```
1. 调用fetch，根据用户提供的网址，抓取主题内容。内容翻译成中英双语，提取CET4以上单词10个以内，解释并造句。写入一个md文件，名字根据网页取，可读性高。
2. 调用filesystem，根据抓取的文件名内容创建一个文件夹，移动md到这里，后续生成文件都放这里。
4. 调用MiniMax MCP把md文档用美式英语少女声音生成语音，下载mp3文件并改名为audio.mp3，存上面创建的文件夹中。
5. 把以上生成的音频和MD文档，制作成一个漂亮的响应式单页HTML，存上面创建的文件夹中。
```

**3. 使用智能体**
- 在 Trae 对话框输入 `@网页生成`，然后直接给 URL：
```
处理 https://www.fridayflashfiction.com/100-word-stories/say-a-little-prayer-by-gordon-lawrie
```
- 等待 AI 自动完成：网页抓取 → 中英双语 + 词汇提取 → MP3 生成 → HTML 网页生成
- 打开生成的 HTML，即可边听英语朗读边阅读双语对照内容

---

### 💡 具体案例/数据

- 测试 URL：`https://www.fridayflashfiction.com/100-word-stories/say-a-little-prayer-by-gordon-lawrie`（100词英语短篇小说）
- 执行顺序：Fetch MCP 抓取 → 中英双语转换 + CET4词汇提取 → Minimax 生成美式英语少女声 MP3（命名为 audio.mp3）→ 生成包含音频播放器的响应式 HTML 单页
- 全程零人工干预，一句指令完成 4 步跨工具工作流

---

### 📝 避坑指南

- ⚠️ `MINIMAX_MCP_BASE_PATH` 必须填写绝对路径（如 `/Users/yourname/Desktop`），填相对路径会导致文件保存失败
- ⚠️ 非「轻松配置」标签的 MCP 需要手动粘贴 JSON，注意 JSON 格式不能有多余逗号或缺少括号，否则配置不生效
- ⚠️ 智能体 Prompt 中步骤编号不连续（原文 1、2、4、5 跳过了 3）不影响执行，但建议自己写时保持连续，避免 AI 误判
- ⚠️ Fetch MCP 对有反爬机制的网站效果差，可换 Firecrawl 或 Puppeteer
- ⚠️ EdgeOne Pages 返回的是临时 URL，不适合长期分享，仅用于快速预览

---

### 🏷️ 行业标签

#Trae #MCP #AI编程 #字节跳动 #智能体 #AIWorkflow #国产AIIDE #Minimax #免费工具

---

---
