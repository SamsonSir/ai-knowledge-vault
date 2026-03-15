# AI学习与效率工具

## 14. [2026-03-10]

## 📗 文章 2


> 文档 ID: `U2v9wBiM5iVlfOkPZW1cPcTMnsd`

**来源**: VPS 到手后的第一个小时：从裸机到安全可用的完整初始化指南 | **时间**: 2026-01 | **原文链接**: `https://blog.ittinker.com/posts/202...`

---

### 📋 核心分析

**战略价值**: 新 VPS 上线即遭扫描，本文提供从裸机到安全可用的完整 10 步加固 SOP，覆盖密钥登录、防火墙、BBR、fail2ban 全链路。

**核心逻辑**:

- VPS 上线即暴露：默认 22 端口 + root 用户 + 密码登录，全球自动化脚本 7×24 小时扫描爆破，无任何加固的服务器平均存活时间极短
- 先更新再部署：新镜像可能滞后数月，`apt update && apt full-upgrade -y` 必须是第一步，内核更新后需 `reboot`
- root 不能日常用：`adduser ittinker` + `usermod -aG sudo ittinker`，日常用普通用户，sudo 按需提权，防止 `rm -rf /` 级误操作
- 密钥 > 密码：ed25519 密钥对理论上无法暴力破解，密码可以；生成后必须测试密钥登录成功，再禁用密码登录，顺序不能反
- SSH 端口改非 22：选 1024–65535 之间任意端口（如 22000），直接让 99% 的无差别扫描器失效；轻量服务器可能不支持，需在云控制台操作
- UFW 默认拒绝入站：`ufw default deny incoming` + 只放行 22000/80/443，最小化攻击面
- BBR 两行搞定：写入 `/etc/sysctl.conf` 后 `sysctl -p` 即生效，高延迟/不稳定网络下效果最明显
- fail2ban 自动封禁：3 次失败 → 封禁 1 小时，监控 `/var/log/auth.log`，无需人工干预
- Cloudflare Only 模式（可选）：只允许 Cloudflare IP 段访问 80/443，配合 cron 每周自动更新 IP 段
- 时区必改：默认 UTC 导致日志时间对不上，`timedatectl set-timezone Asia/Shanghai` 一行解决

---

### 🎯 关键洞察

**为什么顺序很重要（原因 → 动作 → 结果）**:

1. 先测试密钥登录 → 再禁用密码登录：如果顺序反了，密钥配置有误会把自己锁在门外
2. 先开放新 SSH 端口 → 再启用 UFW：UFW 启用前没放行新端口，直接断连
3. 先备份配置 → 再修改：`cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak`，改错了能回滚

**轻量服务器的坑**:
`netstat -lntp | grep :22` 如果输出 `LISTEN 1/init`，说明 22 端口由平台层代理，改 `sshd_config` 无效。此时重点转向：禁 root 登录 + 密钥登录 + fail2ban，安全性依然足够。

---

### 📦 配置/工具详表

| 模块 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|------|-------------|---------|-----------|
| SSH 密钥生成 | `ssh-keygen -t ed25519 -C "your@email.com"` | 生成 `id_ed25519` + `id_ed25519.pub` | 私钥绝不外传；旧系统不支持 ed25519 用 `rsa -b 4096` |
| 公钥上传 | `ssh-copy-id -i ~/.ssh/id_ed25519.pub user@ip` | 自动写入 `authorized_keys` | 手动复制时 `.ssh` 权限必须 700，`authorized_keys` 必须 600 |
| SSH 加固配置 | 见下方代码块 | 禁密码、禁 root、改端口 | 改完先新窗口测试，不要关旧窗口 |
| UFW | `ufw default deny incoming` + 按需 allow | 最小化暴露端口 | 启用前必须先放行 SSH 端口，否则断连 |
| BBR | 写入 sysctl.conf + `sysctl -p` | TCP 拥塞控制优化 | 验证：`sysctl net.ipv4.tcp_congestion_control` 输出 `bbr` |
| fail2ban | `[sshd]` maxretry=3, bantime=3600 | 自动封禁爆破 IP | 端口要和 SSH 实际端口一致 |
| 时区 | `timedatectl set-timezone Asia/Shanghai` | 日志时间正确 | 改完用 `date` 验证 |

---

### 🛠️ 操作流程

**1. 准备阶段**

```bash
# 首次登录
ssh root@你的服务器IP

# 了解机器
cat /etc/os-release && uname -r && free -h && df -h

# 更新系统（可能需要几分钟）
apt update && apt full-upgrade -y && apt autoremove -y && apt autoclean

# 检查是否需要重启
cat /var/run/reboot-required 2>/dev/null && echo ">>> 需要重启" || echo ">>> 无需重启"
# 需要则执行：reboot

# 安装基础工具
apt install -y sudo curl wget git vim htop tree unzip net-tools ufw fail2ban neofetch
```

**2. 核心执行**

```bash
# === 创建普通用户 ===
adduser ittinker          # 按提示设密码，其余回车跳过
usermod -aG sudo ittinker

# === 本地生成密钥（在你的电脑上执行）===
ssh-keygen -t ed25519 -C "your@email.com"
ssh-copy-id -i ~/.ssh/id_ed25519.pub ittinker@你的服务器IP

# === 测试密钥登录（新开终端）===
ssh ittinker@你的服务器IP   # 不需要密码则成功

# === SSH 加固（服务器上）===
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
nano /etc/ssh/sshd_config
```

`sshd_config` 关键修改项：

```
Port 22000                        # 改为非标准端口
PermitRootLogin no                # 禁止 root 登录
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
PasswordAuthentication no         # 禁用密码（密钥测试成功后再改）
Protocol 2
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
```

```bash
# 保存：Ctrl+O → 回车 → Ctrl+X
systemctl restart sshd.service

# 新窗口测试新端口
ssh -p 22000 ittinker@你的服务器IP

# === UFW 防火墙 ===
ufw default deny incoming
ufw default allow outgoing
ufw allow 22000/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw enable   # 输入 y 确认

# === BBR 加速 ===
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p

# === fail2ban ===
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
vim /etc/fail2ban/jail.local
```

`jail.local` 中 `[sshd]` 部分：

```ini
[sshd]
enabled = true
port = 22000
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

```bash
systemctl restart fail2ban && systemctl enable fail2ban

# === 时区 ===
timedatectl set-timezone Asia/Shanghai
date   # 验证
```

**3. 验证与优化**

```bash
# 全量检查
apt update && apt list --upgradable          # 系统已更新
sudo whoami                                  # 输出 root = sudo 正常
grep PasswordAuth /etc/ssh/sshd_config       # PasswordAuthentication no
grep Port /etc/ssh/sshd_config               # 你设置的端口
ufw status verbose                           # Status: active
sysctl net.ipv4.tcp_congestion_control       # = bbr
lsmod | grep bbr                             # tcp_bbr 已加载
systemctl status fail2ban                    # active (running)
fail2ban-client status sshd                  # 监控状态
timedatectl                                  # Asia/Shanghai
```

---

### 📦 可选：Cloudflare Only 模式

```bash
# 下载脚本（仅限域名已接入 Cloudflare CDN）
wget -O ~/.cloudflare-ufw.sh https://gist.githubusercontent.com/Xm798/12560579ce11f62027ea8da1fae37456/raw/b07ac8cfe09badf02fc70e2d8bc2da68cabbda50/cloudflare-ufw.sh
chmod +x ~/.cloudflare-ufw.sh
~/.cloudflare-ufw.sh

# 设置每周一凌晨自动更新 Cloudflare IP 段
(crontab -l 2>/dev/null; echo "0 0 * * 1 /root/.cloudflare-ufw.sh > /dev/null 2>&1") | crontab -
```

---

### 📦 可选：SSH Config 多服务器管理（本地电脑）

```bash
vim ~/.ssh/config
```

```
Host vps1
    HostName 192.168.1.100
    User ittinker
    Port 22000
    IdentityFile ~/.ssh/id_ed25519

Host vps2
    HostName 192.168.1.101
    User admin
    Port 22222
    IdentityFile ~/.ssh/id_ed25519

Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
```

之后直接 `ssh vps1` 即可。

---

### 📦 一键初始化脚本（熟练后使用）

```bash
#!/bin/bash
# VPS 初始化脚本，以 root 身份运行
set -e

NEW_USER="ittinker"
NEW_SSH_PORT="22000"
TIMEZONE="Asia/Shanghai"

echo "=== VPS 初始化脚本 ==="

echo "[1/8] 更新系统..."
apt update && apt upgrade -y

echo "[2/8] 安装基础工具..."
apt install -y sudo curl wget git vim htop tree unzip net-tools ufw fail2ban neofetch

echo "[3/8] 创建用户 $NEW_USER..."
if id "$NEW_USER" &>/dev/null; then
    echo "用户已存在，跳过"
else
    adduser --gecos "" $NEW_USER
    usermod -aG sudo $NEW_USER
fi

echo "[4/8] 配置 SSH 目录..."
mkdir -p /home/$NEW_USER/.ssh
chmod 700 /home/$NEW_USER/.ssh
touch /home/$NEW_USER/.ssh/authorized_keys
chmod 600 /home/$NEW_USER/.ssh/authorized_keys
chown -R $NEW_USER:$NEW_USER /home/$NEW_USER/.ssh

echo ">>> 请将你的公钥粘贴到下面（粘贴后按 Ctrl+D 结束）："
cat >> /home/$NEW_USER/.ssh/authorized_keys

echo "[5/8] 修改 SSH 配置..."
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sed -i "s/^#*Port .*/Port $NEW_SSH_PORT/" /etc/ssh/sshd_config
sed -i "s/^#*PermitRootLogin .*/PermitRootLogin no/" /etc/ssh/sshd_config
sed -i "s/^#*PasswordAuthentication .*/PasswordAuthentication no/" /etc/ssh/sshd_config
sed -i "s/^#*PermitEmptyPasswords .*/PermitEmptyPasswords no/" /etc/ssh/sshd_config

echo "[6/8] 配置防火墙..."
ufw default deny incoming
ufw default allow outgoing
ufw allow $NEW_SSH_PORT/tcp
ufw allow 80/tcp
ufw allow 443/tcp
echo "y" | ufw enable

echo "[7/8] 开启 BBR..."
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p

echo "[8/8] 设置时区..."
timedatectl set-timezone $TIMEZONE

systemctl restart sshd

echo "=========================================="
echo "  ✅ 初始化完成！"
echo "  新 SSH 端口: $NEW_SSH_PORT"
echo "  新用户: $NEW_USER"
echo "  时区: $TIMEZONE"
echo "  登录命令: ssh -p $NEW_SSH_PORT $NEW_USER@$(curl -s ifconfig.me 2>/dev/null || echo '你的IP')"
echo "  ⚠️ 先测试新配置能登录，再关闭当前终端！"
echo "=========================================="
```

---

### 💡 具体案例/数据

| 步骤 | 做了什么 | 为什么重要 |
|------|---------|-----------|
| 更新系统 | 安装最新补丁 | 修复已知漏洞 |
| 创建新用户 | 不再直接用 root | 减少误操作风险 |
| SSH 密钥 | 用密钥替代密码 | 无法被暴力破解 |
| 修改端口 | 躲开默认 22 | 减少被扫描概率 |
| 禁用密码 | 只允许密钥登录 | 彻底杜绝密码攻击 |
| 禁用 root | root 不能直接登录 | 增加攻击难度 |
| UFW 防火墙 | 只开放必要端口 | 减少攻击面 |
| BBR 加速 | 优化网络性能 | 提升访问速度 |
| fail2ban | 自动封禁恶意 IP | 防止持续攻击 |

做完以上全部，安全性超过 90% 的 VPS。

---

### 📝 避坑指南

- ⚠️ 密钥登录测试成功前，绝对不要关闭原终端窗口，也不要禁用密码登录
- ⚠️ UFW enable 前必须先 `ufw allow 你的SSH端口`，否则直接断连
- ⚠️ `authorized_keys` 权限必须是 600，`.ssh` 目录必须是 700，权限不对 SSH 直接拒绝密钥
- ⚠️ 轻量服务器（如腾讯云轻量）SSH 由平台层代理，`netstat -lntp | grep :22` 输出 `LISTEN 1/init` 则改端口无效，转而强化其他措施
- ⚠️ fail2ban 把自己封了：用 VNC 登录后执行 `fail2ban-client set sshd unbanip 你的IP`，并在 `jail.local` 加 `ignoreip = 127.0.0.1/8 ::1 你的IP`
- ⚠️ Cloudflare Only 模式前提：域名必须已接入 Cloudflare CDN，否则会把正常流量也挡掉
- ⚠️ 定期维护：`lastb` 查失败登录，`last` 查成功登录，重要配置修改前先备份

---

### 🏷️ 行业标签
#VPS安全 #Linux运维 #SSH加固 #UFW防火墙 #fail2ban #BBR加速 #服务器初始化 #DevOps

---

---
