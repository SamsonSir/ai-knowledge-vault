# Agent与技能系统

## 100. [2026-03-05]

## 📚 文章 8


> 文档 ID: `BcwfwMKbViTbXUkvyUMcFTbvnDc`

**来源**: OpenClaw 保姆级教程：你要知道的都在这里了！ | **时间**: 2026-03-02 | **原文链接**: `https://mp.weixin.qq.com/s/Bvw5dPeE...`

---

### 📋 核心分析

**战略价值**: OpenClaw 是真正可落地的本地 AI 个人助理，能操控浏览器、桌面、24 小时自动执行任务，本文提供从零部署到进阶使用的完整路径。

**核心逻辑**:

- OpenClaw 四大核心能力：①自动操控浏览器执行网页任务；②操控本地电脑（安装软件、开发程序、监控任务）；③24 小时不间断运行，任务完成后等待审核；④向量记忆模块，越用越懂用户习惯
- OpenClaw 本体开源免费，运行消耗本地电脑资源，一次安装永久可用，无需额外付费
- 必须对接模型 API 才能运行，模型相当于"厨师"，本体相当于"厨房"，厨房免费但厨师收费
- 国内可选模型厂商：智谱 GLM5.0（复杂任务首选）、Kimi、阿里通义（轻量尝试首选）、字节豆包、DeepSeek、Minimax
- 字节的部署文档额外包含 OpenClaw 与飞书打通的教程，即使不用字节模型也值得单独参考
- 非研发人员可用一键脚本安装，Mac/Linux 和 Windows 各有对应命令，脚本会自动安装 Node.js + NVM + OpenClaw
- 一键脚本失败时，不要尝试修复脚本，直接走手动安装三步流程（Node.js → NVM → OpenClaw）
- 安装遇到网络问题，配置国内镜像源解决；不会配置就直接问 AI（豆包/DeepSeek/千问）
- 本地已有 Agent（Trae、Qoder、Claude Code、OpenCode、Codex）的用户，可直接把安装文档链接丢给 Agent，让它全程代劳
- 8 个必装 Skill 覆盖自我进化、浏览器自动化、桌面控制、安全扫描、子任务委派、向量记忆等核心能力

---

### 🎯 关键洞察

**为什么选智谱 GLM5.0 做复杂任务**：当前国内模型中综合表现最优，适合需要多步推理、长链路执行的复杂自动化场景。

**为什么阿里适合轻量尝试**：首月价格最低，适合验证 OpenClaw 是否符合自己需求，但注意关闭自动续费，续费价格与首月不同。

**官方文档的正确用法**：官方文档更像是给模型看的，不适合人类直接阅读。正确姿势是把官网链接 `https://docs.openclaw.ai/zh-CN` 丢给 OpenClaw 本身，让它基于文档内容回答你的问题。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 一键安装（Mac/Linux） | `curl -fsSL https://clawd.org.cn/install.sh \| bash -s -- --registry https://registry.npmmirror.com` | 自动安装 Node.js + NVM + OpenClaw | 脚本失败不要修复，直接走手动流程 |
| 一键安装（Windows） | `iwr -useb https://clawd.org.cn/install.ps1 -OutFile install.ps1; ./install.ps1 -Registry https://registry.npmmirror.com` | 同上 | 同上 |
| Skill: self-improvement | 安装后自动生效 | 记录错误、自我学习改进 | 基础必装 |
| Skill: browser | 安装后自动生效 | 浏览器自动化、网页交互、截图 | 基础必装 |
| Skill: desktop-control | 安装后自动生效 | 鼠标键盘控制、桌面自动化 | 基础必装 |
| Skill: auto-updater | 安装后自动生效 | 自动更新 Clawdbot 和技能 | 基础必装 |
| Skill: skill-vetter | 安装后自动生效 | 扫描已安装技能安全性 | 防止恶意技能上传本地文件 |
| Skill: subagent-driven-development | 安装后自动生效 | AI 学会委派子任务给其他 AI 并审核 | 解放用户专注高层决策 |
| Skill: vector-memory | 安装后自动生效 | 向量记忆搜索，解决上下文过长导致记忆不准 | 任务复杂时必装 |
| Skill: clawhub | 安装后自动生效 | OpenClaw 技能市场入口，让 AI 自行检索安装 | 其他需求从这里扩展 |

---

### 🛠️ 操作流程

**1. 准备阶段：选择模型厂商并购买 API**

| 厂商 | 适用场景 | 购买链接 | 部署文档 |
|-----|---------|---------|---------|
| 智谱 GLM5.0 | 复杂任务首选 | `https://www.bigmodel.cn/glm-coding?ic=N1OXQTTAW7` | `https://docs.bigmodel.cn/cn/coding-plan/tool/openclaw` |
| Kimi | 综合使用 | `https://www.kimi.com/code` | `https://platform.moonshot.ai/docs/guide/use-kimi-in-openclaw#step1-create-kimi-platform-api-key` |
| 阿里通义 | 轻量尝试首选（首月最低） | `https://www.aliyun.com/benefit/ai/aistar?userCode=vz8mervt` | `https://bailian.console.aliyun.com/cn-beijing/?tab=doc#/doc/?type=model&url=3023085` |
| 字节豆包 | 需要飞书集成 | `https://www.volcengine.com/activity/codingplan` | `https://www.volcengine.com/docs/82379/2183190?lang=zh` |

> ⚠️ 阿里首月低价，记得关闭自动续费

**2. 核心执行：安装 OpenClaw**

- 优先尝试一键脚本（见上方配置表）
- 脚本失败 → 手动三步走：
  1. 安装 Node.js：`https://www.runoob.com/nodejs/nodejs-install-setup.html`
  2. 安装 NVM：`https://www.runoob.com/nodejs/nodejs-nvm.html`
  3. 安装 OpenClaw（Mac/Linux）：`https://www.cnblogs.com/catchadmin/p/19556552`
  4. 安装 OpenClaw（Windows）：`https://cloud.tencent.com/developer/article/2626160`
- 网络问题 → 配置国内镜像源，不会就问 AI

**3. 验证与优化：安装必备 Skill**

按顺序安装 8 个必装 Skill（见配置表），然后通过 clawhub 按需扩展其他领域技能。

---

### 💡 具体案例/数据

- clawhub 技能市场总量超过 1 万个 Skill
- Awesome-openclaw-skills 精选整理约 5000 个并分类，按领域查找效率更高：`https://github.com/VoltAgent/awesome-openclaw-skills`

---

### 📝 避坑指南

- ⚠️ 一键脚本执行异常时，不要尝试修复脚本，直接走手动安装流程，省时省力
- ⚠️ 阿里首月低价是限时优惠，续费价格不同，购买后立即关闭自动续费
- ⚠️ 安装 skill-vetter 并优先运行，防止恶意 Skill 将本地文件上传到非法云端
- ⚠️ 官方文档不适合人类直读，遇到问题把文档链接丢给 OpenClaw 让它自己查

---

### 📚 学习资源汇总

| 资源 | 链接 |
|-----|-----|
| 官方文档 | `https://docs.openclaw.ai/zh-CN` |
| 精选 Skill 库（~5000个分类） | `https://github.com/VoltAgent/awesome-openclaw-skills` |
| 学习资源聚合站 | `https://openclaw101.dev/zh` |
| 中文社区 | `https://clawd.org.cn/` |
| 中文教程 | `https://awesome.tryopenclaw.asia/` |
| 新手到中级完整教程 | `https://x.com/stark_nico99/status/2026235176150581282?s=46` |

---

### 🏷️ 行业标签
#OpenClaw #AI助理 #本地部署 #自动化 #LLM #AgentOS #国产模型 #工作流自动化

---

---
