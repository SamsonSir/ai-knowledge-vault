# Agent与技能系统

## 34. [2026-01-28]

## 📘 文章 3


> 文档 ID: `JbykwG7Jli5JuikQH2LcuGEtnLB`

**来源**: Clawdbot 杀疯了！手把手教你接入飞书，把 AI 助理装进社群 | **时间**: 2026-01-28 | **原文链接**: `https://mp.weixin.qq.com/s/qnDCqYtZr4xvGx1mgEDKVw`

---

### 📋 核心分析

**战略价值**: 本地部署的 ClawdBot 没有官方飞书插件，通过社区插件 + WebSocket 长连接方案，可实现飞书群聊/私聊双向 AI 对话，7×24 小时待命。

**核心逻辑**:
- ClawdBot 官方插件库不含飞书，必须依赖社区项目 `m1heng/clawdbot-feishu`，包名为 `@m1heng-clawd/feishu`
- 飞书机器人需在开放平台新建应用并手动启用「机器人能力」，否则无法收发消息
- 权限配置必须包含 5 个 scope：`im:message`、`im:message.p2p_msg:readonly`、`im:message.group_at_msg:readonly`、`im:message:send_as_bot`、`im:resource`，缺一不可
- 插件安装需指定版本 `2026.1.24-3`（最新版），旧版本存在兼容问题
- 本地部署无公网 IP，飞书无法主动推送消息，必须启用 WebSocket 长连接模式，否则机器人只能发消息、无法收消息
- 飞书后台需在「事件与回调」中选择「长连接」并保存，同时添加「接收消息」事件订阅，两步缺一不可
- 本地配置文件 `~/.clawdbot/clawdbot.json` 需在 `feishu` 字段下手动补充 `connectionMode: websocket` 和 `requireMention: true`
- 群聊策略配置阶段选 `Open`（方便测试），后续可按需收紧
- 配置完成后必须在飞书后台点击「发布版本」，否则所有配置不生效
- 验收分两阶段：先测单向（ClawdBot → 飞书群收到消息），再测双向（群内 @机器人 → 收到回复）

---

### 🛠️ 操作流程

**第一步：飞书开放平台准备**

1. 登录飞书开放平台，新建应用
2. 创建后进入应用，启用「机器人」能力
3. 进入权限管理，批量导入以下 JSON：

```json
{
  "scopes": {
    "tenant": [
      "im:message",
      "im:message.p2p_msg:readonly",
      "im:message.group_at_msg:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ]
  }
}
```

---

**第二步：安装飞书插件**

在终端执行（注意必须是 `2026.1.24-3` 版本）：

```bash
clawdbot plugins install @m1heng-clawd/feishu
```

---

**第三步：交互式配置（`clawdbot config` 向导）**

```
运行环境     → 本地部署，直接回车选默认
选择模块     → channels
操作         → 添加配置 Channels
选择 channel → Feishu
填入密钥     → AppID 和 AppSecret（从飞书开放平台复制）
飞书版本     → 国内默认
群聊策略     → Open（测试用）
后续选项     → 一路回车到 finished
最后询问是否直接发消息 → 选 yes
```

---

**第四步：单向联通测试（ClawdBot → 飞书）**

1. 在飞书新建群，将刚创建的机器人拉入群
2. 在群设置中复制「群组 ID（会话 ID）」
3. 在 ClawdBot 配置界面，向该群组 ID 发送一条测试消息
4. 飞书群内收到消息 → 单向通路 OK

---

**第五步：打通双向（WebSocket 长连接）**

飞书后台操作：
1. 进入「事件与回调」→ 选择「长连接」→ 点击保存
2. 在事件配置中添加「接收消息」事件订阅
3. 点击「发布版本」（必须，否则不生效）

本地配置文件修改，打开 `~/.clawdbot/clawdbot.json`，在 `feishu` 字段下补充：

```json
{
  "channels": {
    "feishu": {
      "connectionMode": "websocket",
      "requireMention": true
    }
  }
}
```

重启 ClawdBot：

```bash
clawdbot gateway restart
```

---

**第六步：双向最终验收**

1. 在飞书群内 @机器人 发送消息
2. 观察机器人图标是否闪动（闪动 = 工作中）
3. 收到机器人回复 → 双向通路全部打通

---

### 📦 配置/工具详表

| 模块 | 关键设置/代码 | 预期效果 | 注意事项 |
|------|-------------|---------|---------|
| 飞书权限 | 批量导入 5 个 scope JSON | 机器人可收发消息 | 缺少任一 scope 会导致收发失败 |
| 插件安装 | `@m1heng-clawd/feishu` v`2026.1.24-3` | 飞书渠道可用 | 旧版本有坑，必须装最新版 |
| 群聊策略 | `Open` | 测试阶段无限制 | 生产环境可按需收紧 |
| 连接模式 | `connectionMode: websocket` | 本地无公网 IP 也能收消息 | 不配置则机器人只能发、不能收 |
| 提及设置 | `requireMention: true` | 群内需 @ 才触发 | 避免机器人响应所有消息 |
| 飞书事件 | 添加「接收消息」订阅 + 长连接 | 飞书主动推送消息到本地 | 两步都要做，缺一不可 |
| 发布版本 | 飞书后台点击「发布版本」 | 配置正式生效 | 最容易遗漏的一步 |

---

### 📝 避坑指南

- ⚠️ 插件版本坑：必须安装 `2026.1.24-3` 最新版，旧版本存在已知问题
- ⚠️ 单向≠双向：ClawdBot 能发消息到飞书，不代表飞书能回传消息，必须额外配置 WebSocket
- ⚠️ 发布版本必做：飞书后台所有配置改完后，必须点「发布版本」才生效，否则一切白搭
- ⚠️ 事件订阅不能漏：长连接开了但没加「接收消息」事件，机器人依然听不到群里的话
- ⚠️ 配置文件手动补充：`connectionMode` 和 `requireMention` 不会自动写入，必须手动编辑 `~/.clawdbot/clawdbot.json`

---

### 🏷️ 行业标签
#ClawdBot #飞书机器人 #AI助手接入 #WebSocket长连接 #本地部署 #工作流自动化

---

---
