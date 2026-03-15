# AI图像与视频创作

## 5. [2026-01-12]

## 📗 文章 2


> 文档 ID: `GNAhwoSTOispbIkh4XXcvlpXnOe`

**来源**: 超全Niji V7多场景实测，Midjourney这位前顶流又仰卧起坐了 | **时间**: 2026-01-12 | **原文链接**: `https://mp.weixin.qq.com/s/HKuR2V5d...`

---

### 📋 核心分析

**战略价值**: Niji V7 于2026年1月9日正式上线，在线条质量、提示词遵循度、材质光泽感三个维度有肉眼可见的代际提升，是动漫/插画方向 AI 绘图工具链的新首选节点。

**核心逻辑**:

- **图像质量全面升级**：连贯性大幅增强，眼睛反射细节、背景飘落花瓣等微观元素精准呈现，相当于一次"高清升级"，近景 Waifu 眼睛光晕效果显著改善。
- **提示词遵循能力增强**：模型更偏向字面理解，可准确区分"左边红色立方体/右边蓝色立方体"的空间位置，可绘制"四只手臂各拿冰淇淋"等高度具体的请求。注意：原先强调氛围感的提示词需重新调整，因为模型现在更倾向字面执行。
- **线条质量突破**：杂乱无序的"线头"大幅减少，更接近手绘/板绘质感，简单插画线条勾勒更精确。可用 `anime screenshot` 提示词专门体验线条优化效果。
- **简约风格支持**：Niji V7 有意识追求简洁，支持大面积留白，可用 `minimalist graphic logo` 提示词体验。AI 艺术中"简单画面最难"的悖论在此版本有所突破。
- **默认风格平面化**：默认降低了渲染量（减少3D感），呈现更平面化外观，以展示底层绘图的连贯性，线条与大面积平涂区域结合效果更出色。
- **sref（风格参考）表现出色**：Niji V7 与 Midjourney 的 sref code 可以共用，且在 Niji V7 上体验感优于 Midjourney 本体，加持下提示词随便写也能出好图。
- **cref（角色参考）暂不支持**：官方表示正在开发"超级神秘惊喜"替代方案，目前该功能缺失，需注意工作流规避。
- **即将上线功能**：个性化（Personalization）与情绪板（Moodboards）功能即将推出。
- **局限性依然存在**：大全景/复杂场景线条仍会碎/糊在一起；中式东方风格学得杂，效果不如即梦，中文提示词在中式场景效果更好但时不时男女不分；首饰等细节仍有瑕疵；材质/形体/物种要求叠加多了出图质量下降。
- **手部细节改善**：手指细节有明显进步，但仔细看仍有瑕疵，可结合 NBP（Negative Prompt Booster）修复。

---

### 🎯 关键洞察

**sref code 是 Niji V7 的核心杠杆**：真实风格用 Niji V7 会有"潮潮的线条不够真实"的感觉，因此 Niji V7 的最优使用场景是插画和动漫风格，而非写实风格。sref code 决定了风格差异的主要变量，获取渠道可在 IMA 知识库（同名）搜索。

**工具链组合逻辑**（原因→动作→结果）：
- 原因：单一工具各有短板，Niji V7 擅长风格化角色/环境，NBP 擅长分镜延展，视频工具擅长动态处理
- 动作：Niji V7 生成风格独特的人物角色和环境设定图 → NBP 做分镜和构图延展 → 视频工具动态处理
- 结果：分镜图、场景图、商用广告图均可高效完成

---

### 📦 配置/工具详表

| 场景/功能 | 关键提示词/参数 | 预期效果 | 注意事项/坑 |
|----------|--------------|---------|-----------|
| 动漫截图风格 | `anime screenshot --ar 16:9 --stylize 750 --niji 7` | 清晰线条、动漫质感 | 复杂多角色场景线条易碎 |
| 高细节单角色 | `--chaos 5 --ar 16:9 --stylize 800 --niji 7` | 细节丰富、光影准确 | 大全景整体细节仍差一点 |
| 简约插画/Logo | `minimalist graphic logo --niji 7` | 大面积留白、平面化 | 元素少时错误无处遮盖，需精准描述 |
| 线条质感体验 | `anime screenshot` | 线条传达形体/质感/光照 | — |
| 风格参考 | `--sref [code] --niji 7` | 风格锁定，提示词容错高 | 真实风格 sref 效果不如动漫风格 |
| 景深/电影感 | `shallow depth of field, bokeh effect --niji 7` | 前景虚化、电影质感 | — |
| 中式东方场景 | 使用中文提示词 + `--niji 7` | 中式氛围更准确 | 时不时男女不分，复杂中式场景建议用即梦 |
| 角色设定图 | 详细描述服装/配饰/武器 + `masterpiece, ultra-detailed, dramatic rim lighting --niji 7` | 人物设定精准，适合角色卡 | 首饰细节仍有瑕疵 |
| 异色瞳特写 | `heterochromia eyes, one eye crimson red one eye ice blue --niji 7` | 颜色准确区分，不再混色 | 之前版本会给紫色，V7 已修复 |

---

### 🛠️ 操作流程

1. **准备阶段**
   - 访问官方网页端：`https://www.midjourney.com/imagine`
   - 在界面切换模型至 **Niji V7**（界面有专属切换入口）
   - 确认当前不支持 cref，规避角色参考需求

2. **核心执行**
   - 单角色中景构图优先（方便查看细节，后续扩图/放大均方便）
   - 基础参数模板：`--chaos 5 --ar 16:9 --stylize 400~800 --niji 7`
   - stylize 值：400 = 平衡细节与风格；800 = 风格化更强
   - 需要风格锁定时追加：`--sref [code]`
   - 手部/细节有瑕疵时：交给 NBP 修复

3. **验证与优化**
   - 检查线条是否清晰（大全景/复杂场景线条碎是已知问题）
   - 检查提示词中的空间位置描述是否被正确执行（V7 字面理解增强）
   - 原先氛围感提示词若效果变差，需重写为更具体的描述
   - 中式场景若效果不佳，切换即梦或改用中文提示词

---

### 💡 具体案例/数据

以下为实测有效的完整 Prompt 示例：

**动漫女孩（樱花场景）**
```
a cheerful anime girl with long pink twintails, sparkling magenta eyes, excited smile showing teeth, cherry blossom hair pins, pink gem earrings, pink lace choker, wearing pink sundress, standing under a blooming cherry blossom tree in a Japanese garden, petals floating in the air, stone lantern and koi pond in background, modern anime style, clean linework, vibrant pink color theme, fresh spring atmosphere, bright natural lighting --chaos 5 --ar 16:9 --stylize 400
```

**RPG矮人铸文师（半写实）**
```
a weathered male dwarf runesmith with wild grey beard with glowing runes braided in, intense orange eyes reflecting forge fire, concentrated gruff expression, wearing heavy leather apron over chainmail with burn marks, holding hammer crackling with runic energy, molten metal floating in magical pattern, underground forge background with rivers of lava and ancient stone carvings, semi-realistic digital painting style, detailed rendering, RPG character concept art aesthetic, mystical industrious atmosphere --chaos 5 --ar 16:9 --stylize 400 --niji 7
```

**景深效果（女巫酿药）**
```
witch brewing potion, face illuminated by glowing cauldron in focus, cluttered magic shop shelves blurred behind, floating ingredients soft in foreground, shallow depth of field, bokeh effect, anime illustration style, masterpiece, ultra-detailed, soft natural daylight, romantic fantasy atmosphere --ar 16:9 --niji 7
```

**sref code 实测有效编号**：
- `772402534` → 巴厘岛舞者，粗体平面矢量风，藏红花黄+薰衣草色调
- `1160301490` → 夸张比例涂鸦风，奶油色背景彩色线条
- `4280355464` → 俯视早餐桌，厚黑轮廓，蓝黄主色，纹理颗粒感
- `1003864270` → 海边女子，复古版画风，蓝色+珊瑚色，亚麻纹理

---

### 📝 避坑指南

- ⚠️ **cref 暂不可用**：角色参考功能在 Niji V7 中不支持，官方正在开发替代方案，现阶段工作流需绕开此功能。
- ⚠️ **氛围感提示词需重写**：V7 更偏字面理解，原先靠模糊氛围词驱动的提示词效果会变差，需改为具体描述。
- ⚠️ **大全景/复杂场景慎用**：多角色+复杂背景时线条易碎，建议先出中景单角色，再扩图。
- ⚠️ **中式场景不是强项**：东方风格学得杂偏日系，有中式需求直接用即梦，或改用中文提示词并接受男女不分的概率风险。
- ⚠️ **真实风格不适合 Niji V7**：真实风格会出现"潮潮的线条"感，写实需求请回 Midjourney 主模型。
- ⚠️ **首饰/手部细节仍有瑕疵**：手指细节改善但未完全解决，首饰复杂度高时容易崩，可用 NBP 后处理修复。
- ⚠️ **stylize 值影响风格化程度**：400 偏平衡，800 偏风格化，根据需求调整，不要无脑拉满。

---

### 🏷️ 行业标签

#NijiV7 #Midjourney #AI绘图 #动漫插画 #提示词工程 #sref #角色设计 #AI工具链 #图像生成

---

---
