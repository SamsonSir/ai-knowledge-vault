# Agent与技能系统

## 37. [2026-01-28]

## 📚 文章 8


> 文档 ID: `EyFmwTbDuiqBpYk4pexc4RwLnRe`

**来源**: 成峰：我做了 Claude Code 的Raycast，Skills 1秒启动 | **时间**: 2026-01-28 | **原文链接**: `https://mp.weixin.qq.com/s/78NxShIn...`

---

### 📋 核心分析

**战略价值**: 用 Swift 编译的可执行文件 + Claude Code Skills 机制，实现全局快捷键 1 秒唤起任意 Skill，彻底消灭「打开终端 → 启动 claude → 等待 → 输入命令」的 4 步摩擦。

**核心逻辑**:

- **痛点量化**：作者每天调用 Claude Code Skills 近 100 次，每次需走 4 步（打开终端 → 输入 `claude` → 等 3 秒启动 → 输入 `/skill-name`），累计摩擦极高
- **设计决策**：不做传统 macOS App，而是做可执行文件（executable），目的是让 Claude Code 本身能安装、运行、调试、修改它，保持「可随时改」的源码形态
- **触发方式**：全局快捷键 `Option+Space`，在任意应用内均可唤起，不打断当前工作流
- **Skill 自动发现**：自动扫描 `~/.claude/skills/` 目录下所有 Skill，无需手动配置，装完即用
- **智能排序**：模糊搜索匹配 Skill 名称，最近使用过的 Skill 自动排在前面，减少翻找成本
- **安装方式**：通过 Claude Code 本身完成 clone + 编译 + 文件复制，整个安装流程由 AI 驱动，无需手动执行命令
- **编译技术栈**：Swift + `swift build -c release`，产出 release 级可执行文件，性能有保障
- **调试内置**：专门内置 `/log-viewer` Skill，遇到 bug 直接在工具内查日志，不用跳出去排查
- **扩展方式**：想加新 Skill 直接写文件放进 `~/.claude/skills/`；想改功能直接跟 Claude 说；有 bug 让 Claude 查——整个生命周期都由 Claude 驱动
- **参照物定位**：SkillLauncher = Raycast（快速启动器体验）+ Claude Code Skills（AI 执行能力），面向每天调用 Skills 超过 5 次的重度用户

---

### 🛠️ 操作流程

**1. 准备阶段**

- 在桌面（或任意位置）新建一个文件夹
- 在该文件夹内打开 Claude Code

**2. 核心执行（把以下内容完整复制给 Claude）**

```
帮我安装 SkillLauncher。

地址：https://github.com/Ceeon/SkillLauncher

要求：
1. clone 到当前目录
2. 用 swift build -c release 编译
3. 把 SkillLauncher/skills 里的内容复制到 ~/.claude/skills/
```

Claude 会自动完成 clone → 编译 → 文件复制全流程。

**3. 首次启动**

- 退出 Claude Code，重新打开
- 输入 `/skill-launcher`，工具启动
- 首次运行会弹出「辅助功能」权限请求 → 点允许
- 之后 `Option+Space` 即可随时唤起

**4. 日常使用**

1. `Option+Space` 唤起窗口
2. 输入 Skill 名称（支持模糊搜索）+ 任务指令
3. 回车执行
4. 实时查看输出

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 全局快捷键 | `Option+Space` | 任意应用内唤起窗口 | 首次需授予「辅助功能」权限 |
| Skill 目录 | `~/.claude/skills/` | 自动扫描所有 Skill | 新增 Skill 直接放入此目录即生效 |
| 编译命令 | `swift build -c release` | 生成 release 可执行文件 | 需要本机有 Swift 环境 |
| 项目地址 | `https://github.com/Ceeon/SkillLauncher` | clone 源码 | 全开源，可自由修改 |
| 调试工具 | `/log-viewer` | 查看运行日志 | 遇到 bug 优先用此 Skill 排查 |
| 搜索排序 | 模糊匹配 + 最近使用优先 | 快速定位常用 Skill | 无需手动配置权重 |

---

### 📝 避坑指南

- ⚠️ 首次运行 `/skill-launcher` 后必须点允许「辅助功能」权限，否则全局快捷键无法生效
- ⚠️ 安装前确认本机已有 Swift 环境（macOS 自带，但需确认 Xcode Command Line Tools 已安装）
- ⚠️ 遇到任何问题，优先用 `/log-viewer` 查日志，而不是手动翻终端输出
- ⚠️ 这不是传统 App，没有 `.app` 包，是可执行文件，不要去 Applications 文件夹找它

---

### 🏷️ 行业标签

#ClaudeCode #Skills #效率工具 #Swift #macOS #开发者工具 #AI驱动软件

---

---
