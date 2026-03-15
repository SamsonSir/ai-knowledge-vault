# AI图像与视频创作

## 12. [2026-01-22]

## 📚 文章 8


> 文档 ID: `Y5N0wDKCjil9XCkOhkpcYKZ7n1e`

**来源**: Flora Flow：面向花店现场的花艺搭配工具 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 用 CBIR + 多实例匈牙利算法 + Gemini 多模态推理，解决花店现场"多花材组合搭配是否成立"这一无法用传统以图搜图解决的组合美学判断问题。

**核心逻辑**:

- **问题本质不是识别，而是组合判断**：拍立淘/小红书只能解决"单个物品像不像"，但插花设计的难点是"多种花材放在一起是否成立"，这是一个组合美学判断问题，不是单实例检索问题。
- **色差与花头大小是现场决策的两大障碍**：网购花材存在严重色差（如蓝紫色海洋之歌变成紫红色玫瑰），且花头大小难以判断，直接影响主花选定和颜色占比分布。
- **数据质量决定应用体验上限**：CBIR 数据库需经过：第三方采集 → 人工清洗 → SegFormer 去背景 → OWL-V2 单实例识别 → 人工清洗模糊/遮挡/ROI 面积小的实例 → CLIP 向量化（实例级 + 整图级，均为 512 维）。
- **功能1 核心算法是多实例匈牙利算法**：用户选定多个花材后，3 秒无操作触发请求，对所选花材做 CLIP 向量化，与 CBIR 数据库做多实例组最大匹配计算（匈牙利算法），召回 TopK 结果。这是行业较少见的多物品搭配检索方案（Pinterest/拍立淘均只支持单实例）。
- **功能2 用 Gemini 做 spatial understanding 替代人工标注意图**：用户输入自然语言意图（如"暖橙色系，浪漫风格，周年纪念"）+ 花店现场照片，Gemini 推理后以 BBOX 形式圈选 2~3 个花材，切割实例后再走匈牙利算法召回。
- **功能2 最终得分 = 花材相似性 + 语义相似性加权**：用户 query 经 CLIP 向量化为 512 维，与 CBIR 整图离线向量做语义相似性计算，再与花材实例相似性做简单加权，得出最终排序得分。
- **功能3 用 Nano Banana Pro 生成花艺作品，但效果偏传统**：生成轮廓以圆形/扇形为主，设计雷同缺乏美感，仅用于启发。根本原因：大模型是概率回归模型，数据取值于高概率区域，生成结果固化，而创作设计本质是"异常值行为"，需突破主流设计语言。
- **多模态融合方案选型对比**：简单加权（直观易调试，但缺乏推理能力）vs 二次排序（效果不稳定）vs POOL 池化（维度下降不确定，如白玫瑰+红玫瑰 POOL 后是否变成粉红玫瑰存疑）vs MLP cross attention（效果最强，但需训练专门模型）。
- **细分场景才能做多层级实例检索**：大模型可指定不同层级实例（如服装/上衣/领口/发型）做图像检索，但前提是 CBIR 数据库也做了对应层级的实例分割和特征工程，否则产生维度爆炸，无法建立索引。
- **应用场景定位为盒马鲜生货架**：用户扫小程序，辅助线下导购，解决现场花材不齐全、色感不准、搭配不确定的三重障碍。

---

### 🎯 关键洞察

**为什么匈牙利算法是核心**：插花搭配是"一组花材 vs 一组花材"的最优匹配问题，不是"一朵花 vs 一朵花"。匈牙利算法解决的是二分图最大权匹配，能在多个花材实例之间找到全局最优的相似性组合，而非逐一比对后简单求和，避免了局部最优导致的搭配误判。

**为什么 Gemini 的 spatial understanding 是关键创新**：传统 CBIR 需要用户手动框选或精确描述，Gemini 可以直接从自然语言意图推理出"应该选哪几朵花"并输出 BBOX 坐标，将用户意图与图像空间位置打通，实现了"意图 → 花材选定 → 实例切割 → 向量检索"的全自动管线。

**为什么生成式 AI 不适合做创意设计**：大模型训练目标是最大化高概率区域的输出，生成结果天然趋向"大众审美均值"。而设计创新本质是偏离均值的异常值行为，两者目标相悖。Flora Flow 的功能3 因此只定位为"启发"而非"决策"。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 背景去除 | SegFormer 图像分割，mask 掉背景 | 减少背景色对相似匹配的干扰 | 背景复杂时分割边缘可能不干净，需人工复查 |
| 实例识别 | OWL-V2 零样本物体识别，对插花作品中每朵花单独识别 | 划分多个实例，支持多实例检索 | 需人工清洗模糊、遮挡、ROI 面积小的实例 |
| 向量化 | CLIP，实例级 512 维 + 整图级 512 维 | 同时支持花材相似性和语义相似性计算 | 实例和整图需分别离线处理并存储 |
| 多实例匹配 | 匈牙利算法，多实例组最大匹配 | 召回 TopK 搭配作品 | 行业较少见，Pinterest/拍立淘均不支持 |
| 意图推理 | Gemini，输入用户 query + 花店照片，输出 BBOX JSON | 自动圈选 2~3 个匹配花材 | query 需先翻译为英文再做 spatial understanding |
| 语义相似性 | 用户 query → CLIP 512 维，与 CBIR 整图向量计算余弦相似度 | 兼顾风格语义匹配 | 简单加权缺乏推理能力，橙色款无法召回等边缘 case 需注意 |
| 花艺生成 | Nano Banana Pro，输入 query + 花店照片，生成新花艺图 | 启发性设计参考 | 生成结果偏传统（圆形/扇形），设计雷同，仅供启发 |

---

### 🛠️ 操作流程

**1. 准备阶段：CBIR 数据库构建**
- 从第三方网站采集插花作品图片
- 人工数据清洗（去除低质量图片）
- 用 SegFormer 对每张图做背景 mask
- 用 OWL-V2 对每张图中的鲜花做零样本识别，切割出多个实例
- 人工清洗模糊、遮挡、ROI 面积小的实例
- 用 CLIP 对每个实例单独向量化（512 维）+ 对整张图向量化（512 维），存入数据库

**2. 核心执行：三条功能管线**

功能1（手动选花材）：
- 用户拍摄花店现场照片
- OWL-V2 实时识别现场鲜花
- 用户手动选择多个花材
- 3 秒无操作后触发请求
- 对所选花材做 CLIP 向量化
- 匈牙利算法计算多实例组最大匹配，召回 TopK 结果

功能2（意图推荐）：
- 用户输入自然语言意图 + 上传花店照片
- 调用 Gemini，使用以下 Prompt：
```
Use the user query to select up to 3 distinct flower entities in the image that best match the intent. User query: {query}. First translate the user query into English and use that translation for spatial understanding. Return ONLY JSON (no markdown) as an object with keys "query_en" and "boxes". "query_en" is the English translation of the user query (or the original if already English). "boxes" is a list of up to 3 items, each with keys "label" (Chinese flower or foliage name only) and "box_2d" as [ymin, xmin, ymax, xmax] normalized to 0-1000. Avoid overlapping boxes; keep them tight around petals/texture; skip tiny or blurry regions. If fewer than 3 are visible, return the best available ones.
```
- Gemini 返回 BBOX JSON，切割对应花材实例
- 切割实例走匈牙利算法，计算花材相似性
- 用户 query 经 CLIP 向量化，与 CBIR 整图向量计算语义相似性
- 简单加权合并两路得分，输出最终排序结果

功能3（生成花艺作品）：
- 用户输入意图 + 上传花店照片
- 调用 Nano Banana Pro，使用以下 Prompt：
```
Generate a new floral arrangement image based on the user query and the uploaded market image. Query: {query}. Use 2 flower visible in the uploaded image, coz I need to buy the flower according to design right now. Emphasize premium floral design with clear hierarchy, color harmony, OR texture contrast. Output image with new environment; no bounding boxes.
```
- 输出生成花艺图，仅作启发参考

**3. 验证与优化**
- 功能1/2 通过召回结果数量和相似度分布判断搭配是否"成立"（大量高相似度结果 = 搭配成立；低相关或无结果 = 搭配罕见，风险高）
- 多模态融合方案可按需升级：简单加权 → 二次排序 → MLP cross attention（需训练专门模型）

---

### 💡 具体案例/数据

- 粉色芍药 + 蓝紫配花：召回大量高相似度作品，搭配成立
- 向日葵 + 黄玫瑰：召回结果极少，搭配罕见，存在不确定性风险
- 暖橙色系 + 浪漫风格 + 周年纪念：Gemini 选定 3 个橙色系花材（BBOX 圈选），召回 TOP1 匹配作品
- 网购色差案例：蓝紫色海洋之歌实际到货变成紫红色玫瑰，说明现场实时识别比网购预判更可靠
- CLIP 向量维度：实例级和整图级均为 512 维

---

### 📝 避坑指南

- ⚠️ 简单加权缺乏推理能力：例如"橙色款"这类颜色变体无法通过加权方式召回，需升级到二次排序或 MLP 方案
- ⚠️ 二次排序效果不稳定：第一次召回 TOP20 时可能未包含语义范围内的作品，导致二次排序失效
- ⚠️ POOL 池化存在语义漂移风险：白玫瑰 + 红玫瑰 POOL 后特征是否等同于粉红玫瑰不确定，而现场可能根本没有粉红玫瑰
- ⚠️ 多层级实例检索会导致维度爆炸：只能在细分场景（如专门的花艺场景）做多层级实例分割，通用场景无法建立有效索引
- ⚠️ 生成式 AI 不适合作为设计决策依据：Nano Banana Pro 生成结果固化（圆形/扇形为主），仅作启发，不可作为最终搭配方案
- ⚠️ OWL-V2 识别后需人工清洗：模糊、遮挡、ROI 面积小的实例必须清洗，否则影响向量化质量和召回精度

---

### 🏷️ 行业标签

#CBIR #多实例检索 #匈牙利算法 #Gemini多模态 #CLIP向量化 #OWL-V2 #SegFormer #花艺设计 #零售导购 #组合美学判断

---

---
