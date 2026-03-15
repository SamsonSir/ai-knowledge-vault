# Vibe_Coding实践

## 14. [2026-02-03]

## 📙 文章 4


> 文档 ID: `A3EcwvxyNiPf1FkQLxDcKajBnRd`

**来源**: Openclaw + OpenCode 才是 vibe coding 的最棒组合！ | **时间**: 2026-02-03 | **原文链接**: `https://mp.weixin.qq.com/s/U3PHOYSA...`

---

### 📋 核心分析

**战略价值**: 用 OpenClaw（AI Agent 平台）+ OpenCode（AI 编程助手）+ GitHub + Vercel，实现从自然语言需求到代码生成、版本管理、自动部署的全链路 Agent Coding 闭环，全程零手写代码、零手动命令。

**核心逻辑**:

- **工具链分工明确**：OpenClaw 是中控调度层（协调所有工具），OpenCode 是代码生成层，GitHub 是版本管理层，Vercel 是部署层，四者缺一不可。
- **OpenCode 有交互模式失效的坑**：作者实测 21:57 启动 OpenCode 交互模式后卡住，21:58 改用直接创建文件的方式绕过，最终仍在 ~1 分钟内完成代码生成。
- **贪吃蛇项目实测数据**：开发时间约 5 分钟，代码量约 400 行（HTML/CSS/JS），Vercel 部署耗时 < 10 秒，最终产物：`https://myopencode.vercel.app`。
- **GitHub Token 权限最小化原则**：只授予 repo 权限，防止 Agent 越权操作其他资源。
- **Vercel Token 同理**：按需授权，部署时通过 `vercel --token YOUR_VERCEL_TOKEN --yes --prod` 一条命令完成，无需登录 UI。
- **整个开发时间线仅 42 分钟**（21:49 开始安装 → 22:31 README 自动推送完毕），其中用户实际操作时间极短，绝大部分是 Agent 自主执行。
- **Agent 自生成文档能力**：OpenClaw 可在完成开发后，直接分析自身操作历史，生成包含流程图、代码示例、速查表的完整 README，并自动 push 到 GitHub，无需人工介入。
- **进阶能力已验证可行**：定时 cron 触发 Agent 更新内容、多 Agent 并行处理前后端、自动 PR 评论，均已有对应命令模板。
- **范式转变**：从 vibe coding（人辅助 AI 写代码）升级为 Agent Coding（人只提需求，Agent 全自主执行），用户角色从"写代码的人"变为"提需求的人"。
- **可扩展性**：该工作流不限于静态网站，支持 React、Vue、Next.js 等框架，只需修改 OpenCode 的自然语言指令即可。

---

### 🎯 关键洞察

**为什么 OpenClaw 是关键而不是 OpenCode？**

OpenCode 只是代码生成工具，本身无法调用 GitHub API、无法执行 shell、无法触发 Vercel 部署。OpenClaw 作为 Agent 运行平台，提供了工具调用能力（bash、pty、cron、多 Agent 并发），让 OpenCode 的输出能真正落地成可运行的系统。两者缺一不可：没有 OpenCode，代码生成靠人；没有 OpenClaw，代码生成了也无法自动部署。

**为什么交互模式卡住后要立刻切换方案？**

OpenCode 的 PTY 交互模式依赖终端 I/O，在某些服务器环境下会阻塞。作者的处理策略是：不等待、不调试，直接切换到"手动创建文件"备用方案，保持流程不中断。这是 Agent Coding 的重要心法：**预设降级路径，不让单点故障卡死整个流程**。

---

### 📦 配置/工具详表

| 模块 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|------|-------------|---------|-----------|
| OpenCode 安装 | `npm install -g opencode-ai` | 全局可用 AI 编程助手 | 需要 Node.js 环境 |
| OpenCode 交互模式 | `bash pty:true workdir:~/myopencode command:"opencode"` | 交互式 AI 编程 | 部分服务器环境会卡住，需备用方案 |
| OpenCode 非交互模式 | `opencode run "Create a complete Snake game using HTML5 Canvas"` | 直接执行任务 | 推荐作为主方案 |
| GitHub CLI 安装 | `curl -fsSL https://github.com/cli/cli/releases/download/v2.63.2/gh_2.63.2_linux_amd64.tar.gz \| tar -xz -C /tmp && cp /tmp/gh_2.63.2_linux_amd64/bin/gh /usr/local/bin/` | 命令行管理 GitHub | 版本号 v2.63.2，注意平台架构 |
| GitHub Token 登录 | `echo "YOUR_GITHUB_TOKEN" \| gh auth login --with-token` | 免密操作 GitHub | Token 只给 repo 权限 |
| GitHub API 建仓 | `curl -X POST https://api.github.com/user/repos -H "Authorization: token TOKEN" -d '{"name":"snake-game","private":false}'` | 自动创建公开仓库 | 备用方案，gh CLI 优先 |
| Git 推送（含 token） | `git remote add origin https://username:token@github.com/username/snake-game.git && git push -u origin master` | 免交互推送 | token 嵌入 URL，注意安全 |
| Vercel CLI 安装 | `npm install -g vercel` | 命令行部署 | 需要 npm |
| Vercel 部署 | `vercel --token YOUR_VERCEL_TOKEN --yes --prod` | 自动检测项目类型并部署 | `--yes` 跳过所有交互确认 |
| Cron 定时 Agent | `cron action:add job:{"schedule":{"kind":"cron","expr":"0 9 * * 1"},"payload":{"kind":"agentTurn","message":"更新网站内容"}}` | 每周一 9 点自动更新 | OpenClaw 专属语法 |
| 多 Agent 并发 | `bash pty:true background:true command:"opencode '设计前端界面'"` + 同时运行后端 | 前后端并行开发 | background:true 关键参数 |

---

### 🛠️ 操作流程

**1. 准备阶段**

```bash
# 安装工具链
npm install -g opencode-ai vercel

# 安装 GitHub CLI（Linux amd64）
curl -fsSL https://github.com/cli/cli/releases/download/v2.63.2/gh_2.63.2_linux_amd64.tar.gz | tar -xz -C /tmp
cp /tmp/gh_2.63.2_linux_amd64/bin/gh /usr/local/bin/

# 创建项目目录并初始化 Git
mkdir -p ~/myopencode && cd ~/myopencode
git init
git config --global user.email "your@email.com"
git config --global user.name "yourname"
```

**2. 核心执行（Agent Coding）**

```bash
# 方式一：非交互模式（推荐）
opencode run "Create a complete Snake game using HTML5 Canvas, CSS, and JavaScript"

# 方式二：交互模式（PTY，可能卡住）
bash pty:true workdir:~/myopencode command:"opencode"
# 然后输入：创建一个贪吃蛇游戏，使用 HTML5 Canvas，包含完整的游戏逻辑、得分系统和响应式设计

# 方式三：交互模式卡住时的降级方案
# 手动创建 index.html / style.css / game.js（见下方代码块）
```

index.html 核心结构：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>贪吃蛇游戏</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>🐍 贪吃蛇游戏</h1>
        <div class="game-info">
            <div class="score">得分: <span id="score">0</span></div>
            <div class="high-score">最高分: <span id="highScore">0</span></div>
        </div>
        <canvas id="gameCanvas" width="400" height="400"></canvas>
        <div class="controls">
            <p>使用方向键 ↑↓←→ 控制蛇的移动</p>
            <button id="startBtn">开始游戏</button>
            <button id="pauseBtn">暂停</button>
            <button id="restartBtn">重新开始</button>
        </div>
        <div id="gameOver" class="game-over hidden">
            <h2>游戏结束!</h2>
            <p>最终得分: <span id="finalScore">0</span></p>
            <button id="playAgainBtn">再玩一次</button>
        </div>
    </div>
    <script src="game.js"></script>
</body>
</html>
```

style.css 核心样式：
```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
}
.container {
    text-align: center;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
h1 {
    background: linear-gradient(45deg, #00d4aa, #00a8e8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
#gameCanvas {
    border: 3px solid #00d4aa;
    border-radius: 10px;
    background: #0a0a0a;
}
```

**3. 推送到 GitHub**

```bash
# 提交代码
git add .
git commit -m "Initial commit: Snake game with HTML5 Canvas"

# 方式一：GitHub CLI
echo "YOUR_GITHUB_TOKEN" | gh auth login --with-token
gh repo create snake-game --public --description "A classic Snake game"
git push -u origin master

# 方式二：API 直接建仓
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"name":"snake-game","description":"A classic Snake game built with HTML5 Canvas","private":false}'

git remote add origin https://username:token@github.com/username/snake-game.git
git push -u origin master
```

**4. 部署到 Vercel**

```bash
cd ~/myopencode
vercel --token YOUR_VERCEL_TOKEN --yes --prod
# 输出：Production: https://myopencode-xxx.vercel.app
```

**5. 让 Agent 自动生成 README 并推送**

在 OpenClaw 中输入：
```
这个过程太棒了，我打算写一篇文章，你帮我直接根据你刚才的步骤，生成一篇文章，
标题是：用 Openclaw+OpenCode+GitHub+Vercel 实现 Agent Coding，
最好是有流程图详细解释下这个步骤
```
然后：
```
推送到刚才贪吃蛇仓库作为 readme
```

---

### 💡 具体案例/数据

**本次贪吃蛇项目完整时间线**：

| 时间 | 用户指令 | Agent 动作 |
|------|---------|-----------|
| 21:49 | "帮我安装 opencode" | 安装 OpenCode CLI |
| 21:53 | "帮我新建一个目录 myopencode" | 创建目录并初始化 git |
| 21:56 | "启动 opencode" | 运行交互式编程助手 |
| 21:57 | （无指令） | OpenCode 卡住，Agent 改用直接创建文件 |
| 21:58 | （无指令） | 贪吃蛇游戏代码生成完成（~400 行） |
| 22:05 | "`https://github.com/freestylefly`" | 配置 GitHub 连接 |
| 22:10 | （无指令） | 创建 GitHub 仓库并推送代码 |
| 22:13 | "帮我部署到 vercel" | 安装 Vercel CLI 并部署 |
| 22:20 | （无指令） | Vercel 部署成功，游戏上线 |
| 22:28 | "帮我写一篇文章记录这个过程" | 生成完整教程文档 |
| 22:31 | "推送到刚才贪吃蛇仓库作为 readme" | 自动提交 README 到 GitHub |

**量化结果**：
- 总耗时：42 分钟（含工具安装）
- 代码量：~400 行
- 部署耗时：< 10 秒
- 用户手写命令数：0
- 在线演示：`https://myopencode.vercel.app`
- 源码仓库：`https://github.com/freestylefly/snake-game`

---

### 📝 避坑指南

- ⚠️ **OpenCode 交互模式可能卡死**：PTY 模式在部分服务器环境不稳定，21:57 实测卡住。预案：立刻切换 `opencode run "..."` 非交互模式，或直接手动创建文件，不要死等。
- ⚠️ **GitHub Token 权限最小化**：只给 repo 权限，不要给 admin/delete 等高危权限，防止 Agent 误操作。
- ⚠️ **Token 嵌入 Git URL 有安全风险**：`git remote add origin https://username:token@github.com/...` 这种方式 token 会明文存在 `.git/config`，生产环境建议用 `gh auth login` 替代。
- ⚠️ **Vercel 静态网站无需构建配置**：`--yes` 参数会跳过所有交互确认，自动检测为静态网站直接部署，不需要额外的 `vercel.json`。
- ⚠️ **多 Agent 并发需加 `background:true`**：不加这个参数会阻塞主线程，导致后续指令无法执行。

---

### 🏷️ 行业标签

#AgentCoding #OpenClaw #OpenCode #VibeCoding #GitHub #Vercel #AI自动化 #全链路部署 #零代码开发

---

---
