# Vibe_Coding实践

## 2. [2026-01-10]

## 📔 文章 5


> 文档 ID: `ALCWwTFOhiC2SzkrUiScSQqWnXb`

**来源**: 我把 Mac 留在书房，却在咖啡馆用 iPhone 远程指挥 Vibe Coding Agent 大军 | **时间**: 2026-01-10 | **原文链接**: `https://mp.weixin.qq.com/s/45mq-EK5...`

---

### 📋 核心分析

**战略价值**: 用 iTerm2 + tmux + Mosh + Tailscale + Bark + Codex Hook 六件套，实现 Mac 无人值守、iPhone 随时接管、AI 任务完成主动推送的 Vibe Coding 远程指挥体系。

**核心逻辑**:
- 传统 SSH 会话在网络切换或断线后进程即死，tmux 让会话与终端窗口解耦，关掉 App 进程照跑
- Tailscale 提供跨网络的固定私有 IP，解决动态 IP 和 NAT 穿透问题，是 Mosh 连接的前提
- Mosh 基于 UDP，对丢包和网络切换有天然容忍，比 TCP-based SSH 更适合移动网络
- Bark 通过 curl 调用私有 Device Key 推送通知，无需轮询，AI 跑完主动震动手机
- Codex 的 `notify` Hook 在每轮任务结束后自动触发脚本，形成"任务完成 → 推送 → 回场"闭环
- tmux 开启鼠标支持后，手机端 Termius 可直接点击切换 Pane/Window，无需记快捷键
- 所有路径使用绝对路径（如 `/opt/homebrew/bin/mosh-server`），避免远程环境 PATH 不一致导致命令找不到
- Bark 通知内容需 URL encode（用 `python3 urllib.parse.quote`），否则中文内容会乱码或请求失败
- Mac 安装 Amphetamine 并设置"连接电源时永不休眠"，防止后端休眠导致 SSH/Mosh 断连
- 整套方案组件化，每层职责单一：iTerm2 管界面、tmux 管持久化、Mosh+Tailscale 管连接、Bark 管感知、Codex Hook 管触发

---

### 🛠️ 操作流程

**第一阶段：升级终端界面 (iTerm2)**

```bash
brew install --cask iterm2
```

配置路径：`Cmd + ,` → Profiles → Colors → 右下角选 `Solarized Dark`
配置路径：Profiles → Window → Transparency 调至 `15%`，开启 `Blur`

---

**第二阶段：持久化会话 (tmux)**

```bash
brew install tmux
```

写入配置文件：

```bash
cat <<EOF > ~/.tmux.conf
# 开启鼠标支持 (手机端可直接点击切换窗口)
set -g mouse on
# 解决 256 色显示问题
set -g default-terminal "screen-256color"
# 状态栏样式美化
set -g status-style bg='#282c34',fg='#abb2bf'
set -g status-left '#[fg=green,bold] [#S] '
set -g status-right '#[fg=cyan] %H:%M '
set -g status-justify centre
# 调整分屏快捷键：使用 | 和 -
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
EOF
```

生效：
```bash
tmux source-file ~/.tmux.conf
```

---

**第三阶段：抗丢包连接 (Mosh + Tailscale)**

```bash
brew install mosh
```

| 步骤 | 操作 |
|------|------|
| 1 | Mac 和 iPhone 均安装 Tailscale，登录同一账号 |
| 2 | Tailscale 分配固定私有 IP，记录 Mac 的 IP |
| 3 | 手机端 Termius → 新建主机 → 协议选 Mosh |
| 4 | Mosh Server Command 填入绝对路径 |

Termius 中 Mosh Server Command 必须填：
```
LANG=en_US.UTF-8 /opt/homebrew/bin/mosh-server new
```

---

**第四阶段：任务完成推送 (Bark)**

1. iPhone 下载 Bark App，复制首页 Device Key
2. Mac 创建通知脚本：

```bash
cat <<EOF > ~/notify.sh
#!/bin/bash
KEY="你的Bark_Key"
ENCODED_CONTENT=\$(python3 -c "import urllib.parse; print(urllib.parse.quote('\$1'))")
curl -s "https://api.day.app/\$KEY/Codex通知/\$ENCODED_CONTENT"
EOF
chmod +x ~/notify.sh
```

---

**第五阶段：Codex Hook 自动触发**

打开配置文件：
```bash
code ~/.codex/config.toml
```

写入：
```toml
# 当 Codex 完成一轮对话或任务时，调用此命令
notify = ["/Users/你的用户名/notify.sh", "AI 任务执行完毕，请回场检阅"]
```

---

### 📦 配置/工具详表

| 模块 | 关键设置/代码 | 预期效果 | 注意事项 |
|------|-------------|---------|---------|
| iTerm2 | Solarized Dark + Transparency 15% + Blur | 磨砂玻璃质感终端 | 纯美化，可跳过 |
| tmux | `set -g mouse on` | 手机可点击切换 Pane | 配置后需 `source-file` 生效 |
| Tailscale | Mac + iPhone 同账号 | 固定私有 IP，穿透 NAT | Mosh 连接的前提，必须先装 |
| Mosh | Server Command 用绝对路径 | UDP 抗丢包，网络切换不断连 | 路径必须是 `/opt/homebrew/bin/mosh-server` |
| Bark | Device Key + URL encode | AI 完成主动推送 | 中文必须 encode，否则乱码 |
| Codex Hook | `notify` 字段填绝对路径 | 每轮任务结束自动触发脚本 | 用户名替换为实际值 |
| Amphetamine | 连接电源时永不休眠 | 后端始终在线 | 不装则 Mac 休眠后断连 |

---

### 📦 tmux 核心快捷键清单

| 动作 | 快捷键 |
|------|--------|
| 创建新窗口 (Window) | `Ctrl+b` 然后 `c` |
| 左右垂直分屏 (Pane) | `Ctrl+b` 然后 `\|` |
| 上下水平分屏 (Pane) | `Ctrl+b` 然后 `-` |
| 暂时全屏化当前分屏 | `Ctrl+b` 然后 `z`（再按 `z` 还原） |
| 脱离当前会话 (Detach) | `Ctrl+b` 然后 `d`（进程继续跑） |
| 查看窗口列表 | `Ctrl+b` 然后 `w` |

---

### 💡 完整工作流闭环

```
手机打开 Termius
  → 自动执行: tmux a -t coding || tmux new -s coding
  → 对 Codex 下达任务（如："分析当前驱动的内存泄漏并尝试修复"）
  → Ctrl+b 然后 d 脱离会话，关掉手机 App
  → Mac 全力运行，Codex 执行任务
  → 任务完成 → notify.sh 触发 → Bark 推送震动
  → 点开通知 → Termius 回到 tmux 现场，日志和修改原位等待
```

---

### 📝 避坑指南

- ⚠️ 脚本无法执行：运行 `chmod +x ~/notify.sh` 赋予执行权限
- ⚠️ Mosh 连接失败：Server Command 必须用绝对路径 `/opt/homebrew/bin/mosh-server`，不能依赖 PATH
- ⚠️ Bark 推送中文乱码：必须用 `python3 urllib.parse.quote` 对内容做 URL encode
- ⚠️ Codex notify 路径：`config.toml` 中填写 `/Users/你的用户名/notify.sh` 完整绝对路径
- ⚠️ Mac 后端断连：安装 Amphetamine，设置"连接电源时永不休眠"

---

### 🏷️ 行业标签
#VibeCoding #远程开发 #tmux #Mosh #Tailscale #Bark #Codex #移动端开发 #AI-Agent #终端工作流

---

---
