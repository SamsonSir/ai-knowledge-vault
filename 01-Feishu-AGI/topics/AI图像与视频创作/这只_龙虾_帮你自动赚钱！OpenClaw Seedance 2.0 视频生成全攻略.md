# AI图像与视频创作

## 47. [2026-03-02]

## 📔 文章 5


> 文档 ID: `WrDmwTPIXiO36mkVAIqcSEDHnVd`

**来源**: 这只"龙虾"帮你自动赚钱！OpenClaw Seedance 2.0 视频生成全攻略 | **时间**: 2026-03-13 | **原文链接**: `https://x.com/LufzzLiz/status/2028460767444689392`

---

### 📋 核心分析

**战略价值**: 用 OpenClaw（龙虾 AI Agent）+ 岚叔封装的代码库，实现 Seedance 2.0 的文生视频、图生视频、参考视频生视频全流程自动化，并自动将视频推送到聊天窗口，几乎零手动干预。

**核心逻辑**:

- **工具链组合**: OpenClaw（或 Claude Code）作为 Agent 执行层，岚叔的 `lanshu-waytovideo` 作为封装好的工具库，Seedance 2.0（小云雀平台）作为视频生成后端，三者串联。
- **适用环境**: VPS 或个人电脑均可运行，Agent 兼容 OpenClaw、Claude Code。
- **安装方式有两种**: 手动 clone 仓库 `https://github.com/cclank/lanshu-waytovideo`，或直接在 Agent 对话中说「clone 这个项目：`https://github.com/cclank/lanshu-waytovideo/tree/main` 安装至 openclaw 里」，Agent 会自动完成安装并继承已有规约。
- **Cookie 是唯一需要手动操作的步骤**: 小云雀平台的登录态需要手动从浏览器复制 Cookie 给 Agent，验证码方式不可靠（实测失败），直接复制浏览器 Cookie 才能成功。具体复制方法参考仓库 README。
- **超时问题必须提前处理**: 默认配置会导致任务超时失败，需在配置文件中增加 `"timeoutSeconds": 3600`，修改前让 Agent 先备份原配置，修改后重启服务。
- **Agent 具备自动重试能力**: 实测中小云雀平台抽风导致第二次生成失败，Agent 自动重试，用户只对话了两次就最终成功，体现了代码健壮性。
- **三种生成模式全部跑通**: 文生视频（直接描述 prompt）、图生视频（图片由 Agent 调用 Gemini 生成后再送入 Seedance）、参考视频生视频（Agent 先抓取爆款视频，用户选定后下载预览，再生成）。
- **视频超长可用 ffmpeg 截取**: 若参考视频超过 15 秒，直接告诉 Agent 用 ffmpeg 截取目标片段，一句话完成，无需手动操作。
- **Gemini 模型配置**: 默认主模型为 `google/gemini-flash-latest`，fallbacks 为空，可按需调整。
- **最终产出可直接分发**: 生成的视频自动推送到聊天窗口，可直接投放 YouTube、抖音、视频号、支付宝视频等平台。

---

### 🛠️ 操作流程

**1. 准备阶段**

- 安装代码库（二选一）:
  - 手动: `git clone https://github.com/cclank/lanshu-waytovideo`
  - 或在 OpenClaw 新 topic 中直接说: `clone 这个项目：https://github.com/cclank/lanshu-waytovideo/tree/main 安装至 openclaw 里`
- 配置 Cookie: 打开浏览器登录小云雀，复制 Cookie，粘贴给 Agent，参考仓库 README 说明操作。

**2. 超时配置（必做）**

告诉 Agent 参考以下片段，备份后修改配置文件，增加 `timeoutSeconds`:

```json
"defaults": {
  "model": {
    "primary": "google/gemini-flash-latest",
    "fallbacks": []
  },
  "timeoutSeconds": 3600,
  "models": { ... }
}
```

修改完成后重启服务。

**3. 核心执行**

| 模式 | 操作指令示例 | 备注 |
|------|------------|------|
| 文生视频 | 直接描述视频内容，告诉 Agent 生成 | 最简单，一句话触发 |
| 图生视频 | 告诉 Agent 生成图片并转视频 | 图片由 Agent 调用 Gemini 自动生成 |
| 参考视频生视频 | 让 Agent 找爆款视频 → 选定 → 下载预览 → 生成 | 超 15s 可加一句「用 ffmpeg 截取」 |

**4. 验证与优化**

- 登录小云雀后台确认生成记录（可看到重试次数，正常情况 Agent 会自动处理）。
- 若仍超时，检查 `timeoutSeconds` 是否生效，重启后再让 Agent 重试。
- 生成成功后视频自动推送到对话窗口，直接下载分发。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 超时配置 | `"timeoutSeconds": 3600` | 防止长任务中断 | 修改前必须备份，修改后重启 |
| 主模型 | `"primary": "google/gemini-flash-latest"` | 图片生成 + 任务调度 | fallbacks 默认为空，可自行补充 |
| Cookie 配置 | 从浏览器手动复制 | 登录小云雀平台 | 验证码方式不可靠，直接用 Cookie |
| ffmpeg 截取 | 告诉 Agent「用 ffmpeg 截取前 15s」 | 处理超长参考视频 | 超 15s 的参考视频 Seedance 可能不接受 |

---

### 📝 避坑指南

- ⚠️ **Cookie 不要用验证码方式**: 实测 Agent 索要电话号码和验证码的方式失败，直接复制浏览器 Cookie 才是正路。
- ⚠️ **超时必须提前配置**: 不加 `timeoutSeconds: 3600` 大概率第一次就超时失败，虽然 Agent 会重试，但浪费 Seedance 额度。
- ⚠️ **小云雀平台本身不稳定**: 实测出现过「迷路」（平台 bug 导致生成失败），Agent 会自动重试，不用慌，等就行。
- ⚠️ **参考视频生视频有坑**: 图生视频（Gemini 生图 → Seedance）已跑通，但纯参考视频生视频流程在小云雀平台侧存在问题，需关注后续更新。

---

### 🏷️ 行业标签

#OpenClaw #SeedanceAI #视频自动化 #AIAgent #ClaudeCode #Gemini #视频生成 #小云雀

---

---
