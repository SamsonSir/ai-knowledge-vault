# AI编程与开发工具

## 37. [2026-02-24]

## 📚 文章 8


> 文档 ID: `VpQawzteDi9IbnkV0yscnqi2nDd`

**来源**: 风叶：Claude Sync：让你的 Claude Code 配置在多台设备间无缝同步 | **时间**: 2026-03-13 | **原文链接**: 点击这里

---

### 📋 核心分析

**战略价值**: 用 Git 私有仓库作为中间层，实现 Claude Code 的 skills/plugins/settings 跨设备无缝同步，5 分钟完成新机迁移。

**核心逻辑**:
- 本质是 Git 封装工具：所有同步操作底层都是 `git push/pull`，配置存在 GitHub 私有仓库，不依赖任何第三方云服务
- 同步粒度可控：`skills`、`plugins`、`settings` 默认开启，`projects`、`history` 默认关闭，通过 `config.json` 的 `include` 字段精确控制
- 4 种冲突策略：`ask`（交互询问，推荐）、`local`（保留本地）、`remote`（使用远程）、`newest`（按修改时间取最新），通过 `sync.conflictStrategy` 字段配置
- 安全默认值：默认排除 `.env`、`*.key`、`secrets/`、`*.secret`，可通过 `claude-config-sync config exclude` 追加规则
- Watch 模式：`claude-config-sync watch start` 监听 `~/.claude` 目录变化，5000ms debounce 后自动触发同步
- 自动备份机制：每次 pull/sync 操作前自动创建备份，存储在 `~/.claude-config-sync/backups/`，可通过 `--keep N` 控制保留数量
- 配置文件统一管理：所有配置存于 `~/.claude-config-sync/config.json`，Git 仓库克隆在 `~/.claude-config-sync/repo/`
- 支持多仓库隔离：工作环境和个人环境可分别 `init` 指向不同仓库，互不干扰
- cron 定时同步：Mac/Linux 可用 `0 * * * * claude-config-sync sync` 实现每小时自动同步
- 支持 `.syncignore`：在 `~/.claude-sync/.syncignore` 自定义忽略规则，语法同 `.gitignore`

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 选择性同步 | `"include": {"skills":true,"plugins":true,"settings":true,"projects":false,"history":false}` | 只同步指定类型文件 | projects/history 默认关闭，按需开启 |
| 冲突策略 | `claude-config-sync config set sync.conflictStrategy newest` | 自动取最新修改版本 | 多人协作推荐用 `ask` 避免静默覆盖 |
| 自动同步间隔 | `claude-config-sync config set sync.syncIntervalMinutes 15` | 每 15 分钟自动同步 | 默认 30 分钟，autoSync 默认 false 需手动开启 |
| 排除敏感文件 | `claude-config-sync config exclude "*.pem"` | 阻止该类文件被同步 | 默认已排除 .env/*.key/secrets/*.secret |
| Watch 模式 | `claude-config-sync watch start` | 文件变动 5 秒后自动同步 | Ctrl+C 停止，或用 `watch stop` |
| 备份清理 | `claude-config-sync backup clean --keep 5` | 只保留最近 5 个备份 | 备份路径：`~/.claude-config-sync/backups/` |

---

### 🛠️ 操作流程

**1. 安装**

```bash
# 方式一：npm 全局安装（推荐）
npm install -g claude-config-sync

# 方式二：源码安装
git clone https://github.com/balingsisi/claude-config-sync-tool.git
cd claude-config-sync-tool
npm install
npm run build
npm link

# 验证
claude-config-sync --version  # 应输出 0.1.0
```

**2. 创建 GitHub 私有仓库**
- 访问 GitHub → New repository
- 命名 `claude-config`，选 **Private**，勾选 "Add a README file"
- 建议用 SSH 协议（比 HTTPS 更安全）

**3. 初始化同步（首台设备）**

```bash
claude-config-sync init --repo git@github.com:你的用户名/claude-config.git
```

交互过程：
```
? Git 仓库 URL: git@github.com:你的用户名/claude-config.git
? 分支名称: main
? 您想要同步什么内容？ ✓ skills ✓ plugins ✓ settings ○ projects
? 冲突解决策略: Ask (interactive)
✓ 首次推送完成：15 个文件
```

**4. 日常使用**

```bash
claude-config-sync push    # 推送本地改动
claude-config-sync pull    # 拉取远程改动
claude-config-sync sync    # 双向同步（最常用）
claude-config-sync status  # 查看状态
```

**5. 迁移到新设备（3 步完成）**

```bash
npm install -g claude-config-sync
claude-config-sync init --repo git@github.com:你的用户名/claude-config.git
claude-config-sync pull
# 完成，所有配置恢复
```

---

### 💡 具体案例/数据

**案例 1：家 → 公司**
```
家中：安装新 AI 写作技能 → claude-config-sync push
公司：claude-config-sync pull → 新技能自动出现
```

**案例 2：换新电脑**
```
旧电脑：claude-config-sync push（最后一次）
新电脑：npm install → init → pull → 完成，全部配置恢复
```

**案例 3：团队协作**
```
个人配置 → 个人私有仓库 claude-config
团队共享配置 → 组织私有仓库 team-claude-config
两套仓库分别 init，互不干扰
```

**定时同步（Mac/Linux）**
```bash
crontab -e
# 添加：
0 * * * * claude-config-sync sync   # 每小时同步一次
```

---

### 📝 完整配置文件（`~/.claude-config-sync/config.json`）

```json
{
  "version": "1.0.0",
  "sync": {
    "repository": "git@github.com:user/claude-config.git",
    "branch": "main",
    "autoSync": false,
    "syncIntervalMinutes": 30,
    "include": {
      "skills": true,
      "plugins": true,
      "settings": true,
      "projects": false,
      "history": false,
      "customPatterns": []
    },
    "excludePatterns": [
      ".env",
      "*.key",
      "secrets/",
      "*.secret"
    ],
    "conflictStrategy": "ask"
  }
}
```

---

### 📝 避坑指南

- ⚠️ SSH 未配置会报 "Permission denied"：需先 `ssh-keygen -t ed25519 -C "email"` → `ssh-add ~/.ssh/id_ed25519` → 将公钥添加到 `https://github.com/settings/keys`
- ⚠️ 不要用公开仓库：配置文件可能含有路径、习惯等隐私信息，必须用 Private 仓库
- ⚠️ API Token / 密码不要写进任何配置文件：默认排除规则只覆盖常见格式，自定义文件需手动 `config exclude`
- ⚠️ Watch 模式不会自动后台运行：进程退出即停止，需配合 `pm2` 或 `nohup` 实现持久化
- ⚠️ `sync` 命令是先 pull 后 push：如果远程有冲突文件，会先触发冲突解决流程再推送

---

### 🏷️ 行业标签
#ClaudeCode #开发工具 #配置同步 #Git #效率工具 #开源

---

---
