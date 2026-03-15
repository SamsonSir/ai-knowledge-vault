# AI编程与开发工具

## 14. [2026-01-27]

## 📒 文章 7


> 文档 ID: `LUQTwefK0iPCiGkaOylcLoVPngg`

**来源**: Windows系统Claude Code小白安装教程 | **时间**: 2026-01-27 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: Windows 用户无需 Mac 模拟环境，直接在 PowerShell/终端中完整安装并一键启动 Claude Code 的可复刻操作手册。

**核心逻辑**:
- 前置条件：需要科学上网环境 + Git for Windows + Node.js v22.13.0 LTS (Windows x64 .msi)
- Node.js 安装后必须手动将路径写入系统环境变量，否则终端无法识别 `node` 命令
- 环境变量配置命令：`[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\node", "User")`，每次重装或重配后都要重新执行
- 配置完环境变量后必须关闭所有终端窗口再重开，否则变量不生效，`node -v` 无法返回版本号
- Claude Code 安装命令：`npm install -g @anthropic-ai/claude-code`，安装后用 `claude --version` 验证
- IP 被 Anthropic 拒绝时（报错含 `app-unavailable-in-region`），需在终端手动设置代理端口再安装，端口号因科学上网工具而异
- 设置代理后安装：先 `$Env:HTTP_PROXY="https://127.0.0.1:你的端口"` + `$Env:HTTPS_PROXY="https://127.0.0.1:你的端口"`，再执行 npm 安装
- 代理端口每次启动 Claude Code 都需重新配置，因此非正常 IP 用户必须用含代理设置的 .bat 文件启动，不能裸跑 `claude`
- API Key 来源推荐智谱 BigModel（`https://bigmodel.cn/`），新账号注册赠 2000 万 tokens，绑定企业微信再赠 2000 万 tokens
- 环境配置工具：`npx @z_ai/coding-helper`，用于配置 API Key 和界面语言（可切换中文），通过上下键选择颜色主题后直接进入对话

---

### 🛠️ 操作流程

**1. 准备阶段**

- 确保科学上网可用
- 安装 Git for Windows
- 下载并安装 Node.js v22.13.0 LTS (Windows x64 .msi)
  - 若 .msi 无法双击打开：按 `Win+X` → 终端（非管理员）→ 输入 `msiexec /i `（注意 /i 后有空格）→ 将 .msi 文件拖入窗口 → 回车 → 弹出安装窗口后一路 Next

**2. 配置环境变量**

按 `Win+X` → 终端，执行：
```powershell
[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\node", "User")
```
关闭所有终端窗口，重新打开，验证：
```powershell
node -v
```
显示版本号即成功。

**3. 安装 Claude Code**

正常 IP：
```powershell
npm install -g @anthropic-ai/claude-code
```

IP 被拒（报错含 `app-unavailable-in-region`）：
```powershell
# 1. 设置代理（端口号改成你自己的）
$Env:HTTP_PROXY="https://127.0.0.1:你的端口"
$Env:HTTPS_PROXY="https://127.0.0.1:你的端口"

# 2. 安装
npm install -g @anthropic-ai/claude-code
```
> 端口号查找方法：截图科学上网工具界面发给 AI，让 AI 识别端口号。

安装后验证：
```powershell
claude --version
```

**4. 配置 API Key（智谱 BigModel）**

- 进入 `https://bigmodel.cn/` 注册账号
- 控制台 → API Key → 新建，命名为 `Claude code`
- 终端执行：
```powershell
npx @z_ai/coding-helper
```
- 界面语言改为中文 → 上下键选择 API Key → 粘贴 Key → Enter → 选择颜色主题 → Enter → 进入对话

**5. 创建一键启动 .bat 文件**

桌面右键 → 新建文本文档 → 粘贴以下内容：

正常 IP 版本：
```bat
@echo off
chcp 65001 >nul

echo ==========================================
echo 正在启动 Claude Code (直连模式)...
echo ==========================================

cd /d "%USERPROFILE%\Desktop"
if not exist "Claude_Work" mkdir "Claude_Work"
cd "Claude_Work"
echo [状态] 已进入安全工作区: Desktop\Claude_Work

echo ------------------------------------------
call claude

if %errorlevel% neq 0 (
    echo.
    echo [错误] 启动失败，请检查网络或安装情况。
    pause
)
```

非正常 IP（需代理）版本：
```bat
@echo off
chcp 936 >nul

echo ==========================================
echo 正在准备启动 Claude Code...
echo ==========================================

set HTTP_PROXY=https://127.0.0.1:你的端口
set HTTPS_PROXY=https://127.0.0.1:你的端口
echo [1/3] 代理已连接 (Port: 你的端口)

cd /d "%USERPROFILE%\Desktop"
if not exist "Claude_Work" mkdir "Claude_Work"
cd "Claude_Work"
echo [2/3] 已进入安全工作区: Desktop\Claude_Work

echo [3/3] 正在启动，请稍候...
echo ------------------------------------------
call claude

if %errorlevel% neq 0 (
    echo.
    echo !!!!!!!!!!! 出错了 !!!!!!!!!!!
    echo 请截图报错信息发给 AI
    cmd /k
) else (
    pause
)
```

保存时：文件 → 另存为 → 编码选 **ANSI**（非 UTF-8，否则闪退）→ 文件名后缀改为 `.bat`

之后双击 .bat 文件即可一键启动。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Node.js 安装 | v22.13.0 LTS Windows x64 .msi | 提供 npm 运行环境 | .msi 无法双击时用 `msiexec /i` 拖拽安装 |
| 环境变量 | `SetEnvironmentVariable("Path", $env:Path + ";C:\node", "User")` | 终端识别 node 命令 | 配置后必须重开终端才生效 |
| Claude Code 安装 | `npm install -g @anthropic-ai/claude-code` | 全局安装 claude 命令 | IP 被拒时需先设代理再安装 |
| 代理设置 | `$Env:HTTP_PROXY` / `$Env:HTTPS_PROXY` 指向 127.0.0.1:端口 | 绕过 IP 封锁 | 每次启动都需重新设置，建议写入 .bat |
| API Key 配置 | `npx @z_ai/coding-helper` | 图形化配置 Key 和主题 | 需联网下载，首次运行较慢 |
| 一键启动 | .bat 文件双击 | 免终端直接启动 | 编码必须存为 ANSI，UTF-8 会闪退 |
| 工作区 | 自动创建 `Desktop\Claude_Work` | 避免每次弹出桌面权限确认 | 路径写死在 bat 里，换桌面路径需手动改 |

---

### 📝 避坑指南

- ⚠️ 终端选择：用 `Win+X` → "终端"，不要选"终端管理员"，管理员模式无法拖拽文件路径
- ⚠️ 环境变量不生效：配置后必须关闭所有终端窗口再重开，不能在同一窗口验证
- ⚠️ .bat 文件编码：必须另存为 ANSI 格式，默认 UTF-8 会导致启动时闪退
- ⚠️ IP 被拒报错特征：错误信息含 `app-unavailable-in-region` 或 `<!DOCTYPE html>` HTML 内容，说明是 IP 问题而非安装问题
- ⚠️ 代理端口每次失效：非正常 IP 用户每次启动都需重新 set 代理，必须用含代理的 .bat 版本，不能直接在终端输 `claude`
- ⚠️ 智谱 API Key 配置工具：`npx @z_ai/coding-helper` 需要在有网络的环境下运行，首次会下载依赖

---

### 🏷️ 行业标签
#ClaudeCode #Windows安装 #NodeJS #智谱BigModel #开发环境配置 #代理设置 #bat脚本

---

---
