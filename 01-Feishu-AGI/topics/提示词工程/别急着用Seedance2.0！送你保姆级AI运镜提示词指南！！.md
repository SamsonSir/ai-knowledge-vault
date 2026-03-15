# 提示词工程

## 11. [2026-02-09]

## 📗 文章 2


> 文档 ID: `RqoVwCazZivI9dk64U9cWdS5nqc`

**来源**: 别急着用Seedance2.0！送你保姆级AI运镜提示词指南！！ | **时间**: 2026-03-13 | **原文链接**: https://x.com/yyyole/status/2020729591141474743

---

### 📋 核心分析

**战略价值**: 掌握AI视频运镜提示词的三级体系，是让Seedance 2.0等工具生成"电影感"而非"随手拍"的核心差异点。

**核心逻辑**:
- 运镜提示词是AI视频质量的决定性变量：同一场景，`A girl walking in the forest` vs `A girl walking in the forest, Smooth Dolly Follow, golden hour lighting`，后者直接产生电影感，前者是监控录像感。
- Seedance 2.0的核心优势不是画质，而是它具备"导演思维"——能理解并执行复杂运镜指令。
- 80%的基础需求只需三个词覆盖：**Pan（摇移）、Zoom（变焦）、Dolly（推轨）**，新手从这三个开始练。
- 运镜分三层：基础动作词（是什么）→ 情绪修饰词（怎么动）→ 组合叠加（炫技）。
- 速度描述必须精确：不要用模糊的 `move`，要用 `Smooth 3-second dolly forward` 或 `Rapid 1-second whip pan`，AI才能准确执行。
- 情绪词直接决定视频氛围：`Aggressive` 对应恐怖/动作，`Dreamy` 对应童话/回忆，`Intimate` 对应情感近景，`Cinematic` 是万能增强词。
- 组合运镜不超过2-3个动作，用 `+` 或 `while` 连接，超过3个会产生指令冲突。
- 不同AI工具对运镜词的响应不同：Runway Gen-3偏好电影术语（dolly/crane），Pika Labs支持自然语言，Kling AI和Seedance 2.0中英文混合效果更好。
- 终极提示词结构固定为五段式：主体描述 → 运镜类型+速度/情绪修饰 → 光线描述 → 风格关键词 → 技术参数。
- 好运镜的本质是为故事和情绪服务，不是炫技——从模仿经典电影镜头开始，逐步形成自己的视觉风格。

---

### 🎯 关键洞察

**为什么运镜词比画面描述更重要**：AI视频生成中，画面内容决定"拍什么"，运镜决定"怎么拍"。专业导演80%的工作是在决定镜头语言，而非场景内容。Seedance 2.0的突破在于它能理解这套导演语言，所以不会用运镜词的人，等于把一台IMAX摄影机当手机用。

**三级体系的学习路径逻辑**：
- 基础层解决"能动"的问题
- 进阶层解决"动得有感觉"的问题
- 炫技层解决"动得有冲击力"的问题

跳过基础层直接用组合运镜，AI会因指令模糊而输出混乱结果。

---

### 📦 基础运镜词汇总表

| 类别 | 英文词 | 中文 | 适用场景 |
|------|--------|------|---------|
| 基础动作 | Pan | 水平摇移 | 跟随横向移动主体 |
| 基础动作 | Tilt | 垂直摇移 | 从脚到头/从地到天 |
| 基础动作 | Zoom | 变焦 | 拉近/推远，不移动机位 |
| 基础动作 | Dolly | 推轨 | 物理移动机位推进/后退 |
| 基础动作 | Truck | 平移 | 机位横向平行移动 |
| 基础动作 | Pedestal | 升降 | 机位垂直上下移动 |
| 基础动作 | Crane | 摇臂 | 大幅度升降+弧线运动 |
| 基础动作 | Orbit / Arc Shot | 环绕/弧形 | 围绕主体旋转 |
| 基础动作 | Tracking | 跟踪 | 跟随主体运动 |
| 基础动作 | Static | 固定 | 无运动，强调稳定感 |
| 基础动作 | Push In / Pull Out | 推进/拉出 | 强调/揭示主体 |
| 速度修饰 | Slow | 缓慢 | 悬念、回忆感 |
| 速度修饰 | Fast / Rapid | 快速 | 紧张、激烈 |
| 速度修饰 | Smooth | 流畅 | 浪漫、平和 |
| 速度修饰 | Subtle | 微妙 | 极细微动作，增强沉浸感 |
| 速度修饰 | Gradual | 渐进 | 缓慢变化，自然过渡 |
| 速度修饰 | Sudden | 突然 | 冲击感、转折点 |
| 风格修饰 | Handheld | 手持 | 纪实感、混乱感 |
| 风格修饰 | Aerial | 航拍 | 俯瞰视角 |
| 风格修饰 | POV | 第一人称视角 | 主观沉浸感 |
| 风格修饰 | Dutch Angle | 荷兰角/倾斜 | 不安感、心理扭曲 |
| 风格修饰 | Gimbal | 云台稳定 | 流畅跟随，无抖动 |
| 风格修饰 | Steadicam | 斯坦尼康 | 跟随运动，微微浮动感 |
| 情绪修饰 | Cinematic | 电影感 | 万能增强词 |
| 情绪修饰 | Aggressive | 侵略性 | 恐怖、动作场景 |
| 情绪修饰 | Dreamy | 梦幻 | 童话、回忆场景 |
| 情绪修饰 | Intimate | 亲密 | 近距离情感表达 |
| 情绪修饰 | Epic | 史诗 | 大场面、震撼感 |
| 情绪修饰 | Dynamic | 动态 | 活力、运动感 |
| 特殊效果 | Hyperlapse | 延时摄影 | 时空压缩，城市/自然变化 |
| 特殊效果 | Dolly Zoom | 推轨变焦（希区柯克效果） | 眩晕感、心理冲击 |
| 特殊效果 | Whip Pan | 甩镜 | 快速场景切换 |
| 特殊效果 | Rack Focus | 焦点切换 | 引导观众注意力转移 |

---

### 🛠️ 操作流程

**1. 准备阶段：确定场景情绪基调**
- 问自己：这个镜头要传递什么情绪？（平静/紧张/震撼/亲密）
- 根据情绪选对应的情绪修饰词（见上表）

**2. 核心执行：套用五段式模板**

```
[主体描述 Subject Description],
[运镜类型 Camera Movement] + [速度/情绪修饰词 Speed/Emotion Modifier],
[光线描述 Lighting Description],
[风格关键词 Style Keywords],
[技术参数 Technical Parameters]
```

示例（赛博朋克场景）：
```
A cyberpunk street vendor selling noodles in the rain,
Slow Dolly Circle + Subtle Zoom In,
Neon purple and blue lighting, wet reflections,
Cinematic Blade Runner aesthetic,
8K, photorealistic, shallow depth of field
```

**3. 验证与优化：四级质量自检**

| 级别 | 示例 | 问题 |
|------|------|------|
| ❌ 基础版 | `A deer in the forest` | 无运镜，随手拍感 |
| ⚠️ 初级优化 | `A deer in the forest, camera moving forward` | 词汇模糊，AI理解偏差 |
| ✅ 进阶优化 | `A majestic deer in misty forest, Smooth Dolly Follow at eye level, soft morning light filtering through trees, cinematic depth of field` | 有运镜+光线+风格 |
| 🌟 大师级 | `A majestic deer slowly turning its head in ancient misty forest, Subtle Arc Shot 90 degrees + Gradual Zoom In on eyes, ethereal god rays, photorealistic 8K, dreamy atmosphere` | 完整五段式+组合运镜 |

---

### 💡 具体案例/数据

**经典组合运镜场景模板**：

场景1 — 揭示震撼场景：
```
Starting from a close-up of a mysterious object,
Slow Dolly Back + Crane Up,
gradually revealing it's part of a massive ancient temple,
epic scale, golden hour lighting
```

场景2 — 情绪转折：
```
Character standing at the cliff edge,
Smooth Arc Shot 180 degrees + Subtle Zoom In on face,
expression changing from despair to determination,
dramatic backlight
```

场景3 — 时空转换：
```
Modern city street scene,
Hyperlapse Dolly Forward through decades,
buildings morphing from old to futuristic,
seamless time transition
```

**经典复合组合速查**：

| 组合 | 效果 | 适用场景 |
|------|------|---------|
| Orbit + Zoom In | 视觉冲击力极强 | 揭示主体 |
| Crane Up + Pan | 大气磅礴 | 开场或结尾 |
| Dolly Zoom（Vertigo Effect） | 眩晕感、心理冲击 | 角色意识到真相的瞬间 |
| Hyperlapse + Orbit | 时空压缩感 | 城市/自然24小时变化 |
| Tracking + Handheld Shake | 紧张追逐感 | 逃亡/追逐场景 |

---

### 📝 避坑指南

- ⚠️ 禁用模糊词 `move`：改用 `Smooth 3-second dolly forward`，AI需要精确指令才能输出稳定结果。
- ⚠️ 速度必须量化：`3-second slow zoom`、`Rapid 1-second whip pan`、`Gradual 10-second crane up`，有时间数字比纯形容词效果好得多。
- ⚠️ 组合运镜不超过3个动作：`Pan left + zoom in + track right + orbit + crane up` 这种写法会让AI指令冲突，输出混乱。正确写法：`Dolly forward + subtle tilt up`。
- ⚠️ 不同工具用不同语言策略：Runway Gen-3用电影术语（dolly/crane），Pika Labs用自然语言（camera moves closer slowly），Kling AI和Seedance 2.0用中英文混合效果更好。
- ⚠️ 不要跳过基础层直接炫技：组合运镜建立在对单个运镜词的精准理解上，基础不稳会导致组合效果不可控。

---

### 🏷️ 行业标签

#Seedance2.0 #AI视频生成 #运镜提示词 #Prompt工程 #视频创作 #电影感 #导演语言 #RunwayGen3 #PikaLabs #KlingAI

---

---
