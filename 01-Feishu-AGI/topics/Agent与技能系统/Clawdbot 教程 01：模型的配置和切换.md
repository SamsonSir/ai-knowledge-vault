# Agent与技能系统

## 42. [2026-01-31]

## 📙 文章 4


> 文档 ID: `GycBwU1RxiSYjYkYEaOcWgHhnCb`

**来源**: Clawdbot 教程 01：模型的配置和切换 | **时间**: 2026-02-01 | **原文链接**: `https://mp.weixin.qq.com/s/qlbCkX2P...`

---

### 📋 核心分析

**战略价值**: Clawdbot（openclaw）配置国产模型时的两大核心坑点——命令行配置顺序 + 国内外 URL 区分，以及 `no output` 误判问题的完整排查路径。

**核心逻辑**:

- **优先用 `openclaw configure` 命令**，而非手动改文件，能解决 80% 的配置问题，直接在终端执行即可进入交互式引导。
- **交互式引导三问**：① 本地还是远程 → 选本地；② 配置什么 → 选模型；③ 输入 API Key。
- **模型选择映射关系**：Minimax M2.1 → 选 `Minimax`；Kimi K2.5 → 选 `moonshot AI`。不能按产品名直觉选，必须按平台归属选。
- **Coding Plan 选项的坑**：Kimi 有专属 `coding plan` 选项可直接选；Minimax 没有 coding plan 选项，即使购买了 coding plan 会员，也只能选 `Minimax` 本身。
- **国内外版本区分是最大坑**：Minimax 分 `minimax-cn`（国内）和 `minimax`（海外），选错直接导致配置失败，必须按购买渠道对应选择。
- **选项列表操作技巧**：弹出亚马逊、谷歌等一大堆选项时，不要慌，用方向键往下拉，找到左侧已高亮的那个选项（如 Minimax 或 Kimi coding），直接回车确认。
- **手动改配置文件兜底**：`openclaw configure` 无效或选错国内外版本时，直接编辑 `/Users/你的用户名/.openclaw/openclaw.json`，定位 `baseURL` 字段手动修正。
- **URL 修正对照**（以 Minimax 为例）：国内版 `api.minimax.com`，海外版 `api.minimax.io`，后缀 `.com` vs `.io` 一字之差导致全部失败，其他模型同理去官方文档查正确 URL。
- **`fallbacks` 字段必须同步更新**：`openclaw.json` 中 `agents` 里的 `fallbacks` 字段，切换模型后必须在此处也写入新模型，否则切换不生效。
- **`no output` 不等于配置失败**：返回 `no output` 的含义是"输出在其他环境"（如 Web 端 claude.ai、Telegram bot 等），不是报错。看到此提示应去其他已配置的环境验证，能用则说明配置成功，只是输出路由问题。

---

### 🎯 关键洞察

`no output` 是最容易误判的坑：用户输入"你好"后收到 `no output`，直觉反应是配置失败，实际上是 openclaw 的多环境输出路由机制——响应被路由到了其他已绑定的环境（Web/Telegram 等）。排查顺序应是：先去其他环境确认输出 → 再怀疑配置问题，而不是反过来。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 交互式配置 | `openclaw configure` | 引导式完成模型+API Key 配置 | 优先用此方法，覆盖大部分场景 |
| TUI 启动 | `openclaw tui` | 进入终端 UI 界面 | 切换模型前先用 `/new` 开新窗口 |
| 模型切换 | TUI 内输入 `/model`，搜索模型名 | 实时切换当前使用模型 | 切换前先 `/new`，避免上下文污染 |
| 配置文件路径 | `/Users/你的用户名/.openclaw/openclaw.json` | 手动修正 baseURL 等参数 | `configure` 失败时的兜底方案 |
| baseURL 字段 | `"baseURL": "api.minimax.com"` 或 `"api.minimax.io"` | 指定模型 API 入口 | 国内/海外后缀不同，错了必报错 |
| fallbacks 字段 | `agents` → `fallbacks` 内写入目标模型 | 模型切换真正生效 | 此处未更新则切换无效 |
| Kimi 模型选择 | moonshot AI → Kimi for coding | 配置 Kimi K2.5 | 有专属 coding plan 选项可直选 |
| Minimax 模型选择 | Minimax → minimax-cn（国内）/ minimax（海外） | 配置 Minimax M2.1 | 无 coding plan 选项，按购买渠道选 cn 或不带 cn |

---

### 🛠️ 操作流程

1. **准备阶段**: 确认购买的是国内还是海外版 API/会员，准备好对应的 API Key。

2. **核心执行**:
   - 终端执行 `openclaw configure`
   - 选「本地」→「模型」→ 按模型归属选平台（Kimi → moonshot AI；Minimax → Minimax）
   - 输入 API Key
   - 在选项列表中用方向键找到已高亮项，回车确认
   - 若 configure 失败，打开 `/Users/你的用户名/.openclaw/openclaw.json`，手动修正 `baseURL` 和 `agents.fallbacks` 字段

3. **验证与优化**:
   - 执行 `openclaw tui` 进入 TUI
   - 先输入 `/new` 开新窗口
   - 输入 `/model`，搜索目标模型名（如 "Kimi"），选第一个结果回车
   - 发送测试消息，若返回 `no output`，去 Web 端或 Telegram 等其他环境验证输出是否正常

---

### 💡 具体案例/数据

作者实测三个国产模型均配置成功并正常工作：
- Kimi K2.5 → 国内版（moonshot AI → Kimi for coding）
- Minimax M2.1 → 海外版（Minimax → minimax，baseURL: `api.minimax.io`）
- GLM → 海外版

---

### 📝 避坑指南

- ⚠️ Minimax 没有 coding plan 专属选项，买了 coding plan 也只能选 `Minimax` 本身，不要找不到就乱选其他平台。
- ⚠️ 国内版 URL 后缀 `.com`，海外版 `.io`，配置完不能用先检查这一项，是最高频失败原因。
- ⚠️ `openclaw.json` 里 `agents.fallbacks` 必须同步写入新模型，否则 `/model` 切换后实际不生效。
- ⚠️ 看到 `no output` 不要立刻重新配置，先去其他环境（Web/Telegram）验证，避免重复折腾。
- ⚠️ 切换模型前务必先 `/new` 开新窗口，直接在旧会话切换容易出现异常。

---

### 🏷️ 行业标签

#Clawdbot #openclaw #国产模型接入 #Kimi #Minimax #GLM #API配置 #模型切换

---

---
