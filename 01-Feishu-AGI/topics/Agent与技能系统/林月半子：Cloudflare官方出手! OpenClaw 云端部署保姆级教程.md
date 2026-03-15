# Agent与技能系统

## 47. [2026-02-03]

## 📓 文章 6


> 文档 ID: `QXhNwDcC0icBH3kKxcucwybmn7c`

**来源**: 林月半子：Cloudflare官方出手! OpenClaw 云端部署保姆级教程 | **时间**: 2026-02-03 | **原文链接**: `https://mp.weixin.qq.com/s/N_-f_pjb...`

---

### 📋 核心分析

**战略价值**: 用 Cloudflare Workers + Moltworker 零服务器部署 OpenClaw，三重认证 + R2 持久化 + AI Gateway 可观测，彻底替代自建 VPS 方案。

**核心逻辑**:

- **Moltworker 是 Cloudflare 官方开源项目**，项目地址 `https://github.com/cloudflare/moltworker`，专为 OpenClaw 云端部署设计，非第三方套壳。
- **内置浏览器自动化**（cloudflare-browser），支持网页截图、数据抓取，不是单纯的 API 转发。
- **R2 每5分钟自动备份**对话历史和设备配对信息，容器重启后自动从 R2 恢复，解决 Workers 无状态的根本问题。
- **三重认证链路**：用户请求 → CF Access 登录（邮箱验证码）→ 验证 MOLTBOT_GATEWAY_TOKEN → 设备配对批准 → 才能聊天，防止白嫖。
- **硬性门槛**：必须开通 Workers Paid 订阅，免费版不支持 Sandbox 容器，本地需要 Node.js 18+ 和 Docker。
- **AI Gateway 作为"二传手"**：用你自己的 DeepSeek/OpenRouter Key 调模型，但叠加缓存、限流、Token 消耗统计，所有密钥通过 `wrangler secret put` 加密注入，不写死在代码里。
- **OpenRouter Free Tier 白嫖方案**：配置 `openrouter/free` 模型 ID，自动路由到 Gemini、Kimi 等免费模型，实现 0 成本运行。
- **Chat Channel 配置可免 CLI**：直接在 OpenClaw 对话框里对机器人说"帮我配置 Discord 渠道，Token 是 xxx"，机器人自动完成配置，包括 Clawdbot Pairing 操作。
- **管理界面功能完整**：可查看 R2 备份状态、审批设备配对请求、重启网关进程，集成 Cloudflare Access 做身份认证。
- **首次访问冷启动需 1~2 分钟**，容器初始化时间，不是报错。

---

### 🛠️ 操作流程

#### 1. 准备阶段

- 开通 Cloudflare Workers Paid 订阅
- 本地安装 Node.js 18+、Docker
- 准备 AI 模型 API Key（DeepSeek / OpenRouter 均可）
- 注册 Cloudflare 账号

#### 2. 安装 Wrangler 并登录

```bash
npm i -D wrangler@latest
npx wrangler login
# 浏览器弹出授权页，点击允许即可
```

#### 3. 克隆项目并安装依赖

```bash
git clone git@github.com:cloudflare/moltworker.git
cd moltworker
npm install
```

#### 4. 配置 AI 模型（二选一）

**方案A：直接用 Anthropic Key（最简单）**
```bash
npx wrangler secret put ANTHROPIC_API_KEY
```

**方案B：用 Cloudflare AI Gateway（推荐，可观测 Token 消耗）**

步骤：
1. Cloudflare 后台 → 计算和AI → AI Gateway → 创建网关，选择提供商（如 DeepSeek）
2. 点击 Add，填入 DeepSeek API Key（Gateway 是中间商，Key 必须填）
3. 右侧 Create a token → 输入名称 → 生成 Gateway 专属 Token（复制保存）
4. 回终端执行：

```bash
# 填入 Gateway Token（不是 DeepSeek Key）
npx wrangler secret put AI_GATEWAY_API_KEY

# 填入 Gateway Base URL，格式如下：
# https://gateway.ai.cloudflare.com/v1/你的账户ID/你的网关名/deepseek
npx wrangler secret put AI_GATEWAY_BASE_URL
```

#### 5. 设置 MOLTBOT_GATEWAY_TOKEN（访问控制核心）

```bash
# 生成 32 字节高强度随机 Token
export MOLTBOT_GATEWAY_TOKEN=$(openssl rand -hex 32)

# 显示并保存（只显示一次！）
echo "你的 Gateway Token: $MOLTBOT_GATEWAY_TOKEN"

# 注入到 Cloudflare
echo "$MOLTBOT_GATEWAY_TOKEN" | npx wrangler secret put MOLTBOT_GATEWAY_TOKEN
```

#### 6. 配置 Cloudflare Access（身份认证）

**开启 Access：**
Cloudflare Dashboard → Workers & Pages → 点进 `moltbot-sandbox` → 设置 → 域和路由 → workers.dev 行右侧 `...` → Enable Cloudflare Access

**获取两个值并注入：**

| 变量 | 去哪找 |
|------|--------|
| `CF_ACCESS_TEAM_DOMAIN` | Zero Trust Dashboard → Team domain |
| `CF_ACCESS_AUD` | Zero Trust Dashboard → Access → Applications → 点进应用 → 复制 UUID |

```bash
npx wrangler secret put CF_ACCESS_TEAM_DOMAIN
npx wrangler secret put CF_ACCESS_AUD
```

#### 7. 配置 R2 持久存储（防失忆）

1. Cloudflare Dashboard → R2 → Manage R2 API Tokens → Create User API Token
2. 权限选 **Object Read & Write**，范围选 **Specific bucket → moltbot-data**
3. 生成后复制 Access Key ID 和 Secret Access Key（只显示一次！）

```bash
npx wrangler secret put R2_ACCESS_KEY_ID
npx wrangler secret put R2_SECRET_ACCESS_KEY

# Account ID：Cloudflare 首页 → Manage Account → ... → 复制账户ID
npx wrangler secret put CF_ACCOUNT_ID
```

#### 8. 部署

```bash
npm run deploy
# 成功后终端输出 OpenClaw 访问地址
```

#### 9. 访问与登录

```
https://your-worker.workers.dev/?token=YOUR_GATEWAY_TOKEN
```

- 输入邮箱（必须在允许列表内）→ 输入验证码 → 等待 1~2 分钟冷启动
- 进入后先访问 **Moltbot Admin 界面** → 审批设备配对请求 → 才能正常使用

---

### 📦 配置/工具详表

| 模块 | 关键 Secret 变量 | 用途 | 注意事项 |
|------|----------------|------|---------|
| AI 模型直连 | `ANTHROPIC_API_KEY` | 直接调用 Anthropic | 有 Key 直接用，最简单 |
| AI Gateway | `AI_GATEWAY_API_KEY` | Cloudflare Gateway Token | 不是 DeepSeek Key |
| AI Gateway | `AI_GATEWAY_BASE_URL` | `https://gateway.ai.cloudflare.com/v1/{账户ID}/{网关名}/deepseek` | 格式严格，账户ID不能错 |
| 访问控制 | `MOLTBOT_GATEWAY_TOKEN` | 登录 AI 助手控制界面 | 泄露等于失控，用 openssl 生成 |
| CF Access | `CF_ACCESS_TEAM_DOMAIN` | 告诉 Worker 去哪验证 JWT | Zero Trust Dashboard 找 |
| CF Access | `CF_ACCESS_AUD` | 验证通行证是否发给本应用 | 应用详情页的 UUID |
| R2 存储 | `R2_ACCESS_KEY_ID` | R2 读写权限 | 只显示一次，立即保存 |
| R2 存储 | `R2_SECRET_ACCESS_KEY` | R2 读写权限 | 只显示一次，立即保存 |
| R2 存储 | `CF_ACCOUNT_ID` | 定位 R2 Bucket 归属 | 首页 Manage Account 复制 |

---

### 📦 模型配置 Raw JSON

**DeepSeek via AI Gateway：**

```json
{
  "models": {
    "providers": {
      "deepseek": {
        "baseUrl": "https://gateway.ai.cloudflare.com/v1/你的账户ID/openclaw-gateway/deepseek",
        "apiKey": "XlD9YH2moXXXUFaogRhDpB",
        "api": "openai-completions",
        "models": [
          {
            "id": "deepseek-chat",
            "name": "DeepSeek Chat",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-chat"
      }
    }
  }
}
```

> `apiKey` 填 Cloudflare Gateway Token，不是 DeepSeek Key。

**OpenRouter 免费模型（0成本方案）：**

前置：Cloudflare AI Gateway → Provider API Keys → OpenRouter → Add → 填 `sk-or-xxxx`

```json
{
  "models": {
    "providers": {
      "openrouter": {
        "baseUrl": "https://gateway.ai.cloudflare.com/v1/你的账户ID/openclaw-gateway/openrouter",
        "apiKey": "XlD9YH2moxxxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "openrouter/free",
            "name": "Openrouter free",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

> `apiKey` 同样填 Cloudflare Gateway Token，不是 OpenRouter 的 Key。

修改路径：OpenClaw → Config → Raw 模式 → 粘贴 → Apply，立即生效。

---

### 💡 两个 Token 的区别（高频混淆点）

| Token | 变量名 | 是什么 | 在哪填 |
|-------|--------|--------|--------|
| MOLTBOT_GATEWAY_TOKEN | `MOLTBOT_GATEWAY_TOKEN` | 你自己生成的访问密码 | URL 参数 `?token=` |
| AI Gateway Token | `AI_GATEWAY_API_KEY` | Cloudflare Gateway 的认证凭证 | Config Raw 的 `apiKey` 字段 |

---

### 📝 避坑指南

- ⚠️ **R2 Token 和 Access Key 只显示一次**，生成后立即复制到安全位置，关掉页面就找不回来了。
- ⚠️ **Config Raw 里的 apiKey 填 Gateway Token，不是模型提供商的 Key**，这是最高频的配置错误。
- ⚠️ **首次访问冷启动 1~2 分钟**，页面转圈不是报错，耐心等待。
- ⚠️ **进入界面后必须先去 Admin 审批设备**，否则无法正常对话。
- ⚠️ **免费版 Workers 不支持 Sandbox 容器**，Workers Paid 订阅是硬性前提，无法绕过。
- ⚠️ **Base URL 格式严格**：`https://gateway.ai.cloudflare.com/v1/{账户ID}/{网关名}/{提供商}`，账户ID和网关名必须与后台一致。
- ⚠️ **Discord Channel 配置可跳过 CLI**：直接在对话框告诉机器人"帮我配置 Discord 渠道，Token 是 xxx"，机器人自动完成，包括 Pairing 操作。

---

### 🏷️ 行业标签

#Cloudflare #OpenClaw #Workers #AI部署 #无服务器 #DeepSeek #OpenRouter #R2存储 #CloudflareAccess #Moltworker

---

---
