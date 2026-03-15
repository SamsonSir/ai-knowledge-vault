# 工作流自动化

## 17. [2026-02-07]

## 📙 文章 4


> 文档 ID: `NUMpwqGhcihCprkK1u5c3nJNnpb`

**来源**: 鹿导：OpenClaw + Gemini 3 Flash + 飞书 部署完整指南 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 在阿里云美区服务器上，用 Antigravity 反代 Google Gemini 3 Flash（Google One 会员免费额度，5小时重置），搭建 OpenClaw + 飞书的全自动 AI Agent 通道，实现近零成本 7x24 在线数字员工。

**核心逻辑**:
- 整体链路：飞书用户 → 飞书云端 → feishu-openclaw 桥接 → OpenClaw Gateway → Antigravity Proxy → Google Gemini 3 Flash
- 服务器选美区（弗吉尼亚）是关键，国内区域访问 Google 会被墙，推荐配置：2 vCPU / 2 GiB 内存 / 40 GiB ESSD，Ubuntu 系统
- 2 GiB 内存必须开 Swap（2G），否则 Node.js 进程在构建/运行时会 OOM 崩溃
- Antigravity Proxy 监听 127.0.0.1:8080，不对外暴露，OpenClaw 通过 baseUrl 本地调用，apiKey 填 "test" 即可（OAuth 由 Antigravity 自己处理）
- openclaw onboard 时加 --install-daemon 参数，先跳过模型选择，再手动编辑 ~/.openclaw/openclaw.json 写入自定义 provider，避免 onboard 向导覆盖配置
- 三个核心服务（antigravity-proxy、openclaw-gateway、feishu-bridge）全部注册为 systemd 服务，保证服务器重启后自动拉起
- 飞书桥接必须先在服务器跑起来再回飞书开放平台配置长连接，顺序反了会导致长连接建立失败
- 飞书权限必须包含 im:resource，否则消息收发会报权限不足；事件订阅选「长连接」模式，不需要公网 Webhook
- 模型配置中 primary 设为 antigravity-proxy/gemini-3-flash，fallback 设为 antigravity-proxy/gemini-3-pro-high，contextWindow 1048576，maxTokens 65536
- apt upgrade 过程中弹出 openssh-server 配置冲突，必须选 "keep the local version currently installed"，否则阿里云定制的 sshd_config 被覆盖可能导致 SSH 永久断连

---

### 🛠️ 操作流程

#### 第一阶段：服务器基础环境

```bash
# SSH 登录
ssh root@<公网IP>

# 更新系统
apt update && apt upgrade -y
apt install -y curl wget git build-essential

# 开 Swap（2GB 内存必做）
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
free -h

# 安装 Node.js 22+
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
node -v   # 确认 >= 22
npm -v

# 安装 pnpm（源码构建时需要）
npm install -g pnpm
```

#### 第二阶段：安装 OpenClaw

```bash
# 一键安装（加 --no-onboard，先不做引导，后面手动配置模型）
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard

# 验证
openclaw --version
```

#### 第三阶段：配置 Antigravity Proxy

```bash
# 全局安装
npm install -g antigravity-claude-proxy@latest

# 添加 Google 账号（无头模式，会输出 OAuth URL）
antigravity-claude-proxy accounts add --no-browser
# → 复制输出的 URL 到本地浏览器完成 Google 授权，把授权码粘贴回终端

# 如果报错（端口占用），先清掉再添加
kill $(lsof -t -i:8080)
# 或
systemctl stop antigravity-proxy
antigravity-claude-proxy accounts add --no-browser

# 后台启动代理
nohup env HOST=127.0.0.1 antigravity-claude-proxy start > /var/log/antigravity-proxy.log 2>&1 &

# 验证
curl https://127.0.0.1:8080/health
curl "https://127.0.0.1:8080/account-limits?format=table"
```

**设置 systemd 持久运行**：

```bash
cat > /etc/systemd/system/antigravity-proxy.service << 'EOF'
[Unit]
Description=Antigravity Claude Proxy
After=network.target

[Service]
Type=simple
User=root
Environment=HOST=127.0.0.1
Environment=PORT=8080
ExecStart=/usr/bin/env antigravity-claude-proxy start
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable antigravity-proxy
systemctl start antigravity-proxy
systemctl status antigravity-proxy
```

#### 第四阶段：配置 OpenClaw 使用 Gemini 3 Flash

**1. 运行 onboard 向导**

```bash
openclaw onboard --install-daemon
# 向导中：跳过初始模型选择，选 gemini-3-flash，选 yes 安装 daemon
```

**2. 编辑配置文件**

```bash
nano ~/.openclaw/openclaw.json
# 清空旧内容（nano 中：Ctrl+6 设标记 → 移到末尾 → Ctrl+K 逐行删除）
```

写入以下完整配置：

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "antigravity-proxy": {
        "baseUrl": "https://127.0.0.1:8080",
        "apiKey": "test",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "gemini-3-flash",
            "name": "Gemini 3 Flash",
            "reasoning": true,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 1048576,
            "maxTokens": 65536
          },
          {
            "id": "gemini-3-pro-high",
            "name": "Gemini 3 Pro High",
            "reasoning": true,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 1048576,
            "maxTokens": 65536
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "antigravity-proxy/gemini-3-flash",
        "fallbacks": ["antigravity-proxy/gemini-3-pro-high"]
      }
    }
  }
}
```

**3. 验证 & 启动**

```bash
openclaw models list   # auth 列显示 yes = 成功
openclaw gateway       # 启动 Gateway
openclaw status
openclaw doctor        # 选 yes
```

**4. Gateway systemd 服务**

```bash
cat > /etc/systemd/system/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway
After=network.target antigravity-proxy.service

[Service]
Type=simple
User=root
ExecStart=/usr/bin/env openclaw gateway
Restart=always
RestartSec=5
Environment=HOME=/root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable openclaw-gateway
systemctl start openclaw-gateway
systemctl status openclaw-gateway
```

#### 第五阶段：配置飞书频道

**1. 安装飞书桥接**

```bash
cd ~
git clone https://github.com/AlexAnys/feishu-openclaw.git
cd feishu-openclaw
npm install
```

**2. 飞书开放平台创建机器人**

- 打开 https://open.feishu.cn/app → 创建自建应用 → 填写名称（如"AI 助手"）
- 添加应用能力 → 选「机器人」
- 权限管理 → 批量导入以下 JSON：

```json
{"scopes":{"tenant":["im:chat:read","im:chat:update","im:message.group_at_msg:readonly","im:message.p2p_msg:readonly","im:message.pins:read","im:message.pins:write_only","im:message.reactions:read","im:message.reactions:write_only","im:message:readonly","im:message:recall","im:message:send_as_bot","im:message:send_multi_users","im:message:send_sys_msg","im:message:update","im:resource"],"user":["contact:user.employee_id:readonly"]}}
```

**3. 先回终端启动桥接（必须先于飞书长连接配置）**

```bash
mkdir -p ~/.clawdbot/secrets
echo "你的飞书AppSecret" > ~/.clawdbot/secrets/feishu_app_secret
chmod 600 ~/.clawdbot/secrets/feishu_app_secret

cd ~/feishu-openclaw
CLAWDBOT_CONFIG_PATH=/root/.openclaw/openclaw.json FEISHU_APP_ID=cli_你的AppID node bridge.mjs
```

**4. 回飞书开放平台完成配置**

- 事件订阅 → 选「长连接」模式
- 添加以下 4 个事件：
  - `im.chat.member.bot.added_v1`
  - `im.message.bot_muted_v1`
  - `im.message.message_read_v1`
  - `im.message.receive_v1`
- 点击「创建版本」→ 填写必填项 → 发布

**5. feishu-bridge systemd 服务**

```bash
cat > /etc/systemd/system/feishu-bridge.service << 'EOF'
[Unit]
Description=Feishu OpenClaw Bridge
After=network.target openclaw-gateway.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/feishu-openclaw
Environment=FEISHU_APP_ID=cli_你的AppID
Environment=CLAWDBOT_CONFIG_PATH=/root/.openclaw/openclaw.json
Environment=HOME=/root
ExecStart=/usr/bin/node bridge.mjs
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable feishu-bridge
systemctl start feishu-bridge
```

---

### 📦 配置/工具详表

| 模块 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|------|-------------|---------|-----------|
| Antigravity Proxy | HOST=127.0.0.1, PORT=8080 | 本地代理 Gemini，5小时额度重置 | 只绑 127.0.0.1，不对外暴露 |
| openclaw.json | baseUrl: `https://127.0.0.1:8080`, apiKey: "test" | OpenClaw 调用本地代理 | 用 127.0.0.1 不用 localhost |
| 模型配置 | contextWindow: 1048576, maxTokens: 65536 | 超长上下文 | cost 全填 0，不计费 |
| 飞书权限 | 必须含 im:resource | 消息收发正常 | 缺这个权限会静默失败 |
| 飞书事件 | 长连接模式，4个事件 | 实时收消息 | 必须先跑 bridge.mjs 再配长连接 |
| Swap | 2G swapfile | 防 OOM | 写入 /etc/fstab 保证重启生效 |

---

### 🎯 关键洞察

**API 配置清单（鹿导实际在用的全套）**：

| 类型 | 工具 | 用途 |
|------|------|------|
| 搜索情报 | Tavily API | 国外技术栈调研、结构化数据返回，适合喂给 AI |
| 搜索情报 | 博查(Bocha) API | 国内中文互联网情报，供应链/行业动态监控 |
| 模型引擎 | Google Antigravity (Gemini 3) | 主控大脑，高并发低延迟，超长上下文 |
| 模型引擎 | OpenRouter (DeepSeek) | 战术备用，主模型异常时保底 |
| 通讯 | Feishu API | 早报推送、系统报警、灵感反馈 |
| 通讯 | iMessage CLI | 紧急通道，不看飞书时直接轰炸手机 |
| 视觉自动化 | Peekaboo + Browser | 控制 Mac mini 屏幕，操作无 API 的后台系统 |

**Memo 工作流（灵感捕捉 + 夜间复盘）**：
1. 白天随时给 OpenClaw 发 `Memo: <碎片灵感>`
2. OpenClaw 按预设 Prompt 即时延展并记录
3. 晚上固定时间 OpenClaw 主动发起复盘，汇总所有 Memo
4. 拆解成第二天具体可执行的工作计划

---

### 📝 避坑指南

- ⚠️ apt upgrade 弹出 openssh-server 冲突 → 必须选 "keep the local version currently installed"，选错可能永久断 SSH
- ⚠️ 飞书长连接配置必须在 bridge.mjs 跑起来之后，顺序反了长连接建立失败
- ⚠️ baseUrl 写 `https://127.0.0.1:8080` 不要写 localhost，部分环境 localhost 解析异常
- ⚠️ Google OAuth 有效期有限，过期后执行 `antigravity-claude-proxy accounts add --no-browser` 重新授权
- ⚠️ 2 GiB 内存不开 Swap 直接跑 Node.js 多服务会 OOM，必须先建 swapfile
- ⚠️ openclaw onboard 加 --no-onboard 安装，加 --install-daemon 做 onboard，两个参数用途不同别混

---

### 🛠️ 排错速查

| 问题 | 排查命令 |
|------|---------|
| 飞书发消息无回复 | `journalctl -u feishu-bridge -f` |
| 模型调用失败 | `journalctl -u antigravity-proxy -f` |
| Gateway 无响应 | `journalctl -u openclaw-gateway -f` |
| 代理健康检查 | `curl https://127.0.0.1:8080/health` |
| OpenClaw 深度诊断 | `openclaw status --deep` + `openclaw models list` |
| Google OAuth 过期 | `antigravity-claude-proxy accounts add --no-browser` |
| 飞书权限不足 | 回开放平台确认 im:resource 已开通 |
| 三服务整体状态 | `systemctl status antigravity-proxy openclaw-gateway feishu-bridge` |

---

### 🏷️ 行业标签
#OpenClaw #Gemini #飞书机器人 #AIAgent #VibeCoding #反向代理 #阿里云部署 #一人公司 #systemd #Antigravity

---

---
