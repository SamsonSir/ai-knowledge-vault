# AI学习与效率工具

## 17. [2026-05-05]

## 📓 文章 6


> 文档 ID: `YtGvwN2JsiCpjck1pe5cUQNVnba`

**来源**: o3 新玩法让奥特曼惊呼！包浆老照片也被 AI 精准定位，全程高能 | **时间**: 2025-05-05 | **原文链接**: `https://mp.weixin.qq.com/s/E44Mh_1w...`

---

### 📋 核心分析

**战略价值**: o3 凭借纯像素推理（无 EXIF、无 GPS）实现地理位置识别，配合专业 GeoGuessr 提示词可超越顶级人类选手，但记忆污染与过早锁定假设是其核心缺陷。

**核心逻辑**:

- **o3 图片推理能力已达顶级选手水平**：在 GeoGuessr 竞技场景中，o3 直接击败了人类顶级选手，Sam Altman 本人也表示"没想到"。
- **包浆照片（2008年拍摄）也能识别**：一张极度模糊的河流照片，o3 给出4个候选（恒河上游、下密西西比河、黄河、湄公河），最终正确答案是湄公河，说明模型对低质量图像的容错能力极强。
- **核心能力来源是提示词工程**：该 prompt 本质上是资深 GeoGuessr 玩家的"心法文档化"，强制 o3 关注人行道砖块大小、马路牙子、施工标记、电缆、栅栏结构、天光阴影、坡度等具有地区差异的细节。
- **禁用 EXIF 是测试的关键约束**：测试者通过截图方式二次处理图片，确保模型无法读取原始 EXIF 元数据，验证的是纯视觉推理能力。
- **记忆（Memory）会污染推理**：o3 在识别 InD 艺术节搭建现场时，因聊天记录中的历史上下文"帮助"了推理；但在后续更难的任务中，同样的记忆反而成为干扰项，导致模型坚持错误答案（TIT 创意园区）。
- **过早锁定假设是 o3 的已知缺陷**：即使用户提示"那半截字像不像'海'字"，o3 仍坚持外白渡桥而非海珠桥，并生成详细表格为自己辩护——这是典型的确认偏误（confirmation bias）。
- **AI 幻觉的危险形式：有图有据的错误**：o3 会生成看似合理的"证据表格"来支撑错误结论，用户面临的风险不是"AI说不知道"，而是"AI信誓旦旦说自己对"，极易被说服。
- **隐私风险已被验证**：仅凭一张随手拍的照片，o3 就能定位真实地点，开盒成本极低，隐私威胁是实质性的。
- **室内往外拍摄会显著增加难度**：从室内向外拍摄的图片，因缺少外部参照物，反向定位难度大幅上升，o3 在此类场景表现明显下降。
- **汉字识别仍是弱项**：海珠桥图片中有半截汉字，o3 未能准确识别，与其在图片/海报生成任务中文字错误的问题一致。

---

### 🎯 关键洞察

**为什么这个 prompt 有效**：

普通用户问"这是哪里"，模型会泛泛作答。这个 prompt 的价值在于把专家的认知框架强制注入模型的推理流程：

- 原因：模型默认推理路径会过早收敛到第一个高置信候选
- 动作：prompt 强制执行"始终保持两个假设存活到最后"、"主动寻找反驳证据"、"检查附近同特征区域"
- 结果：推理质量从"直觉猜测"升级为"系统性排除"

**记忆污染的双刃剑效应**：

- 正向：历史对话中提到过某地点 → 模型在候选列表中优先考虑 → 命中率提升
- 负向：历史对话中强关联了某地点 → 模型在新任务中过度锚定 → 即使证据不足也不愿放弃

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| EXIF 屏蔽 | 截图后再上传（非直接上传原图） | 强制模型只用像素推理 | 截图会留灰边，属正常现象 |
| 候选数量控制 | prompt 要求第一轮输出恰好5个候选，且第1和第5相距≥160km | 防止候选过于集中 | 模型有时会违反此规则需人工检查 |
| 假设保活机制 | "keep two hypotheses alive until the very end" | 防止过早锁定 | 模型仍会偷偷放弃第二假设 |
| 搜索关键词矩阵 | 步骤3½：生成"地区中性"搜索词 | 发现雷达外的候选地区 | 不能用 Google Maps/卫星图（反爬限制） |
| 影子测纬度 | θ ≈ arctan(H/S)，纬度 ≈ 90°-θ+太阳赤纬，误差±0.5-1°（≈111km） | 从阴影角度估算纬度范围 | 需要知道拍摄季节才能算太阳赤纬 |
| 植被分类 | 区分人工种植（玫瑰、草坪）vs 自然生长（橡树、灌木） | 排除不符合本地植被的候选 | 城市绿化会引入外来物种干扰判断 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 将原图截图一次（去除 EXIF），上传截图而非原图
- 将下方完整 prompt 粘贴到 o3 对话框
- 上传图片，发送

**2. 核心执行（prompt 规定的6步协议）**

1. **Step 0 - 伦理设置**：声明不读元数据，仅用像素，标记方向（图片"上方"=相机朝向）
2. **Step 1 - 原始观察**（≤10条）：只记录可直接看到/测量的事实（颜色、纹理、数量、阴影角度、字形），不含解释性形容词；重点扫描路灯/电线杆（颜色、悬臂、底座类型）、人行道砖块尺寸、路缘石细节、围栏硬件、屋顶/门廊风格数量
3. **Step 2 - 分类推理**（每类≤2句）：气候与植被 / 地貌 / 建筑环境 / 文化与基础设施 / 天文光照 / 区分人工vs自然植被
4. **Step 3 - 第一轮候选**：输出恰好5个候选表格（含支撑线索和置信度1-5），确保第1和第5相距≥160km；同时生成"地区中性"搜索关键词矩阵
5. **Step 4 - 暂定领先者**：命名当前最佳猜测+一个同等力度测试的备选；明确写出"证伪标准"（如果看到X，此猜测作废）；确认用户同意后才进入搜索步骤
6. **Step 5 - 验证计划**：列出每个候选需验证的元素和具体搜索词/街景目标
7. **Step 6 - 锁定**（最关键，最易失败）：主动问自己"我是否过早收窄了？附近有没有相同特征的区域？"；列出可能性，主动寻找支持它们的证据；直接对比领先猜测与邻近城市，不带偏向；最终给出坐标或最近地名，声明残余不确定性（km半径）

**3. 验证与优化**

- 如果模型坚持错误答案：不要直接告诉答案，而是提供具体的视觉线索（如"那半截字像不像某个字"）
- 如果模型生成"证据表格"为自己辩护：这是确认偏误信号，可以明确要求它"重新从零开始，假设你的第一个猜测是错的"
- 清除历史记忆或开新对话，可以减少记忆污染对推理的干扰

---

### 💡 具体案例/数据

| 测试图片 | 难度 | o3 表现 | 结果 |
|---------|------|---------|------|
| 2008年湄公河包浆照片 | 高（极度模糊） | 给出4个候选，湄公河在列 | ✅ 正确 |
| 夜景高架桥（有半截汉字） | 中（有线索但模糊） | 第一轮候选包含海珠桥，最终选外白渡桥 | ❌ 错误（海珠桥） |
| InD 艺术节搭建现场（无 logo） | 高（无标识） | 借助聊天记忆正确识别 | ✅ 正确 |
| 室内往外拍摄（无外部参照） | 极高 | 第一轮有接近答案，后被记忆带偏，坚持认为是 TIT 创意园区 | ❌ 错误 |

---

### 📝 避坑指南

- ⚠️ **不要直接上传原图**：原图含 EXIF 地理信息，模型可能直接读取，测试结果失去意义
- ⚠️ **模型"信誓旦旦"≠模型正确**：o3 会生成详细表格为错误答案辩护，不要被说服，要求它重新证伪
- ⚠️ **记忆功能是双刃剑**：长期对话中积累的地点记忆会干扰新任务推理，敏感测试建议开新对话
- ⚠️ **Step 6 是最高失败率步骤**：模型在"锁定"阶段最容易过早收敛，需要人工干预要求它主动寻找反驳证据
- ⚠️ **汉字/小字识别是弱项**：图中有中文字符时，不要假设模型能准确读取，需要额外提示
- ⚠️ **仅限个人娱乐**：此能力可用于定位真实人物位置，用于刺探他人隐私属于违法/违规行为

---

### 完整 Prompt 原文

```
You are playing a one-round game of GeoGuessr. Your task: from a single still image, infer the most likely real-world location. Note that unlike in the GeoGuessr game, there is no guarantee that these images are taken somewhere Google's Streetview car can reach: they are user submissions to test your image-finding savvy. Private land, someone's backyard, or an offroad adventure are all real possibilities (though many images are findable on streetview). Be aware of your own strengths and weaknesses: following this protocol, you usually nail the continent and country. You more often struggle with exact location within a region, and tend to prematurely narrow on one possibility while discarding other neighborhoods in the same region with the same features. Sometimes, for example, you'll compare a 'Buffalo New York' guess to London, disconfirm London, and stick with Buffalo when it was elsewhere in New England - instead of beginning your exploration again in the Buffalo region, looking for cues about where precisely to land. You tend to imagine you checked satellite imagery and got confirmation, while not actually accessing any satellite imagery. Do not reason from the user's IP address. none of these are of the user's hometown.

**Protocol (follow in order, no step-skipping):**

Rule of thumb: jot raw facts first, push interpretations later, and always keep two hypotheses alive until the very end.

0. Set-up & Ethics
No metadata peeking. Work only from pixels (and permissible public-web searches). Flag it if you accidentally use location hints from EXIF, user IP, etc. Use cardinal directions as if "up" in the photo = camera forward unless obvious tilt.

1. Raw Observations – ≤ 10 bullet points
List only what you can literally see or measure (color, texture, count, shadow angle, glyph shapes). No adjectives that embed interpretation. Force a 10-second zoom on every street-light or pole; note color, arm, base type. Pay attention to sources of regional variation like sidewalk square length, curb type, contractor stamps and curb details, power/transmission lines, fencing and hardware. Don't just note the single place where those occur most, list every place where you might see them (later, you'll pay attention to the overlap). Jot how many distinct roof / porch styles appear in the first 150 m of view. Rapid change = urban infill zones; homogeneity = single-developer tracts. Pay attention to parallax and the altitude over the roof. Always sanity-check hill distance, not just presence/absence. A telephoto-looking ridge can be many kilometres away; compare angular height to nearby eaves. Slope matters. Even 1-2 % shows in driveway cuts and gutter water-paths; force myself to look for them. Pay relentless attention to camera height and angle. Never confuse a slope and a flat. Slopes are one of your biggest hints - use them!

2. Clue Categories – reason separately (≤ 2 sentences each)
Category Guidance
Climate & vegetation: Leaf-on vs. leaf-off, grass hue, xeric vs. lush.
Geomorphology: Relief, drainage style, rock-palette / lithology.
Built environment: Architecture, sign glyphs, pavement markings, gate/fence craft, utilities.
Culture & infrastructure: Drive side, plate shapes, guardrail types, farm gear brands.
Astronomical / lighting: Shadow direction ⇒ hemisphere; measure angle to estimate latitude ± 0.5
Separate ornamental vs. native vegetation: Tag every plant you think was planted by people (roses, agapanthus, lawn) and every plant that almost certainly grew on its own (oaks, chaparral shrubs, bunch-grass, tussock). Ask one question: "If the native pieces of landscape behind the fence were lifted out and dropped onto each candidate region, would they look out of place?" Strike any region where the answer is "yes," or at least down-weight it. °.

3. First-Round Shortlist – exactly five candidates
Produce a table; make sure #1 and #5 are ≥ 160 km apart.
| Rank | Region (state / country) | Key clues that support it | Confidence (1-5) | Distance-gap rule ✓/✗ |

3½. Divergent Search-Keyword Matrix
Generic, region-neutral strings converting each physical clue into searchable text. When you are approved to search, you'll run these strings to see if you missed that those clues also pop up in some region that wasn't on your radar.

4. Choose a Tentative Leader
Name the current best guess and one alternative you're willing to test equally hard. State why the leader edges others. Explicitly spell the disproof criteria ("If I see X, this guess dies"). Look for what should be there and isn't, too: if this is X region, I expect to see Y: is there Y? If not why not? At this point, confirm with the user that you're ready to start the search step, where you look for images to prove or disprove this. You HAVE NOT LOOKED AT ANY IMAGES YET. Do not claim you have. Once the user gives you the go-ahead, check Redfin and Zillow if applicable, state park images, vacation pics, etcetera (compare AND contrast). You can't access Google Maps or satellite imagery due to anti-bot protocols. Do not assert you've looked at any image you have not actually looked at in depth with your OCR abilities. Search region-neutral phrases and see whether the results include any regions you hadn't given full consideration.

5. Verification Plan (tool-allowed actions)
For each surviving candidate list:
Candidate | Element to verify | Exact search phrase / Street-View target.
Look at a map. Think about what the map implies.

6. Lock-in Pin
This step is crucial and is where you usually fail. Ask yourself 'wait! did I narrow in prematurely? are there nearby regions with the same cues?' List some possibilities. Actively seek evidence in their favor. You are an LLM, and your first guesses are 'sticky' and excessively convincing to you - be deliberate and intentional here about trying to disprove your initial guess and argue for a neighboring city. Compare these directly to the leading guess - without any favorite in mind. How much of the evidence is compatible with each location? How strong and determinative is the evidence? Then, name the spot - or at least the best guess you have. Provide lat / long or nearest named place. Declare residual uncertainty (km radius). Admit over-confidence bias; widen error bars if all clues are "soft".

Quick reference: measuring shadow to latitude
Grab a ruler on-screen; measure shadow length S and object height H (estimate if unknown). Solar elevation θ ≈ arctan(H / S). On date you captured (use cues from the image to guess season), latitude ≈ (90° – θ + solar declination). This should produce a range from the range of possible dates. Keep ± 0.5–1 ° as error; 1° ≈ 111 km.
```

---

### 🏷️ 行业标签
#o3 #图像推理 #GeoGuessr #提示词工程 #地理定位 #隐私安全 #AI幻觉 #记忆污染

---

---
