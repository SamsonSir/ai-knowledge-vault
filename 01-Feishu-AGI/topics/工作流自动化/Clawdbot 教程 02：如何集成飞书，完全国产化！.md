# 工作流自动化

## 15. [2026-02-05]

## 📙 文章 4


> 文档 ID: `XC5SwJ15RiKAg0kDyFjchZeCnfh`

**来源**: Clawdbot 教程 02：如何集成飞书，完全国产化！ | **时间**: 2026-02-05 | **原文链接**: `https://mp.weixin.qq.com/s/yANheGk5...`

---

### 📋 核心分析

**战略价值**: 通过 Clawdbot 2026.2.2 官方飞书插件，将国产大模型（minimax/kimi/GLM 等）+ 飞书群聊打通，实现零翻墙的全国产 AI 助手方案。

**核心逻辑**:
- Clawdbot 2026.2.2 版本正式原生支持飞书 channel，飞书通过长连接（非 Webhook）接收事件，无需公网 IP
- 飞书机器人权限需通过 JSON 批量导入，共 15 项 tenant 权限 + 3 项 user 权限，缺一不可
- 飞书机器人必须手动开启「机器人能力」（填写欢迎语并保存），否则无法收发消息
- 飞书插件通过 `openclaw channels add` 交互式向导安装，但存在两个已知 bug 需手动绕过
- Bug 1：插件已存在但未安装成功时，向导会静默跳回上层菜单，需手动删除插件目录后重装
- Bug 2：zod 依赖缺失是已知 bug，本地安装会因目录冲突失败，唯一解法是全局安装：`npm install -g zod`
- Channel 配置向导最后必须选择「Finished」确认，否则配置不会写入，这是高频踩坑点
- 私信访问策略推荐选 Pairing 模式，用户需发送配对码才能绑定，防止陌生人滥用
- 飞书事件订阅必须选「使用长连接接收事件」，添加 `im.message.receive_v1` 事件，否则机器人收不到私信
- 飞书机器人配置必须「创建版本并发布」才能生效，未发布等于所有配置作废
- 最终配对流程：飞书发消息 → 机器人回复 `pair:XXXXXX` → 将配对码粘贴到 Clawdbot Web UI 完成绑定

---

### 🛠️ 操作流程

**第一步：飞书开发者后台创建机器人**

1. 进入飞书开发者后台，创建新应用，填写名称、描述、图标
2. 记录「凭证与基础信息 - 应用凭证」中的 `App ID` 和 `App Secret`
3. 进入「权限管理」→「批量导入导出权限」，导入以下 JSON：

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": [
      "aily:file:read",
      "aily:file:write",
      "im:chat.access_event.bot_p2p_chat:read"
    ]
  }
}
```

4. 点击「确认新增权限」
5. 进入「机器人」配置页 → 点击「如何开始使用」→ 输入欢迎语（如"你好，我是 AI 助手"）→ 保存，开启机器人能力

---

**第二步：Clawdbot 本地配置飞书 Channel**

```bash
# 1. 启动交互式向导
openclaw channels add
# 选择 Feishu/Lark，系统自动下载插件

# 2. 如果提示"插件已存在"并跳回菜单：
#    按系统提示找到插件目录，手动删除整个插件文件夹
#    然后重新运行：
openclaw channels add

# 3. 提示缺少 zod 依赖时，全局安装：
npm install -g zod

# 4. 再次运行向导：
openclaw channels add
```

向导填写项：

| 配置项 | 填写内容 |
|--------|---------|
| Feishu account id | 自定义名称，如 `my-bot` |
| 飞书版本 | 国内用户选「中国版飞书」 |
| App ID | 飞书后台获取的 App ID |
| App Secret | 飞书后台获取的 App Secret |
| Configure DM access policies now? | Yes |
| Feishu DM policy | Pairing（推荐） |
| Add display names? | No |
| 最后确认 | ⚠️ 必须选「**Finished**」 |

```bash
# 5. 配置完成后重启网关
openclaw gateway restart
```

---

**第三步：飞书后台完成事件配置**

1. 进入「事件与回调」→「事件配置」→「订阅方式」→ 选「使用长连接接收事件」→ 保存
   - 若提示"没有建立长连接"，等 1-2 分钟后再点保存
2. 点击「添加事件」，搜索并添加 `im.message.receive_v1`
3. 进入「版本管理与发布」→「创建版本」→「发布」

---

**第四步：配对机器人**

1. 在飞书中找到刚创建的机器人，发送任意消息
2. 机器人自动回复配对码，格式：`pair:XXXXXX`
3. 打开 Clawdbot Web UI，将配对码发送给 Clawdbot
4. 绑定成功，即可在飞书私聊或群聊中使用

---

### 📝 避坑指南

- ⚠️ 插件安装提示"已存在"并跳回菜单 → 手动删除插件目录，重新运行 `openclaw channels add`
- ⚠️ zod 依赖缺失是已知 bug，本地安装无效 → 必须用 `npm install -g zod` 全局安装
- ⚠️ 向导最后没有点「Finished」→ channel 不会被添加，需重新走一遍向导
- ⚠️ 长连接提示未建立 → 等 1-2 分钟后再保存，同时检查 `openclaw gateway restart` 是否已执行
- ⚠️ 机器人没有发布版本 → 所有配置不生效，必须在「版本管理与发布」中创建并发布版本
- ⚠️ 未开启「机器人能力」→ 无法收发消息，必须在机器人配置页填写欢迎语并保存

---

### 🏷️ 行业标签
#Clawdbot #飞书集成 #国产AI #大模型 #AI助手部署 #飞书机器人 #全国产化方案

---

---
