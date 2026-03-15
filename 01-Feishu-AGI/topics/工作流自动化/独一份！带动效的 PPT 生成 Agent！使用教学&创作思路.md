# 工作流自动化

## 4. [2026-01-13]

## 📔 文章 5


> 文档 ID: `Xgp8wQ0QciPoQBkxNWycUq4Vnle`

**来源**: 独一份！带动效的 PPT 生成 Agent！使用教学&创作思路 | **时间**: 2026-01-13 | **原文链接**: `https://mp.weixin.qq.com/s/YY0Fqd2p...`

---

### 📋 核心分析

**战略价值**: 基于 Claude Code + Nano Banana Pro + 可灵 API，构建一个能生成带转场动画视频的 PPT 的本地 Agent Skills，输出物包含静态图片、演示网页、完整合成视频三件套。

**核心逻辑**:

- **能力边界**：现有市面 Agent 产品均不支持 PPT 动效生成，该 Skills 填补空白，输出带转场视频的演示级 PPT
- **输出三件套**：① 每页 PPT 静态图片 ② 可用键盘控制的演示网页（空格播放、左右键翻页）③ ffmpeg 合成的完整演示视频
- **转场设计逻辑**：切换页面时播放转场视频，切换完毕后替换为静态图片（方便讲解），封面页设计为无限循环动态视频（适合等场/暖场）
- **图片生成**：调用 Gemini 的 Nano Banana Pro 模型（需开启付费），通过 Google AI Studio 获取 API Key
- **视频生成**：调用可灵 Kling-2.6 Pro 模式生成转场视频，并发限制为 3，代码内已做并发控制处理
- **元提示词机制**：转场首尾帧提示词不是硬编码，而是设计了一个「元提示词」，Claude Code 根据该元提示词 + 已生成图片动态生成每个转场的具体提示词
- **FFmpeg 合成复杂度**：涉及图片停留时间控制、图片与视频分辨率对齐、片段拼接、最终压缩，是整个流程中工程量最重的环节
- **Skills 构建方法论**：准备好上下文文件（提示词模板、API 文档、API Key）→ 在目标文件夹打开 Claude Code → 让其生成计划 → 审批执行，全程用 Sonnet 4.5 完成，未调用 Opus
- **安装方式**：将安装提示词直接发给 Claude Code 或 OpenCode，让 CLI 自动执行安装，建议开启 Plan 模式（Shift+Tab 两次）降低出错概率
- **使用方式**：将目标文档放入文件夹 → 在该文件夹启动 Claude Code → 说「调用 Skills 将当前文件夹下的 XXX 文档生成 PPT」→ 按方向键选择参数（页数、是否带动效、分辨率）→ 全程回车等待，无需再次交互

---

### 🎯 关键洞察

**元提示词的价值**：不直接写死转场提示词，而是写一个「生成提示词的提示词」，让模型根据已生成的图片内容动态推导出最合适的首尾帧描述。这种模式可复用到任何需要「上下文感知型提示词生成」的场景，是 Agent 设计中的高价值模式。

**架构复杂度跃迁点**：纯图片生成阶段架构简单；一旦引入视频 + 网页演示 + 完整视频输出，架构复杂度非线性上升，需要协调图片模块、视频模块、网页渲染模块、ffmpeg 合成模块四个子系统。

---

### 📦 配置/工具详表

| 模块 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|------|-------------|---------|-----------|
| Gemini API | `GEMINI_API_KEY=YOUR_KEY` | 调用 Nano Banana Pro 生成 PPT 图片 | 必须开启付费，免费 Key 无法调用该模型 |
| 可灵 API | `KLING_ACCESS_KEY` + `KLING_SECRET_KEY` | 生成转场动画视频 | 创建时产生两个 Key，两个都需要填入；并发上限 3，代码已处理 |
| 视频模型 | Kling-2.6 Pro 模式 | 高质量转场视频 | — |
| ffmpeg | 本地调用 | 合成完整演示视频 | 需处理图片时长控制、分辨率对齐、拼接压缩 |
| 演示网页 | 空格=播放转场视频，左右键=翻页 | 浏览器内直接演示 | 封面页为无限循环视频 |
| Plan 模式 | Shift+Tab × 2 | 降低安装出错概率 | 出问题直接让 Claude Code 自修复 |

---

### 🛠️ 操作流程

**1. 准备阶段**

获取两个 API：
- Google AI Studio 获取 Gemini API Key（需开启付费）：`https://aistudio.google.com/api-keys`
- 可灵充值入口：`https://klingai.com/cn/dev/pricing?scrollTo=video`（建议先用体验包）
- 可灵 API Key 获取：`https://app.klingai.com/cn/dev/api-key`（会生成两个 Key，均需保存）

**2. 安装 Skills**

将以下提示词发给 Claude Code 或 OpenCode（替换三处 API Key 为真实值后发送）：

```
请帮我将 NanoBanana PPT Skills 安装为 Claude Code Skill：

1. 创建 Skill 目录：
   mkdir -p ~/.claude/skills/ppt-generator

2. 克隆项目到 Skill 目录：
   git clone https://github.com/op7418/NanoBanana-PPT-Skills.git ~/.claude/skills/ppt-generator

3. 进入目录并安装依赖：
   cd ~/.claude/skills/ppt-generator
   python3 -m venv venv
   source venv/bin/activate
   pip install google-genai pillow python-dotenv

4. 配置 API 密钥：
   cp .env.example .env

   然后编辑 .env 文件，填入我的 API 密钥：
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY
   KLING_ACCESS_KEY=YOUR_KLING_ACCESS_KEY
   KLING_SECRET_KEY=YOUR_KLING_SECRET_KEY

5. 验证安装：
   python3 generate_ppt.py --help

完成后，告诉我如何在 Claude Code 中使用这个 Skill。

我的 API 密钥：
- GEMINI_API_KEY: YOUR_GEMINI_API_KEY_HERE
- KLING_ACCESS_KEY: YOUR_KLING_ACCESS_KEY_HERE (可选)
- KLING_SECRET_KEY: YOUR_KLING_SECRET_KEY_HERE (可选)
```

安装时按 Shift+Tab 两次开启 Plan 模式，出错让 Claude Code 自行修复。

项目地址：`https://github.com/op7418/NanoBanana-PPT-Skills`

**3. 使用阶段**

1. 将目标文档放入一个文件夹（也可以没有文档，让 Skills 调用搜索工具自动写内容）
2. 在该文件夹内启动 Claude Code
3. 输入指令：「调用 Skills 将当前文件夹下的 XXX 文档生成 PPT」
4. 用方向键选择参数：PPT 页数 / 是否生成动效视频 / 图片分辨率
5. 之后全程回车等待，无需再次交互
6. 生成完毕后自动保存所有图片，并打开演示网页

**4. 演示阶段**

- 浏览器打开演示网页
- 空格键：播放当前转场视频
- 左/右方向键：切换上一页/下一页
- 封面页：无限循环动态视频，适合暖场等待

---

### 💡 完整 Agent 架构流程

```
用户文档输入
    ↓
文档分析 & 内容规划
    ↓
PPT 生成模块 + 风格加载器
    ↓
图片生成提示词生成（基于风格加载器）
    ↓
调用 Nano Banana Pro API 生成图片（含生成过程监控）
    ↓
[图片生成完成]
    ↓
元提示词 + 生成图片 → 生成每个转场的首尾帧提示词
    ↓
调用可灵 API（Kling-2.6 Pro）生成转场视频（并发=3）
    ↓
将图片路径 + 视频路径注入演示网页代码 → 生成演示网页
    ↓
调用本地 ffmpeg 合成完整演示视频
（处理：图片时长控制 → 分辨率对齐 → 片段拼接 → 压缩）
    ↓
输出：演示网页 + 完整视频
```

---

### 📝 避坑指南

- ⚠️ Gemini 免费 Key 无法调用 Nano Banana Pro，必须开启付费才能使用
- ⚠️ 可灵 API 创建时生成两个 Key（Access Key + Secret Key），两个都要填，缺一不可
- ⚠️ 可灵并发上限为 3，代码已内置处理，不要手动修改并发逻辑
- ⚠️ 安装前务必将提示词中三处 `YOUR_XXX_KEY_HERE` 替换为真实 Key，否则安装后无法运行
- ⚠️ 安装过程建议开启 Plan 模式（Shift+Tab × 2），出错直接让 Claude Code 自修复，不要手动干预
- ⚠️ ffmpeg 需本地已安装，合成视频时会调用本地 ffmpeg 命令

---

### 🏷️ 行业标签

#ClaudeCode #PPT生成 #Agent构建 #NanoBananaPro #可灵API #元提示词 #AISlides #SkillsInstall #ffmpeg #Kling2.6

---

---
