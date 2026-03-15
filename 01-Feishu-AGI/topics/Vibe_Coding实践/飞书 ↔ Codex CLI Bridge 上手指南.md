# Vibe_Coding实践

## 6. [2026-01-16]

## 📓 文章 6


> 文档 ID: `G8Cpwgzm8irfWDkPOBwcGAHJnUg`

**来源**: 飞书 ↔ Codex CLI Bridge 上手指南 | **时间**: 2026-01-15 | **原文链接**: `https://mp.weixin.qq.com/s/bS6crMmS...`

---

### 📋 核心分析

**战略价值**: 用飞书长连接双向桥接本地 Codex CLI，彻底消除"离开电脑就掉线"的上下文断裂问题，实现真正的移动端 Vibe Coding 控制台。

**核心逻辑**:

- **痛点根因**：Codex CLI 是本地进程，回复只在终端可见，离开工位即断联，无法异步跟进关键输出
- **桥接方向①（Codex → 飞书）**：Codex 有新回复时，通过群自定义机器人 Webhook 自动推送到飞书群
- **桥接方向②（飞书 → Codex）**：飞书消息通过长连接事件 `im.message.receive_v1` 接收，写入本地 Codex 会话，无需公网回调
- **tui 模式**：桥接进程维持一个真实终端会话，飞书消息像键盘输入一样注入 Codex，上下文连续，体验最接近"人在电脑前"
- **exec 模式**：每条飞书消息触发一次 `codex exec`，结果出来后 `resume --last` 继续，输出更干净，适合任务式一问一答
- **session 输出源**：从 `~/.codex/sessions/**/rollout-*.jsonl` 抽取最后一条 assistant 消息，去噪后推送，内容整洁
- **pty 输出源**：直接读终端原始输出，经 `stripAnsi` 去噪，实时性更强但可能有杂音
- **防刷屏机制**：`idlePushMs`（默认 10000ms）控制合并窗口，等待无新输出 10 秒后才合并推送一次，避免逐行轰炸群
- **安全白名单**：`allowedOpenIds` 限定哪些 `open_id` 可以写入本地终端，不配则任何能私聊机器人的人都能远程操控你的终端
- **推荐组合**：`tui + session`，兼顾上下文连续性与输出干净度

---

### 🎯 关键洞察

**为什么用长连接而非 Webhook 回调**：飞书事件订阅支持两种接收方式——服务端回调（需公网 IP）和长连接（本地进程主动保持连接）。桥接工具选择 `im.message.receive_v1` 长连接，原因是本地开发机通常没有公网地址，长连接方案零运维、零端口暴露，直接在内网跑即可。

**tui vs exec 的本质差异**：tui 是"持久会话注入"，exec 是"无状态调用+恢复"。前者上下文天然连续，后者每次都是新调用再 resume，适合明确边界的任务型交互。

**`sendToUserOnIdle` 的通勤价值**：推群的同时私聊发起者，意味着你在地铁上发出的指令，Codex 跑完后会直接私信你结果，不用盯着群消息流。

---

### 📦 配置/工具详表

| 字段 | 说明 | 推荐值 | 注意事项 |
|------|------|--------|---------|
| `appId` / `appSecret` | 飞书自建应用身份凭证 | 从飞书开放平台获取 | 必填，缺一不可 |
| `webhookUrl` | 群自定义机器人推送地址 | 群机器人配置页复制 | 用于 Codex → 飞书方向 |
| `allowedOpenIds` | 终端控制白名单 | 填入自己的 open_id | 强烈建议配，空数组=无限制 |
| `mode` | 工作模式 | `tui`（默认推荐） | `exec` 适合任务式问答 |
| `outputSource` | 输出抓取方式 | `session`（推荐） | `pty` 更实时但有杂音 |
| `idlePushMs` | 合并推送等待窗口 | `10000`（10秒） | 调小=更实时，调大=更整洁 |
| `sendToUserOnIdle` | 是否同时私聊发起者 | `true`（通勤场景） | 推群+私聊双通道 |
| `maxMessageChars` | 单条消息字符上限 | 按飞书消息限制设置 | 防止超长消息炸群 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 安装 Node.js 18+
- 本地确认 `codex` 命令可用（`codex --version` 验证）
- 飞书开放平台创建自建应用，订阅事件 `im.message.receive_v1`，开启长连接接收模式
- 在目标飞书群添加自定义机器人，复制 Webhook URL

**2. 安装 & 启动**

```bash
# 克隆项目
git clone https://github.com/Larkspur-Wang/feishu_X_codex

# 安装依赖
npm install

# 复制配置文件
copy config.example.json config.json
# Linux/Mac 用：cp config.example.json config.json

# 编辑 config.json，填入 appId/appSecret/webhookUrl/allowedOpenIds 等字段

# 启动
npm start
```

**指定工作目录（三种方式）**

```bash
# Windows CMD
set WORKING_DIR=E:\Your\Project
npm start

# PowerShell
$env:WORKING_DIR="E:\Your\Project"
npm start

# 启动参数直传
npm start -- --dir=E:\Your\Project
```

**3. 获取 open_id 并配置白名单**

```json
// 第一步：临时设为空数组
{ "allowedOpenIds": [] }
```

启动后向机器人发一条消息，控制台会打印你的 `open_id`，复制后填回配置：

```json
{ "allowedOpenIds": ["ou_xxxxxxxxxxxxxxxx"] }
```

重启生效。

---

### 📝 避坑指南

- ⚠️ **乱码/碎字符**：输出源改为 `session`，从 `~/.codex/sessions/**/rollout-*.jsonl` 读取，比 pty 干净得多
- ⚠️ **allowedOpenIds 为空**：等于把终端控制权开放给所有能私聊机器人的人，生产环境绝对不能省
- ⚠️ **workingDir 未限制**：建议明确指定工作目录，防止误操作到系统目录或其他项目
- ⚠️ **消息刷屏**：`idlePushMs` 默认 10 秒，如果觉得太慢可以调到 3000-5000ms，但不建议低于 2000ms

---

### 🏷️ 行业标签

#CodingAssistant #飞书 #CodexCLI #VibeCoding #远程开发 #开发者工具 #NodeJS #自动化桥接

---

---
