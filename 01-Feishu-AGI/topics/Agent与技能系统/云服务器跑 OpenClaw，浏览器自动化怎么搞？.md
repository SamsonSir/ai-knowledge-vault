# Agent与技能系统

## 103. [2026-03-06]

## 📔 文章 5


> 文档 ID: `ANPNwl87jiyJOkkfWXHc9VcUnee`

**来源**: 云服务器跑 OpenClaw，浏览器自动化怎么搞？ | **时间**: 2026-03-14 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: OpenClaw 通过内置两种浏览器模式（个人资料模式 + 扩展模式），将"持久登录态 + 浏览器控制 + 任务调度"做成默认能力，彻底解决云服务器无图形界面下的浏览器自动化难题。

**核心逻辑**:

- **OpenClaw 定位**：不是聊天工具，是 AI 执行系统——能打开浏览器、点击网页、调用 API、发飞书消息、执行定时任务。区别于 Claude Code（写代码），OpenClaw 直接把事情执行掉。
- **HTTP 爬虫失效原因**：X.com 是 SPA 单页应用，HTTP 请求返回空 HTML；无法保持登录态；IP 封禁频率可达每小时 5 次。结论：❌ 不可用。
- **Playwright 不稳定原因**：`navigator.webdriver=true` 暴露自动化特征；模拟登录 100% 触发验证码；点击间隔固定、无鼠标轨迹被风控识别；有开发者反馈"稳定运行一周后突然罢工"。结论：⚠️ 随时可能被封。
- **OpenClaw 优势本质**：底层同样用 CDP（Chrome DevTools Protocol），但它把"持久浏览器环境 + 登录状态管理 + 任务调度"做成了默认能力，用户无需自己写脚本维护。
- **个人资料模式原理**：OpenClaw 启动独立 Chrome 实例，有独立用户目录，登录一次后长期保持登录态，支持 24 小时无人值守运行。
- **扩展模式原理**：通过 OpenClaw Relay 插件接管当前正在使用的 Chrome，直接复用已有登录态，适合临时操作。
- **WebFetch 的局限**：内置 WebFetch 只能抓取静态内容并转成 Markdown，无法处理需要登录的网站（X、Reddit、YouTube）、需要点击/滚动的交互操作、需要执行 JS 的动态内容。
- **云服务器配置核心**：云服务器无图形界面，需安装 XFCE 桌面 + TigerVNC，通过 VNC Viewer 连接后才能看到 Chrome 窗口完成首次登录；`DISPLAY=:1` 必须正确配置，否则 Chrome 启动失败。
- **实操验证**：用个人资料模式拉取 `https://scys.com/?filter=essence` 本周精华帖，OpenClaw 自动提示微信扫码登录，手动扫码后继续，可逐条发送帖子（标题、核心总结、作者、发布日期、帖子链接、飞书文档原文链接）。
- **扩展模式使用节奏**：先打开目标网页 → 激活扩展切换为 ON → 再下指令；复杂任务分步执行；遇到验证码手动完成后告知 OpenClaw 继续。

---

### 🎯 关键洞察

**为什么 OpenClaw 比 Playwright 更稳定**：

- Playwright 启动的浏览器天然带有 `navigator.webdriver=true` 标记，这是浏览器指纹检测的核心特征之一。
- OpenClaw 扩展模式接管的是用户日常使用的真实 Chrome，没有任何自动化标记，风控系统无法区分人工操作和自动化操作。
- 登录环节是 Playwright 最脆弱的点——模拟登录必然触发验证码，而 OpenClaw 的登录是人工完成的，验证码也是人工过的，之后的所有操作都复用这个合法登录态。

**技术栈关系梳理**：

```
Claude Code（编程开发工具）
    ⬇ 使用
封装好的 Skills 能力（如 Browser Use）
    ⬇ 基于
Playwright（浏览器控制工具）
```

OpenClaw 是另一条路：直接把浏览器控制 + 登录管理 + 任务调度打包，面向非工程师用户。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| XFCE 桌面 | `sudo apt install xfce4 xfce4-goodies -y` | 云服务器获得图形桌面 | 默认无桌面，必须先装 |
| TigerVNC | `sudo apt install tigervnc-standalone-server tigervnc-common -y` | 支持远程桌面连接 | 本地需安装 VNC Viewer 客户端 |
| VNC 启动 | `vncserver :1 -geometry 1920x1080 -depth 24` | 创建虚拟显示器 :1 | 连接地址：`云服务器IP:5901` |
| DISPLAY 变量 | `export DISPLAY=:1` | Chrome 能找到虚拟屏幕 | 设置错误 Chrome 无法启动 |
| openclaw.json | `"headless": false` / `"headless": true` | 有头/无头模式切换 | 首次登录必须用 false，登录后可改 true |
| remoteDebuggingPort | `18800` | OpenClaw 通过 CDP 控制浏览器 | Chrome 启动参数必须一致 |
| userDataDir | `~/.config/openclaw-browser-openclaw` | 持久化登录态 | 路径中 nomi 换成自己用户名 |
| systemd DISPLAY | `Environment=DISPLAY=:1` | 服务启动时自动设置显示器 | 必须在 [Service] 段配置 |
| 扩展安装 | `openclaw extension install` | 下载到 `~/.openclaw/extensions/chrome/` | 需在 chrome://extensions/ 手动加载 |
| Relay Token | `cat ~/.openclaw/config/relay-token` | 获取扩展认证 Token | 复制后粘贴到扩展配置中 |

---

### 🛠️ 操作流程

#### 个人资料模式（云服务器）

1. **安装桌面环境**
```bash
sudo apt update
sudo apt install xfce4 xfce4-goodies -y
sudo apt install tigervnc-standalone-server tigervnc-common -y
vncserver :1 -geometry 1920x1080 -depth 24
```

2. **配置 OpenClaw**
修改 `~/.openclaw/openclaw.json`：
```json
{
  "browser": {
    "enabled": true,
    "profile": "openclaw",
    "headless": false,
    "remoteDebuggingPort": 18800,
    "userDataDir": "~/.config/openclaw-browser-openclaw"
  }
}
```

3. **配置 systemd 服务**
```ini
[Unit]
Description=OpenClaw Service
After=network.target

[Service]
Environment=DISPLAY=:1
ExecStartPre=-/usr/bin/pkill -f openclaw
ExecStartPre=-/usr/bin/pkill -f chrome
ExecStart=/home/nomi/.linuxbrew/bin/openclaw run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
⚠️ `nomi` 换成你的用户名。

4. **手动启动 Chrome 并登录**
```bash
export DISPLAY=:1
google-chrome \
  --remote-debugging-port=18800 \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --user-data-dir=/home/nomi/.config/openclaw-browser-openclaw \
  > /tmp/chromium.log 2>&1 &
```
通过 VNC Viewer 连接 `云服务器IP:5901`，在弹出的 Chrome 窗口中手动登录目标网站。

5. **验证**：登录完成后告知 OpenClaw 继续，后续自动复用登录态。

---

#### 扩展模式

1. **安装扩展**
```bash
openclaw extension install
```

2. **Chrome 加载扩展**
   - 打开 `chrome://extensions/`
   - 开启"开发者模式"
   - 点击"加载未打包的扩展程序"
   - 选择 `~/.openclaw/extensions/chrome/` 目录

3. **配置 Token**
```bash
cat ~/.openclaw/config/relay-token
```
复制 Token，粘贴到扩展配置中。

4. **激活扩展**
   - 打开任意目标网页（如 `https://www.x.com`）
   - 点击 OpenClaw Relay 扩展图标
   - 将开关切换为 ON

5. **下指令**：回到 OpenClaw 对话窗口，直接说操作需求。

---

### 💡 具体案例/数据

**案例 1：个人资料模式拉取 scys.com 精华帖**

指令：
> 用个人资料模式打开 `https://scys.com/?filter=essence` 拉取本周的帖子，一个帖子一个帖子的单独发送给我（不要全部总结完，一起发），格式：标题、核心总结、作者、发布日期、帖子链接、飞书文档的原文链接

流程：OpenClaw 提示微信扫码登录 → 手动扫码 → 告知"我已经手动登录，继续" → 逐条输出帖子信息 → 发现帖子链接格式错误 → 补充说明"帖子链接应为文章详情页，形如 `https://scys.com/articleDetail/xq_topic/22811452515421841`" → 纠正后得到正确结果。

**案例 2：扩展模式知乎批量收藏**

指令：`把当前页面前 5 个回答都收藏到「AI」收藏夹。`

OpenClaw 执行：找到第一个回答收藏按钮 → 点击 → 选择「AI」收藏夹确认 → 滚动到第二个回答 → 重复，直到完成 5 个。

**案例 3：扩展模式电商比价**

指令：`提取这个商品的价格、名称，然后打开淘宝搜索同名商品，比较价格。`

返回结果示例：
```
📱 商品名称：iPhone 15 Pro Max 256GB
💵 当前平台价格：¥9,999
🛒 淘宝最低价：¥9,299（省 ¥700）
✨ 建议：淘宝购买更划算
```

---

### 📝 避坑指南

- ⚠️ `DISPLAY` 变量必须设置为 `:1`（VNC 创建的虚拟显示器），设置为 `:0` 会导致 Chrome 无法启动
- ⚠️ systemd 服务文件中必须加 `Environment=DISPLAY=:1`，否则服务启动后 Chrome 找不到显示器
- ⚠️ `ExecStart` 路径中的用户名（`nomi`）必须替换为实际用户名
- ⚠️ Chrome 启动参数 `--remote-debugging-port` 必须与 `openclaw.json` 中的 `remoteDebuggingPort` 一致（均为 18800）
- ⚠️ 首次登录必须用 `headless: false`，登录完成后才能切换为 `headless: true` 后台运行
- ⚠️ 扩展模式必须先打开目标网页，再激活扩展，顺序不能反
- ⚠️ Playwright 模拟登录 X.com 验证码 100% 失败，不要尝试
- ⚠️ 扩展模式直接操作日常账号，安全边界较低，敏感账号（网银、支付）务必用个人资料模式的独立实例

---

### 📊 方案对比总表

| 维度 | HTTP 爬虫 | Playwright | OpenClaw |
|------|----------|-----------|---------|
| 能执行 JS | ❌ 不能 | ✅ 能 | ✅ 能 |
| 能复用登录态 | ❌ 不能 | ⚠️ 需额外配置持久化目录 | ✅ 能 |
| 被检测风险 | ⚠️ 高 | ⚠️ 中高 | ✅ 极低 |
| 稳定性 | ❌ 差 | ⚠️ 一般 | ✅ 稳定 |
| 需要额外成本 | 否 | 否 | 否 |

### 📊 两种浏览器模式对比

| 特性 | 个人资料模式 | 扩展模式 |
|------|------------|---------|
| 原理 | OpenClaw 启动独立 Chrome 实例 | 插件接管当前 Chrome |
| 登录态 | 需手动登录一次，长期保持 | 直接复用已有登录态 |
| 24小时运行 | ✅ 支持 | ❌ 不适合 |
| 安全边界 | 🛡️ 清晰隔离 | ⚠️ 操作日常账号，风险较高 |
| 适合场景 | 定时任务、批量操作、敏感账号、无人值守 | 临时操作、已登录网站、需要现有插件 |

---

### 🏷️ 行业标签

#浏览器自动化 #OpenClaw #云服务器 #CDP #VNC #反爬虫 #AI执行系统 #无头浏览器 #登录态管理 #定时任务

---

---
