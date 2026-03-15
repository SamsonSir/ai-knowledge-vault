# Agent与技能系统

## 17. [2026-01-21]

## 📘 文章 3


> 文档 ID: `Rx5GwOLjQi8LS1kUzFhc1PGpnDd`

**来源**: 卡兹克：Skills的最正确用法，是将整个Github压缩成你自己的超级技能库 | **时间**: 2026-01-21 | **原文链接**: `https://mp.weixin.qq.com/s/JER462B3...`

---

### 📋 核心分析

**战略价值**: 用 AI 搜索 GitHub 开源项目 → 用 skill-creator 一键 Skill 化 → 注入 Agent，让任何人都能把人类30年开源积累变成自己的私人武器库。

**核心逻辑**:

- **重复造轮子是反效率的**：GitHub 上几乎所有常见需求都有经过时间鞭打的成熟开源项目，稳定性和成功率远超临时让 AI 写的代码。
- **Skills 的结构优势**：Skills 可以把脚本 + Prompt 打包在一起，这是单 Prompt 或单脚本做不到的，天然适合封装开源项目。
- **支持平台**：Coze（扣子）、OpenCode、Claude Code，只要装了 `skill-creator` 这个官方 Skill，均可执行 GitHub 项目 Skill 化。
- **AI 搜索替代 GitHub 检索门槛**：不懂 GitHub 的普通人，直接用 ChatGPT（推荐 GPT-5.2 Thinking，搜索能力强、幻觉低）提问「有没有做 XX 功能的 GitHub 开源项目」，AI 会直接推荐最优解。
- **构建 Skill 时推荐 Claude 4.5 Opus**，首次运行调试时推荐 **GPT 5.2 Codex**（运行体验比 Claude 4.5 Opus 好 N 倍），后续运行模型无所谓。
- **先 Plan 后 Dev 的两阶段策略**：先让 Agent 进入 Plan 模式规划封装方案，确认无误后再切换开发模式，成功率更高、后期稳定性更强。
- **首次运行必然有 BUG，要迭代固化**：第一次运行会遇到环境问题（如 YouTube 防爬需要浏览器扩展导出 Cookie），AI 会全程指导解决，解决后把经验更新回 Skill 文件，后续运行从几分钟压缩到十几秒。
- **Skill 自我管理**：卡兹克自建了一个「管理 Skills 的 Skill」，可直接对本地所有 Skill 执行卸载、删除、修改、优化操作，避免每次进文件夹手动管理。
- **Skill 化的本质是能力固化**：每个 Skill 经过「首次运行 → 发现问题 → 迭代更新」后固化，成为 Agent 中一个可靠的、可复用的技能节点。

---

### 🎯 关键洞察

**为什么历史悠久的开源项目比 AI 临时写的代码更可靠？**
原因：经过无数用户和时间的鞭打，边界情况已被处理，文档完善，社区活跃。
动作：优先搜索 GitHub 成熟项目而非让 AI 从零生成。
结果：Skill 的成功率、稳定性、效率全面碾压临时代码。

**为什么普通人之前用不了 GitHub 开源项目？**
两道门槛：① 不知道有哪些项目；② 部署需要命令行，环境配置卡死大多数人。
Skills 同时解决了这两个问题：AI 负责搜索推荐，skill-creator 负责封装部署，用户只需提需求。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| skill-creator | Claude 官方提供的 Skill 生成器，需提前安装到 OpenCode 或 Claude Code | 自动分析 GitHub 项目并打包成 Skill | 不装这个 Skill 无法执行后续所有操作 |
| 构建 Skill 的模型 | Claude 4.5 Opus | 代码生成质量高，封装成功率高 | 首次运行调试不推荐用它 |
| 首次运行调试模型 | GPT 5.2 Codex（需有权限） | 运行体验比 Claude 4.5 Opus 好 N 倍 | 后续运行模型随意 |
| AI 搜索工具 | ChatGPT，选 GPT-5.2 Thinking | 搜索能力强、幻觉低，能精准推荐 GitHub 项目 | 其他模型也可用，效果略差 |
| OpenCode Plan 模式 | 开启 Plan 模式后发送封装需求 | Agent 先规划再开发，成功率更高 | 确认规划无误后再切换开发模式 |
| yt-dlp Skill | 封装命令：`帮我把这个开源工具 https://github.com/yt-dlp/yt-dlp 打包成一个Skill，只要我后续给出视频链接，就可以帮我下载视频。` | 支持 YouTube、B站等上千个网站下载视频 | YouTube 防爬需装浏览器扩展导出 Cookie |
| 经验回写命令 | `把这些经验，都更新到video-downloader这个skill里，下次就别这么慢了。` | Skill 自动迭代，后续运行从几分钟→十几秒 | 每次首次运行后都应执行此步骤 |
| Skills 管理 Skill | 自建，可对本地所有 Skill 执行卸载/删除/修改/优化 | 无需进文件夹手动管理 | 需自行构建 |

---

### 🛠️ 操作流程

**以「封装 yt-dlp 视频下载 Skill」为完整示例：**

1. **需求 → 搜索**
   打开 ChatGPT，选 GPT-5.2 Thinking，输入：
   > 有没有那种就是去各种视频网站上，下载视频，比如Youtube、B站等等的github上的开源项目。

   → AI 推荐 **yt-dlp**（GitHub 143k stars，支持上千个网站）

2. **复制 GitHub 链接**
   `https://github.com/yt-dlp/yt-dlp`

3. **进入 OpenCode，开启 Plan 模式，发送封装 Prompt**
   > 帮我把这个开源工具 `https://github.com/yt-dlp/yt-dlp` 打包成一个Skill，只要我后续给出视频链接，就可以帮我下载视频。

4. **Agent 规划阶段**
   Agent 调用 skill-creator 分析项目，向你提问（如：需要哪些格式？是否需要字幕？），回答后 Agent 给出完整计划。

5. **确认计划 → 切换开发模式**
   确认规划无误，发送：`开始开发！`
   → 约 2 分钟完成 Skill 构建。

6. **首次运行（用 GPT 5.2 Codex）**
   把视频链接扔给 OpenCode，遇到问题（如 YouTube Cookie 问题）按 AI 指导操作，全程约几分钟。

7. **经验回写，固化 Skill**
   运行成功后发送：
   > 把这些经验，都更新到 video-downloader 这个 skill 里，下次就别这么慢了。

   → Skill 自动更新，后续下载只需十几秒。

---

### 💡 具体案例/数据

| 开源项目 | GitHub Stars | 功能 | Skill 化后的用途 |
|---|---|---|---|
| yt-dlp | 143k | 视频下载，支持上千个网站 | 一句话下载 YouTube、B站等任意视频 |
| Pake | 45k | 将 Web 项目打包成轻量级桌面 APP | 网页开发完直接一句话变桌面 APP |
| FFmpeg | - | 视频处理 | 多模态素材处理 Skill（与 ImageMagick 合并封装） |
| ImageMagick | - | 图片/视频处理 | 同上，与 FFmpeg 合并为万能素材处理 Skill |
| ArchiveBox | - | 网页存档，支持 N 种格式 | 发送网页链接即可多格式本地存档 |
| Ciphey | - | 自动密码破译 | 配合本地 Agent 直接破译密码 |
| 万能格式转化 | - | 多个格式转化项目合并封装 | 替代所有格式转化 APP，一个 Skill 解决所有格式问题 |

---

### 📝 避坑指南

- ⚠️ **必须先装 skill-creator**：没有这个 Skill，OpenCode/Claude Code 无法执行任何 GitHub 项目的 Skill 化操作。
- ⚠️ **YouTube 防爬机制**：首次运行 yt-dlp Skill 时，YouTube 的防爬机制会导致失败，需要安装浏览器扩展导出 Cookie，AI 会指导，但要预留时间。
- ⚠️ **首次运行必用 GPT 5.2 Codex**：涉及运行程序的 Skill，首次运行用 Claude 4.5 Opus 体验差，务必切换到 GPT 5.2 Codex（需有权限）。
- ⚠️ **首次运行后必须回写经验**：不执行「把经验更新到 Skill」这一步，下次运行还是会重复踩坑，速度不会提升。
- ⚠️ **先 Plan 再 Dev**：直接跳过规划阶段让 Agent 开发，成功率和稳定性都会下降，务必先走 Plan 模式。

---

### 🏷️ 行业标签

#Skills #Agent #GitHub开源 #yt-dlp #OpenCode #ClaudeCode #skill-creator #工作流自动化 #Pake #ArchiveBox

---

---
