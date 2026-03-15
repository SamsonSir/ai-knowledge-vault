# AI图像与视频创作

## 17. [2026-02-01]

## 📒 文章 7


> 文档 ID: `JCd2wCX1dizS82kmIO1cy7uXncg`

**来源**: 小松鼠：结合RemotionSKill，手搓AI视频自动化生成流水线 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 用 6 个可复用 Skill 模块 + 1 个主流程，将「文章 → MP4」的全链路视频生成压缩到 10 分钟内自动完成，且每个模块可独立迭代。

**核心逻辑**:

- **字幕不是后期工序，是前期数据结构**：Remotion 本身需要手写 `<Sequence from={} durationInFrames={}>` 控制每帧，字幕本质上就是时间轴拆分后的文字，直接在 React 层用 `<SubtitleTrack>` 组件渲染，省掉后期字幕轨道。
- **文本动画来源于现成 React 库**：参考 `https://www.reactbits.dev/text-animations/split-text`，让 AI 学习该库后抽象出 8 种动画（逐字淡入、波浪、打字机、3D旋转、颜色渐变、缩放弹出、滑动进入、模糊聚焦），覆盖标题/重点/代码/转场等场景。
- **TTS 选型原则是「跑通优先」**：不调用外部 API Key，直接用本地 `edge-tts`（`pip install edge-tts`），完全免费，保护注意力，字幕文本即语音文本，批量一次生成。
- **音效库是人工筛选 + AI 分类**：手动收集 42 个音效，让 AI 分析使用场景并写成说明文档供 Skill 调用；音量配比：配音 1.0、音效 0.15-0.5、BGM 0.25。
- **角色动画用 tween 动画复用品牌形象**：单独 React 文件调试角色动作，抽象成公用组件 `<SquirrelCharacter>`，支持 pose/position/enterAnimation/loopAnimation/scale 参数。
- **主技能是 6 个子技能的调度器**：用户只需提供一个 `.md` 文章文件，主技能按顺序调用子技能，最终输出六轨道合成视频，整个过程 10 分钟内完成，最后多轨道渲染仅需 53 秒。
- **六轨道独立设计保证可关闭/可迭代**：不满意某轨道（如配音难听）可直接关闭该轨道导出，再到剪映二次加工；想升级某能力只需迭代对应 Skill，不影响其他模块。
- **开发方法论：先手动跑通 → 发现重复 → 抽象 Skill → 组合主流程**：每次迭代都在解决实际问题，不是一次性设计完整架构。
- **AI 协作模式是「你决策，AI 实现」**：提出问题（如"给标题加动画"），AI 给方案，你做取舍；不是让 AI 替你写代码，而是共同思考迭代。
- **适用场景明确**：教育科普、知识讲解、技术分享类视频，不适合需要真人出镜或高度创意剪辑的内容。

---

### 🎯 关键洞察

**为什么字幕要在 React 层做而不是后期**：
Remotion 的时间轴本身就是按帧拆分的文字段落，这份数据天然就是字幕数据。如果后期再加字幕，等于把同一份数据处理两遍。直接在生成视频脚本时同步生成字幕文件，用 React 组件渲染到底部，一次搞定，且字幕和画面帧完全同步，不存在对齐问题。

**为什么 TTS 选 edge-tts 而不是商业 API**：
第一版的目标是跑通流程，不是做出最好的语音。edge-tts 零成本、零配置、本地运行，能让整个流水线闭环。等流程稳定后再替换 TTS 模块为更好的模型，成本极低（只改一个 Skill）。

**六轨道架构的核心价值**：
每个轨道独立意味着每个维度可以单独关闭、单独迭代、单独替换。这不是技术复杂度的体现，而是「可维护性」的体现——任何一个环节出问题，不会拖垮整个流水线。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| subtitle-generator | `<SubtitleTrack subtitles={subtitles} fontSize={45} color="#fff" fadeDuration={10} />` | 自动时间轴字幕渲染 | 字幕文本即 TTS 文本，两者共用同一份数据 |
| remotion-text-animations | `renderSplitTextWithFadeIn("文字", frame, 0, 80, "#fff")` | 8 种文本动画 | 参考 `https://www.reactbits.dev/text-animations/split-text` |
| tts-voice-generator | `pip install edge-tts` → `python generate_voice.py batch script.txt ../public/audio/voice/output` | 批量本地配音生成 | 完全免费，无需 API Key |
| sfx-matcher | 42 个音效，配音 1.0 / 音效 0.15-0.5 / BGM 0.25 | 转场/标题/强调/UI/科技/情绪 6 类音效 | 音效质量依赖素材，需自行替换高质量素材 |
| remotion-character-system | `<SquirrelCharacter pose="thinking" position="bottom-right" enterAnimation="bounce" loopAnimation="thinkLoop" scale={0.25} />` | 角色 tween 动画 | 先单独 React 文件调试，再抽象为公用组件 |
| video-builder（主技能） | 输入：`.md` 文章文件；输出：六轨道合成视频 | 10 分钟内全自动生成，最终渲染 53 秒 | 用户确认满意后自行运行导出命令 |

---

### 🛠️ 操作流程

1. **准备阶段**
   - 准备一篇 `.md` 格式的文章作为输入
   - 安装依赖：`pip install edge-tts`
   - 收集音效素材（42 个，分 6 类），让 AI 分析使用场景并生成说明文档供 sfx-matcher 调用
   - 准备角色形象图片用于 tween 动画

2. **核心执行**
   - 调用 `video-builder` 主技能，传入 `.md` 文件
   - 主技能自动按序执行：
     1. `remotion-text-animations` → 生成带动画的 Remotion 脚本
     2. `subtitle-generator` → 同步生成字幕文件，按段分好时间轴
     3. `tts-voice-generator` → 根据字幕段落批量生成配音音频
     4. `sfx-matcher` → 根据转场时长从音效库匹配音效 + BGM
     5. `remotion-character-system` + `remotion-character-integration` → 插入角色动画轨道
   - 六轨道合并：字幕轨 / 文本动画轨 / 配音轨 / 音效轨 / BGM 轨 / 角色动画轨

3. **验证与优化**
   - React 模式下实时预览，不满意可反复调试代码
   - 不满意某轨道可直接关闭（如关闭配音轨），导出后到剪映二次加工
   - 确认满意后，手动运行导出命令生成最终 MP4
   - 后续迭代：只需替换对应 Skill（如换更好的 TTS 模型），不影响其他模块

---

### 📦 Skill 目录结构

```
video-builder（主技能）
  ├──→ remotion-text-animations（文本动画）
  ├──→ subtitle-generator（字幕生成）
  ├──→ tts-voice-generator（配音生成）
  ├──→ sfx-matcher（音效匹配）
  ├──→ remotion-character-system（角色动画）
  └──→ remotion-character-integration（角色集成）
```

六层主轨道：字幕 / 文本动画 / 配音 / 音效 / BGM / 角色动画

---

### 💡 具体案例/数据

- 全流程从文章到 MP4：**10 分钟内**完成
- 最终多轨道渲染时间：**53 秒**
- 音效库规模：**42 个**专业音效，覆盖 6 类场景
- 文本动画种类：**8 种**（逐字淡入/波浪/打字机/3D旋转/颜色渐变/缩放弹出/滑动进入/模糊聚焦）
- 音量配比经验值：配音 **1.0**、音效 **0.15-0.5**、BGM **0.25**

---

### 📝 避坑指南

- ⚠️ **不要一开始就追求最好的 TTS**：第一版目标是跑通流程，用 edge-tts 本地方案即可，后期再换模型成本极低。
- ⚠️ **字幕数据和 TTS 文本必须共用同一份**：两份数据分开维护会导致字幕和配音不同步。
- ⚠️ **音效质量取决于素材，不取决于 Skill**：sfx-matcher 的调用逻辑正确，但素材质量需自行把控，建议后期替换高质量音效包。
- ⚠️ **角色动画先单文件调试再抽象**：直接写公用组件容易踩坑，先在独立 React 文件里跑通动画效果，再让 AI 抽象成组件。
- ⚠️ **主技能整合前先删掉所有中间文件**：避免历史文件干扰主流程的完整性验证。
- ⚠️ **导出命令由用户手动触发**：React 调试模式下不自动导出，用户确认满意后才运行导出命令，防止误操作。

---

### 🏷️ 行业标签

#Remotion #AI视频生成 #TTS #EdgeTTS #React动画 #视频自动化 #Skill系统 #AIGC #视频流水线 #多轨道合成

---

---
