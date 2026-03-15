# 大模型技术架构

## 37. [2026-03-11]

## 📘 文章 3


> 文档 ID: `TlJ1w1ITfiqT96krO9xcvAW4nbh`

**来源**: Gemini Embedding 2：原生多模态 embedding 模型 | **时间**: 2026-03-11 | **原文链接**: `https://mp.weixin.qq.com/s/RQPjydhs...`

---

### 📋 核心分析

**战略价值**: Gemini Embedding 2 是首个将文本、图片、视频、音频、PDF 统一编码进同一向量空间的商用 API，彻底消除多模态检索的多模型拼接架构。

**核心逻辑**:

- **统一向量空间是核心突破**：以前做跨模态检索（如用文字搜视频片段），需要为每种模态单独跑模型、单独建索引、再写代码拼结果。现在一次 API 调用、一个向量、一个索引搞定所有模态。
- **支持模态范围**：文本（最多 8192 tokens）、图片（最多 6 张，PNG/JPEG）、视频（最长 128 秒，MP4/MOV）、音频（最长 80 秒，MP3/WAV，不支持 AAC/FLAC）、PDF（最多 6 页），支持 100+ 语言，可混合传入同一次调用。
- **Matryoshka 缩维几乎无损**：默认 3072 维，支持灵活缩维。768 维存储成本是 3072 维的 1/4，MTEB 分数仅掉 0.18（68.17 → 67.99）。反直觉细节：1536 维（68.17）比 2048 维（68.16）还高 0.01，Google 官方推荐优先用 3072、1536、768 三个档位。
- **纯文本性能未退步**：前代 gemini-embedding-001 仍排 MTEB English 榜第一，均分 68.32，领先第二名 5 分以上。Embedding 2 在纯文本上没有明显差距，核心增量在多模态。
- **竞品对比**：Cohere Embed v4 支持文本+图片（128K 长上下文，不支持音频/视频）；CLIP 系列、Jina CLIP v2、Nomic 均只支持图片+文本；开源侧 Qwen3-Embedding-8B 拿到 70.58 分（纯文本），NVIDIA Llama-Embed-Nemotron-8B 领跑多语言 MTEB，但目前均为纯文本。Gemini Embedding 2 是唯一在商用 API 中覆盖全模态 + 100 语言的。
- **真实落地案例**：法律科技公司 Everlaw（CTO Max Christoff）用于诉讼发现（litigation discovery），在百万级记录上精确率和召回率均有提升，图片和视频搜索是之前架构完全无法实现的能力。
- **生态集成已就绪**：LangChain、LlamaIndex、Haystack、Weaviate、QDrant、ChromaDB、Pinecone、Vertex AI Vector Search 均已支持。
- **当前状态是 Public Preview**：API 容量可能受限，规格在正式发布前可能变动，做原型没问题，上生产需谨慎评估。
- **向量空间不向后兼容**：gemini-embedding-001 和 gemini-embedding-2-preview 向量空间完全不同，升级必须对整个数据集重新编码并重建索引，无渐进迁移路径。

---

### 🎯 关键洞察

**为什么统一向量空间是质变而非量变**：

传统多模态检索的架构是"各模态独立编码 → 各自建索引 → 后融合（late fusion）"，这意味着跨模态相似度计算本质上是在不同语义空间之间做近似映射，精度天花板低，且工程复杂度随模态数量线性增长。

Gemini Embedding 2 的原生多模态编码（native multimodal embedding）是"早融合（early fusion）"——模型在训练阶段就学习了不同模态之间的语义对齐关系，输出的向量直接可比。这使得"用一句话描述搜到对应的视频片段"这类任务从架构层面变得可行，而不是靠后处理技巧凑合。

Everlaw 的案例印证了这一点：诉讼发现场景中，证据材料混合了文字、图片、视频，之前的架构根本无法统一检索图片和视频，现在可以直接做。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 模型名称 | `gemini-embedding-2-preview` | 调用多模态 embedding | Public Preview，规格可能变动 |
| 文本输入 | 最多 8192 input tokens | 长文本编码 | 超出截断 |
| 图片输入 | 最多 6 张，PNG/JPEG | 图片语义向量 | 不支持其他格式 |
| 视频输入 | 最长 128 秒，MP4/MOV | 视频片段检索 | 超过需自行分片 |
| 音频输入 | 最长 80 秒，MP3/WAV | 音频语义检索 | 不支持 AAC/FLAC；30 分钟录音需切 20+ 段 |
| PDF 输入 | 最多 6 页 | 文档检索 | 合同/研报/论文基本超限，需分页处理 |
| 向量维度 | 3072（默认）/ 1536 / 768 | 灵活存储/性能平衡 | 推荐用 3072、1536、768 三档；1536 比 2048 分数略高 |
| Batch API | 半价 | 降低大批量编码成本 | — |
| 向量兼容性 | 与 gemini-embedding-001 不兼容 | — | 升级必须全量重新编码，无渐进迁移 |

---

### 🛠️ 操作流程

**1. 准备阶段**

安装 SDK：
```bash
pip install google-genai
```
获取 API Key，通过 Gemini API 或 Vertex AI 接入。

**2. 核心执行**

多模态混合调用示例（文本 + 图片 + 音频，一次调用返回一个向量）：

```python
from google import genai
from google.genai import types

client = genai.Client()

result = client.models.embed_content(
    model="gemini-embedding-2-preview",
    contents=[
        "What is the meaning of life?",
        types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/png",
        ),
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/mpeg",
        ),
    ],
)
```

**3. 维度选择策略**

| 场景 | 推荐维度 | 理由 |
|------|---------|------|
| 精度优先 | 3072 | 最高 MTEB 68.17 |
| 精度/存储平衡 | 1536 | 同分 68.17，存储减半 |
| 存储敏感/大规模 | 768 | 存储 1/4，分数仅降 0.18 |

**4. 长媒体分片处理**

- 音频超过 80 秒：按 75 秒切片（留 5 秒余量），逐片编码后建索引
- 视频超过 128 秒：按 120 秒切片
- PDF 超过 6 页：按 6 页分组，逐组编码

**5. 验证与优化**

- 接入框架：LangChain / LlamaIndex / Haystack / Weaviate / QDrant / ChromaDB / Pinecone / Vertex AI Vector Search 均已原生支持
- 多模态语义搜索 demo 可直接试用：`https://findmemedia.lmm.ai/`
- 参考 Logan K 的 X 帖子：`https://x.com/OfficialLoganK/status/2031411916489298156`

---

### 💡 具体案例/数据

- **Everlaw**（法律科技）：CTO Max Christoff 确认，在百万级诉讼证据记录上，精确率和召回率均有提升；图片和视频的语义搜索是之前架构完全无法实现的新能力。
- **MTEB 跑分对比**：

| 模型 | 维度 | MTEB English | 模态 |
|------|------|-------------|------|
| gemini-embedding-001 | — | 68.32（榜首，领先第二 5 分+） | 纯文本 |
| gemini-embedding-2-preview | 3072 | 68.17 | 文本+图片+视频+音频+PDF |
| gemini-embedding-2-preview | 1536 | 68.17 | 同上 |
| gemini-embedding-2-preview | 2048 | 68.16 | 同上 |
| gemini-embedding-2-preview | 768 | 67.99 | 同上 |
| Qwen3-Embedding-8B | 32~4096 | 70.58 | 纯文本（开源） |

---

### 📝 避坑指南

- ⚠️ **向量空间不兼容**：从 gemini-embedding-001 升级到 gemini-embedding-2-preview，必须对全量数据集重新编码并重建索引，没有任何渐进迁移方案，提前规划重建成本。
- ⚠️ **音频格式限制**：只支持 MP3 和 WAV，AAC 和 FLAC 不支持。会议录音（通常为 AAC）需先转码再处理。
- ⚠️ **音频时长上限 80 秒**：30 分钟录音需切成 22+ 段，分片逻辑需自行实现。
- ⚠️ **视频时长上限 128 秒**：超过约 2 分钟的视频必须自行分片。
- ⚠️ **PDF 最多 6 页**：绝大多数合同、研报、论文都超限，必须分页批量处理。
- ⚠️ **Public Preview 状态**：API 容量可能受限，规格在正式 GA 前可能变动，生产环境上线前需评估稳定性风险。
- ⚠️ **维度选择**：不要选 2048，1536 维分数反而更高（68.17 vs 68.16），且存储更小。

---

### 🏷️ 行业标签

#多模态Embedding #向量数据库 #GeminiAPI #语义搜索 #RAG #AI基础设施 #DeepMind

---

---
