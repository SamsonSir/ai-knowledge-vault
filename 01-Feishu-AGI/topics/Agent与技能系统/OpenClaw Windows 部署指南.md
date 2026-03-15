# Agent与技能系统

## 94. [2026-03-03]

## 📕 文章 9


> 文档 ID: `W4mvwnFeDi4xhPkj8bIcaVJAnMh`

**来源**: OpenClaw Windows 部署指南 | **时间**: 2026-03-14 | **原文链接**: `https://github.com/openclaw/openclaw`

---

### 📋 核心分析

**战略价值**: 在无法访问外网的 Windows 环境下，通过离线包 + 跳过 C++ 编译的方式，完整部署 OpenClaw 多 Agent AI 数字员工平台，并打通飞书接入与云端发布能力。

**核心逻辑**:

- **前置环境要求明确**：OS 必须是 Windows 10/11 或 Windows Server；Node.js 必须 ≥ v22.x；包管理器用 pnpm。
- **Node.js 安装有两条路**：有网用官网 `https://nodejs.org/` 下 LTS v22.x；无网或偏好版本管理用 `winget install CoreyButler.NVMforWindows` 装 nvm-windows，再 `nvm install 22 && nvm use 22`。
- **pnpm 必须全局安装**：`npm install -g pnpm`，装完跑 `pnpm setup` 启用自动补全，`pnpm --version` 验证。
- **源码获取两条路**：有网 `git clone https://github.com/openclaw/openclaw.git`；无网用离线包 `openclaw-main.zip` 解压。
- **跳过 C++ 编译是关键坑**：Windows 缺少 C++ 编译库，直接 `pnpm install` 会因 `node-llama-cpp` 编译失败报错。必须用 `pnpm install --ignore-scripts` 跳过本地模型编译，这是 Windows 部署最核心的一步。
- **编译代码用 npm 不用 pnpm**：`npm run dev`，注意这里是 `npm` 而非 `pnpm`。
- **首次配置走 onboard 向导**：`pnpm dev onboard`，按顺序点击，AI 模型优先选免费的跑通流程（推荐 `qwen-code`，登录邮箱认证即可）。
- **启动服务命令**：`pnpm dev gateway`，服务起来后面板地址固定为 `https://127.0.0.1:18789/chat?session=main`。
- **飞书接入需在开发者后台配置长连接**：路径为 开发者后台 → 事件与回调 → 订阅方式 → 使用长连接接收事件/回调，配置成功后终端会打印 `[ws] receive events or callbacks through persistent connection`。
- **多 Agent 形态是核心用法**：多 bot 分工协作，多 Agent 交互实现方式多样，云端部署后可用手机语音操作，不再局限于开发环境。

---

### 🛠️ 操作流程

**1. 准备阶段**

安装 Node.js v22（二选一）：

```powershell
# 方法1：官网下载 LTS v22.x
# https://nodejs.org/

# 方法2：nvm-windows
winget install CoreyButler.NVMforWindows
nvm install 22
nvm use 22
node --version  # 验证显示 v22.x.x
```

安装 pnpm：

```powershell
npm install -g pnpm
pnpm setup
pnpm --version  # 验证
```

**2. 获取源码**

```powershell
# 有网
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 无网：解压 openclaw-main.zip 后 cd 进目录
```

**3. 安装依赖（跳过 C++ 编译）**

```powershell
pnpm install --ignore-scripts
# ⚠️ 不要用 pnpm install，会因 node-llama-cpp 编译失败报错
```

**4. 编译代码**

```powershell
npm run dev
```

**5. 首次配置**

```powershell
pnpm dev onboard
# 按向导顺序点击，AI 模型选 qwen-code（免费，邮箱认证）
```

**6. 启动服务**

```powershell
pnpm dev gateway
```

访问面板：`https://127.0.0.1:18789/chat?session=main`

---

### 📦 配置/工具详表

| 模块/功能 | 关键命令/路径 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 查看帮助 | `pnpm dev --help` | 列出所有子命令 | — |
| 查看状态 | `pnpm dev status` | 显示各服务运行状态 | — |
| 健康检查 | `pnpm dev health` | 返回各组件健康状态 | Gateway 启动后若健康检查失败，检查端口占用 |
| 启动控制面板 | `pnpm dev dashboard` | 自动打开浏览器 | — |
| 安全审计 | `pnpm dev security audit` | 输出安全审计报告 | — |
| 更新 OpenClaw | `pnpm dev update` | 拉取最新版本 | — |
| 配置修改 | `pnpm dev configure` | 进入配置界面 | — |
| 飞书接入 | 开发者后台 → 事件与回调 → 订阅方式 → 长连接 | 终端打印 `[ws]` 确认连接 | 需要自建或飞书应用权限 |
| 面板地址 | `https://127.0.0.1:18789/chat?session=main` | Web 对话界面 | 端口 18789 固定 |

---

### 📝 避坑指南

- ⚠️ **直接 `pnpm install` 必报错**：Windows 缺 C++ 编译环境，`node-llama-cpp` 会编译失败，必须加 `--ignore-scripts` 跳过。
- ⚠️ **Feishu 插件报 `spawn EINVAL`**：以管理员身份运行 PowerShell，或在 onboard 阶段跳过飞书配置，后续再单独接入。
- ⚠️ **Gateway 健康检查失败**：检查 18789 端口是否被占用，或防火墙是否拦截。
- ⚠️ **首次模型配置别选重型本地模型**：先用 `qwen-code` 等免费云端模型跑通整个流程，再考虑本地模型。

---

### 🔗 参考文档

- 官方文档：`https://docs.openclaw.ai/`
- GitHub：`https://github.com/openclaw/openclaw`
- 社区案例：`https://openclaw.ai/showcase`

---

### 🏷️ 行业标签

#OpenClaw #多Agent #AI数字员工 #Windows部署 #飞书接入 #本地部署 #pnpm #Node22

---

---
