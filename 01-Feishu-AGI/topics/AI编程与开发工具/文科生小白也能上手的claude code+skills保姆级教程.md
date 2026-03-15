# AI编程与开发工具

## 17. [2026-02-02]

## 📙 文章 4


> 文档 ID: `WEYNw8KL3iPTeGk9vqwcPqMAnIg`

**来源**: 文科生小白也能上手的claude code+skills保姆级教程 | **时间**: 2026-01-28 | **原文链接**: `https://mp.weixin.qq.com/s/TxQZca1m...`

---

### 📋 核心分析

**战略价值**: 非程序员从零完成 Claude Code + Skills 的完整安装配置，并掌握 Skills 的调用与可视化使用方式。

**核心逻辑**:

- **Claude Code ≠ 写代码工具**：它是能读取本地文件、调用工具、自主执行任务的 AI 智能体，覆盖文档整理、PPT 制作、OKR 规划、录屏教程等非编程场景。
- **对比 ChatGPT 的核心差异**：网页版 AI 每次对话都是"白板"，需手动上传上下文；Claude Code 直接读取本地文件，能主动找到你的 OKR 文件并基于它给建议。
- **Skills = 给 AI 的 SOP**：解决的是"每次任务质量不稳定"的问题，把最佳执行流程固化下来，防止 AI 自由发挥导致质量下降。
- **Skills vs 传统工作流（Dify/n8n/扣子）**：传统工作流门槛高、遇错即崩、需要人工串联节点；Skills 内置容错能力，AI 遇到问题会自动换方式，无需人工干预。
- **MCP 与 Skills 的关系**：MCP 是"工具接口"（解决 AI 用什么工具的问题），Skills 是"流程框架"（解决 AI 怎么干活的问题），两者互补不冲突。
- **Skills 目录结构**：`skill.md`（核心，给 AI 看的操作手册）、`README.md`（给人看的说明书）、`reference/`（知识库/风格样本）、`examples/`（示例输出）、`scripts/`（可调用脚本工具箱）、`.clinerules`（高级规则配置）。最小可运行单元只需 `skill.md` 一个文件。
- **国内用户首选智谱 AI**：无需特殊网络、支持国内支付、有免费额度，且官方提供一键配置工具 `Coding Tool Helper`，适合小白。
- **安装顺序不能乱**：必须先装 Node.js → Windows 额外装 Git → 再装 Claude Code → 最后配置 API Key，顺序错误会导致报错。
- **遇到报错的万能解法**：复制错误信息 + 系统类型（Mac/Windows）+ 当前操作步骤，发给任意 AI 让它指导，不需要自己看懂报错。
- **可视化界面是小白必备**：纯命令行看不到文件变化，配合 Trae/Cursor/VS Code 的内置终端使用，可直观看到 AI 修改了哪些文件。

---

### 🛠️ 操作流程

#### 第一步：安装 Node.js

**Mac 用户（Homebrew 方式）**

```bash
# 检查是否已有 Homebrew
brew --version

# 没有则先安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js
brew install node
```

**Windows 用户**

1. 访问 `https://nodejs.org/` 下载 LTS 版本（`.msi` 文件）
2. 双击安装，确保勾选 "Add to PATH"，其余一路 Next
3. 额外安装 Git：访问 `https://git-scm.com/download/win`，下载后一路 Next 默认安装

**验证安装（关闭终端重新打开后执行）**

```bash
node --version   # 应显示 v20.x.x
git --version    # Windows 用户验证 Git，应显示 git version 2.x.x
```

---

#### 第二步：安装 Claude Code

官方文档：`https://docs.anthropic.com/en/docs/claude-code`

```bash
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
```

等待 1-3 分钟，安装完成后验证：

```bash
claude --version   # 显示版本号即成功
```

---

#### 第三步：获取智谱 AI API Key

1. 注册：`https://open.bigmodel.cn/`，手机号注册后完成实名认证
2. 套餐选择：GLM Coding Pro 连续包年（性价比最高），购买链接：`https://www.bigmodel.cn/glm-coding?ic=IQKEJG5NOT`
3. 创建 API Key：控制台 → "API 管理" → "创建新的 API Key" → 命名（如"Claude Code 专用"）→ 立即复制保存

---

#### 第四步：配置 Claude Code（三选一）

**方法一：一键自动配置（强烈推荐）**

```bash
npx @z_ai/coding-helper
```

按提示输入 Y 回车，粘贴 API Key，自动完成配置 + MCP 安装。详细文档：`https://docs.bigmodel.cn/cn/guide/develop/claude`

---

**方法二：手动修改配置文件（备选）**

文件位置：
- Mac/Linux：`~/.claude/settings.json`
- Windows：`C:\Users\你的用户名\.claude\settings.json`

打开方式（Mac）：
```bash
open ~/.claude/settings.json
```

写入内容（替换 `your_zhipu_api_key` 为真实 Key）：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your_zhipu_api_key",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1
  }
}
```

再修改 `~/.claude.json`（Mac）或 `C:\Users\你的用户名\.claude.json`（Windows）：

```json
{
  "hasCompletedOnboarding": true
}
```

`hasCompletedOnboarding: true` 的作用是跳过首次启动引导流程，直接使用智谱 AI 配置。

---

**方法三：环境变量配置（熟悉终端的用户）**

Mac/Linux：
```bash
export ANTHROPIC_API_KEY="your-zhipu-api-key-here"
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
```

永久生效：将上面两行加入 `~/.zshrc` 或 `~/.bash_profile`

Windows：右键"此电脑" → 属性 → 高级系统设置 → 环境变量 → 用户变量中新增：
- `ANTHROPIC_API_KEY` = 你的 API Key
- `ANTHROPIC_BASE_URL` = `https://open.bigmodel.cn/api/paas/v4`

---

#### 第五步：验证配置成功

```bash
claude
```

首次运行提示 "Do you want to use this API key" → 选 Yes；提示信任当前文件夹 → 选 Trust。

测试命令：
```bash
请帮我看一下当前目录下有哪些文件
```
或
```bash
你好，请做一个自我介绍
```

能正常回答即配置成功。

---

#### 第六步：安装和使用 Skills

**方法一：用 Skill Creator 创建自定义 Skills**

在 Claude Code 中发送：
```
请帮我安装这个 Skills：https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
```
按提示 yes/回车，引导式创建自己的 Skill。

**方法二：从市场安装现成 Skills**

访问 `https://skillsmp.com/`，找到目标 Skill，复制右侧安装命令，粘贴到终端回车执行，重启 Claude Code 即可使用。

**调用 Skills 的语法**：
```
请使用 【Skill名字】 来执行 【任务描述】
```

---

### 📦 配置/工具详表

| 模块 | 关键设置/地址 | 作用 | 注意事项 |
|------|------------|------|---------|
| Node.js | `https://nodejs.org/` 下载 LTS | Claude Code 运行环境 | Windows 必须勾选 Add to PATH |
| Git（仅 Windows） | `https://git-scm.com/download/win` | npm 安装复杂包时依赖 | 一路 Next 默认安装即可 |
| Claude Code | `npm install -g @anthropic-ai/claude-code` | 主程序 | 加 `--registry` 参数走国内镜像 |
| 智谱 AI | `https://open.bigmodel.cn/` | 国内可用的 API 服务 | 必须实名认证才能使用 |
| 一键配置工具 | `npx @z_ai/coding-helper` | 自动配置 API + MCP | 首选方案，失败再用手动方法 |
| `API_TIMEOUT_MS` | `3000000` | 防止长任务超时中断 | 手动配置时必填 |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | `1` | 禁用非必要流量 | 手动配置时建议加上 |
| `hasCompletedOnboarding` | `true` | 跳过首次引导 | 写在 `~/.claude.json`，不是 settings.json |
| Skill Creator | `https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md` | 引导式创建 Skill | 适合从零创建自定义流程 |
| Skills 市场 | `https://skillsmp.com/` | 搜索现成 Skills | 优先找适合自己任务的，不要贪多 |

---

### 🎯 关键洞察

**Skills 资源库汇总**：

| 来源 | 链接 | 特点 |
|------|------|------|
| Anthropic 官方仓库 | `https://github.com/anthropics/skills` | 源头，适合学习和修改 |
| awesome-claude-skills | `https://github.com/ComposioHQ/awesome-claude-skills` | 最全精选列表，分类清晰，更新频繁 |
| Claude 中文社区 | `https://claudecn.com/` | 中文教程 + 可直接下载的 Skills |
| Skills Marketplace | `https://skillsmp.com/` | 可搜索发现新 Skills |

**Skills 目录结构速查**：

| 文件/文件夹 | 给谁看 | 作用 | 是否必须 |
|------------|--------|------|---------|
| `skill.md` | AI | 操作手册，定义流程和每步执行方式 | ✅ 必须 |
| `README.md` | 人 | 安装说明、使用方法、注意事项 | 可选 |
| `reference/` | AI | 知识库，放风格样本、模板、标准文档 | 可选 |
| `examples/` | AI | 示例输出，告诉 AI 好结果长什么样 | 可选 |
| `scripts/` | AI 调用 | 工具箱，放自动化脚本 | 可选 |
| `.clinerules` | AI | 高级规则和限制配置 | 可选 |

---

### 📝 避坑指南

- ⚠️ **安装完 Node.js 或 Git 后，必须关闭终端重新打开**，否则 `node --version` 会报"找不到命令"。
- ⚠️ **Windows 用户跳过 Git 安装**：npm 安装 Claude Code 时大概率报错，必须先装 Git。
- ⚠️ **`settings.json` 和 `.claude.json` 是两个不同文件**：前者在 `~/.claude/` 文件夹内，后者在用户根目录 `~/`，不要搞混。
- ⚠️ **JSON 格式错误会导致配置失效**：手动编辑后用在线 JSON 校验工具检查格式，注意逗号、引号、括号。
- ⚠️ **不要贪多安装 Skills**：先装 2-3 个真正符合自己工作场景的，用熟再扩展，装太多反而乱。
- ⚠️ **遇到红色报错不要慌**：复制错误信息 + 系统类型 + 当前步骤，发给任意 AI 用以下模板提问：
  ```
  我是一个完全不懂编程的小白，我在【安装 Claude Code / 配置 API Key】的过程中遇到了这个错误：【错误信息】。我用的是 [Mac/Windows] 电脑。请用最简单的语言告诉我怎么解决，每一步要做什么。
  ```

---

### 🏷️ 行业标签

#ClaudeCode #Skills #MCP #AI智能体 #非程序员入门 #智谱AI #工作流自动化 #超级个体

---

---
