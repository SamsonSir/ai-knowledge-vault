# 大模型技术架构

## 12. [2026-01-27]

## 📔 文章 5


> 文档 ID: `KuzgwC5dzih1e2kVGx2cCh0qnQd`

**来源**: 一文带你读懂DeepSeek-OCR 2的细节！附实测！ | **时间**: 2026-01-28 | **原文链接**: `https://mp.weixin.qq.com/s/DlT8o4FQ...`

---

### 📋 核心分析

**战略价值**: DeepSeek-OCR-2 用 LLM 替换传统 ViT 作为视觉编码器，首次在编码器中引入 prefix LM 双流注意力架构，解决了 2D 视觉 Token 排序问题，同时统一了编解码架构，为原生多模态奠基。

**核心逻辑**:

- **V1→V2 唯一核心改动**：视觉编码模块从 ViT（纯 Encoder，全双向注意力）替换为 LM 格式编码器（Qwen2-0.5B-base 初始化）
- **ViT 的根本缺陷**：图像 Patch 是 2D 结构，直接线性化后加位置编码，等价于强制从左上到右下顺序阅读，双栏排版、竖版文字等场景会产生视觉-语义 Gap
- **排序方案的选型过程**：
  - encoder-decoder（mBART 式交叉注意力）→ 视觉 token 处于独立编码器内，实验发现难以收敛，放弃
  - 纯 decoder（因果注意力）→ 前面 token 看不到后面 token，对图像理解不合理，放弃
  - **最终选型**：prefix LM 结构（双向 + 因果双流注意力），视觉 token 区域全双向互见，可学习 query token 区域因果单向
- **prefix LM 不是首创**：UniLM（三种结构并行）、ChatGLM1 均用过此结构，但在视觉编码器中首次使用
- **双流注意力的 mask 实现逻辑**：通过 `token_type_ids` 区分图像位置（type=0）和文本位置（type=1），图像位置之间 mask 置 0（互相可见），文本位置只能看到自身及之前内容（因果）
- **可学习 query 的作用**：与视觉 token 交互，有效压缩视觉信息，提升表征能力
- **三步训练流程**（顺序不可乱）：
  1. 仅训练 DeepEncoder-V2 + 尾部 MLP，预测 token 内容，初始化 Vision Tokenizer 和 LLM 编码器
  2. LLM 编码器 + DeepSeek-LLM 解码器联合训练，增强可训练 Query 的表征能力
  3. 仅训练 DeepSeek-LLM 解码器，专注理解 DeepEncoder-V2 重排序后的视觉 Token 序列
- **架构统一的战略意义**：视觉编码用 LM、解码也用 LM，编解码架构完全统一，为原生多模态打基础
- **工程用途**：① DeepSeek-LM 问答时处理用户上传图片（先 OCR 转文字再给 LLM）；② 给 DeepSeek 自身生产预训练数据

---

### 🎯 关键洞察

**为什么 prefix LM 能解决排序问题**：

传统 ViT 的全双向注意力无法感知阅读顺序，而纯因果 LM 又会让图像前半部分 token 无法感知后半部分的视觉上下文。prefix LM 的核心是用 mask 矩阵做"分区治理"：图像区域保持全双向（保留空间语义完整性），query 区域保持因果（强制按序压缩信息）。这样模型既能理解图像的 2D 空间关系，又能按序输出排列后的视觉 token 序列。

**排序带来的直接收益**：视觉 token 重排序后，编辑距离指标明显下降，竖版文字识别准确率显著提升。

---

### 📦 核心代码：自定义 4D Attention Mask

```python
def _create_custom_4d_mask(self, sequence_length, dtype, device, batch_size, token_type_ids):
    min_dtype = torch.finfo(dtype).min
    masks = []
    for b in range(batch_size):
        # 初始化全 mask（全不可见）
        mask = torch.full((sequence_length, sequence_length), fill_value=min_dtype, dtype=dtype, device=device)
        type_ids = token_type_ids[b]
        image_positions = (type_ids == 0).nonzero(as_tuple=True)[0]  # 图像 token 位置
        text_positions  = (type_ids == 1).nonzero(as_tuple=True)[0]  # 文本/query token 位置

        # 图像区域：非因果（全双向，互相可见）
        if len(image_positions) > 0:
            mask[image_positions[:, None], image_positions] = 0.0

        # 文本/query 区域：因果（只能看到图像 + 自身及之前的文本）
        for i, text_pos in enumerate(text_positions):
            if len(image_positions) > 0:
                mask[text_pos, image_positions] = 0.0          # 可看到所有图像 token
            mask[text_pos, text_positions[:i + 1]] = 0.0       # 只能看到自身及之前文本

        masks.append(mask)
    mask = torch.stack(masks, dim=0).unsqueeze(1)
    return mask
```

**关键参数说明**：
- `token_type_ids == 0`：图像 token，双向注意力
- `token_type_ids == 1`：文本/query token，因果注意力
- `min_dtype`：用 float 最小值填充表示"不可见"（softmax 后趋近于 0）

---

### 📦 配置/工具详表

| 模块 | 关键设置 | 预期效果 | 注意事项 |
|------|---------|---------|---------|
| 视觉编码器 | Qwen2-0.5B-base 初始化 | 替代 ViT，支持 LM 格式编码 | 非从零训练，用预训练 LM 权重初始化 |
| 注意力结构 | prefix LM（双向+因果双流） | 解决 2D 排序问题 | 需自定义 4D mask，不能用标准 causal mask |
| 可学习 query | 与视觉 token 交互 | 压缩视觉信息 | Step2 专门训练此部分表征能力 |
| 解码器 | DeepSeek-LLM | 理解重排序后的视觉 token | Step3 单独微调，不动编码器 |
| 评测基准 | OmniDocBench v1.5 | 端到端 OCR 综合评测 | PaddleOCR-VL 在此榜单仍领先 |

---

### 🛠️ 三步训练流程

1. **Step 1 - Vision Tokenizer 预训练**
   - 训练对象：DeepEncoder-V2 + 尾部 MLP
   - 初始化：Vision Tokenizer（DeepEncoder）+ LLM 编码器（Qwen2-0.5B-base）
   - 目标：预测 token 内容，建立视觉编码基础能力

2. **Step 2 - Query 表征增强**
   - 训练对象：LLM 编码器 + DeepSeek-LLM 解码器
   - 目标：增强可训练 Query 与视觉 token 的交互表征能力

3. **Step 3 - 解码器专项微调**
   - 训练对象：仅 DeepSeek-LLM 解码器
   - 目标：专注理解 DeepEncoder-V2 重排序后的视觉 Token 序列

---

### 💡 实测结果数据

| 场景 | 结果 | 备注 |
|------|------|------|
| 机打文字 OCR | 准确率高 | 基础场景表现稳定 |
| 简单手写体 | 识别正确 | 笔迹清晰时无问题 |
| 复杂连笔手写体 | 会出错 | 过于连笔时失败 |
| 表格文字内容 | 识别正确 | 文字本身没问题 |
| 表格结构 | 识别错误 | 结构还原是当前短板 |
| 生僻字/形近字 | 识别正确 | 相较 V1 有提升 |
| 竖版文字 | 有提升 | 排序机制带来的直接收益 |
| 简单公式 | 识别正确 | 无问题 |
| 复杂公式 | 丢失信息 | 可能与输入图片分辨率过低有关 |

**榜单对比**：OmniDocBench v1.5 端到端评测中，DeepSeek-OCR-2 相较 DeepSeek-OCR V1 有大幅提升，但 PaddleOCR-VL 仍排名更高。视觉 token 排序的编辑距离指标明显下降（正向）。

---

### 📝 避坑指南

- ⚠️ **表格结构识别不可靠**：文字内容准确但结构还原会出错，生产环境中表格场景需后处理或结合专用表格解析工具
- ⚠️ **复杂公式需高分辨率输入**：复杂公式丢失信息的问题可能与图片尺寸过小有关，使用时确保公式图片分辨率足够
- ⚠️ **连笔手写体是硬伤**：简单手写可用，过于连笔的场景当前版本仍会出错，不适合作为手写识别主力
- ⚠️ **PaddleOCR-VL 在榜单上仍更强**：端到端场景若追求最高精度，DeepSeek-OCR-2 不是当前最优选，其核心价值在架构创新而非 SOTA 性能
- ⚠️ **三步训练顺序不可跳过**：Step1 建立视觉编码基础，Step2 训练 query 交互，Step3 才微调解码器，顺序依赖明确

---

### 🏷️ 行业标签

#DeepSeek #OCR #VLM #prefixLM #视觉编码器 #多模态 #LLM架构 #Qwen2 #OmniDocBench #原生多模态

---

---
