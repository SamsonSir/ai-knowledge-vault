# AI音乐创作

## 3. [2026-01-19]

## 📔 文章 5


> 文档 ID: `XILHwN1oniDWxikaf2qcINeQnJc`

**来源**: AI音乐周刊 W.A 011 | **时间**: 2026-01-13~19 | **原文链接**: `https://mp.weixin.qq.com/s/kNb3Qdsz7wEKTEXTnZYukg`

---

### 📋 核心分析

**战略价值**: 本期覆盖 AI 音乐领域一周内最密集的平台政策、融资、模型开源、工具更新与学术突破，是从业者快速校准行业方向的一手情报。

**核心逻辑**:

- **Bandcamp 禁令（1月13日）**: 首个主流平台明令禁止"完全或主要由 AI 生成"的音乐上传，同时禁止 AI 模仿他人风格。执行机制依赖用户举报，平台保留下架权。核心争议：2023年大裁员后审核人力严重不足；"生成式 AI"定义模糊，可能误伤 Vocaloid、随机算法等早期实验性音乐。Mirlo、Ampwall 等小平台此前已有更细化的类似政策。
- **Musical AI 融资（1月14日）**: 完成 450 万美元融资，Heavybit 领投，BDC Capital 和 Build Ventures 跟投。核心技术是"可辩护、可解释的归属（Attribution）"系统——对权利人提供版税透明度，对 AI 公司消除法律不确定性。CEO Sean Power 目标：建立标准化许可与支付体系。
- **Suno Studio 1.1（1月14日）**: 核心新功能是 Stem + Cover（分轨翻唱）——选中任意音轨，用文字描述改变音色（如哼唱转乐器、钢琴轨换吉他）；多轨导出时间从约 5 分钟压缩至约 10 秒；每条音轨新增独立 Track EQ；Project Browser 界面重设计。
- **HeartMuLa 开源（1月15日）**: 四模块全栈音乐模型家族：HeartCLAP（音频-文本跨模态对齐）、HeartCodec（12.5 Hz 极低帧率高保真编解码）、HeartTranscriptor（鲁棒歌词识别）、HeartMuLa 生成核心（LLM 驱动，支持文本风格+歌词+参考音频多条件输入）。特色：细粒度段落级风格控制（前奏/主歌/副歌独立定义）+ 短视频高吸引力短音乐生成模式。
- **Synthesizer V Studio 2 Pro 2.2.0（1月15日）**: 历经两年研发，发布合唱声库系列。首发三款：Collection 1（Gospel/Pop）、Collection 2（Classical）、Collection 3（Folk/Ceremonial），每款含 16 个独立声音，支持中/英/日等 6 种语言。新增 Unison 功能（单轨最多 16 人合奏，精准立体声控制）、内置 EQ+压缩+混响链+房间声学模拟、MusicXML 导入、钢琴卷帘音阶显示、渲染缓存优化。
- **Step-Audio-R1.1 开源（1月16日）**: 阶跃星辰发布端到端语音大模型，BigBench Audio 准确率 96.4%，超越 Grok、Gemini、OpenAI，登顶 Artificial Analysis 语音推理榜。首字延迟（TTFA）仅 1.51 秒。核心架构：双脑架构——"构思脑"（高级推理）与"表达脑"（语音生成）解耦，实现边推理边说话（Mind-Paced Speaking），同时通过声学基础推理直接基于音频特征思考，避免转录信息损耗。已在 HuggingFace 和 ModelScope 全面开源，支持 Docker 或自定义 vLLM 后端部署。
- **Reverse Lo-Fi 游戏（Qosmo × Google Magenta）**: 网页互动游戏，玩家实时选择 Prompt 方块生成背景音乐，目标是维持动漫女孩专注学习状态——音乐太静则打瞌睡，太动感则起身跳舞。核心技术：Google Magenta 实时音乐生成。
- **交互式 AI 音乐论述（Jordi Pons）**: 提出 AI 音乐三要素：互动性（实时响应用户输入）、艺术主导权（艺术家设计互动逻辑）、生成式（无预录音轨，每次独一无二）。援引案例：SENAIDA 生成式专辑、Suno/Sonauto AI 电台、Google Magenta 互动装置。核心判断：音乐正从"固定录音"向"生成系统"演变，类比游戏之于电影。当前挑战：聆听习惯从被动转主动、缺乏统一分发平台。

---

### 🎯 关键洞察

**Bandcamp 禁令的结构性矛盾**: 政策理念获社区支持，但执行依赖用户举报 + 人工审核，而平台在 2023 年已大规模裁员。这意味着禁令更多是"道德宣言"而非"技术防线"，短期内难以有效过滤。真正的技术检测（如 Musical AI 的归属系统）才是行业基础设施方向。

**Step-Audio-R1.1 双脑架构的工程意义**: 传统语音模型在"高推理质量"与"低延迟"之间存在硬性权衡——推理链越长，响应越慢。双脑解耦架构通过让构思脑和表达脑并行运作，打破了这一约束，1.51 秒 TTFA + 96.4% 准确率同时达成，是端到端语音模型的重要工程里程碑。

**HeartCodec 的技术突破点**: 12.5 Hz 帧率极低，意味着每秒仅需 12.5 个离散 token 表示音频，大幅降低序列长度，使 LLM 处理长结构音乐成为可能，同时保持高保真度——这是音乐生成模型长期面临的"长结构 vs 生成效率"矛盾的一个有效解法。

---

### 📦 配置/工具详表

| 工具/模型 | 关键功能/参数 | 获取/部署方式 | 注意事项 |
|---|---|---|---|
| Suno Studio 1.1 | Stem+Cover 分轨翻唱；多轨导出 ~10 秒；Track EQ | Suno 官网 Studio 界面 | 官方演示：`https://youtu.be/aYiUPPOWLWg?si=ItQ7mmJ369m9UF5N`；中文教程：`https://my.feishu.cn/wiki/T348wR406i06Iqk4rDEc1cb8nud?from=from_copylink` |
| HeartMuLa | HeartCLAP / HeartCodec(12.5Hz) / HeartTranscriptor / 生成核心；段落级风格控制 | `https://heartmula.github.io/` | 开源，支持多条件输入（文本+歌词+参考音频） |
| Synthesizer V Studio 2 Pro 2.2.0 | 合唱声库（3款×16声音×6语言）；Unison 单轨最多16人；内置 EQ+压缩+混响+房间声学 | `https://dreamtonics.com/choir-voice-collections/` | 历经两年研发，MusicXML 导入支持 |
| Step-Audio-R1.1 | 双脑架构；TTFA 1.51s；BigBench Audio 96.4% | HuggingFace：`https://huggingface.co/stepfun-ai/Step-Audio-R1.1`；ModelScope：`https://modelscope.cn/models/stepfun-ai/Step-Audio-R1.1`；在线：`https://www.stepfun.com/studio/audio?tab=conversation` | 支持 Docker 或自定义 vLLM 后端部署 |
| Reverse Lo-Fi | Google Magenta 实时生成；Prompt 方块交互 | `https://reverse-lofi.qosmo.jp/` | 网页直接体验，无需安装 |

---

### 🛠️ 操作流程：Suno Studio 1.1 分轨翻唱

1. **准备阶段**: 登录 Suno Studio，打开已有项目或新建一首歌曲，确保进入 Studio 编辑界面（非普通生成页面）。
2. **核心执行**: 在多轨视图中选中目标 Stem（如钢琴轨）→ 点击 Cover 按钮 → 输入文字描述目标音色（如"acoustic guitar, warm tone"）→ 确认生成。也可录入哼唱片段作为参考直接转换为乐器音色。
3. **导出**: 完成编辑后使用 Multitrack Export，等待约 10 秒（旧版约 5 分钟）获得分轨文件。
4. **后期调整**: 对各轨使用新增的独立 Track EQ 进行频率微调。

---

### 🛠️ 操作流程：Step-Audio-R1.1 本地部署

1. **准备阶段**: 确认环境支持 Docker 或 vLLM，从 HuggingFace（`https://huggingface.co/stepfun-ai/Step-Audio-R1.1`）或 ModelScope（`https://modelscope.cn/models/stepfun-ai/Step-Audio-R1.1`）下载模型权重。
2. **核心执行**: 选择 Docker 镜像直接部署，或配置自定义 vLLM 后端加载模型权重，启动推理服务。
3. **验证**: 发送语音输入，验证 TTFA 是否接近 1.51 秒，测试推理准确率是否达到预期水平；也可先通过在线体验（`https://www.stepfun.com/studio/audio?tab=conversation`）对比效果。

---

### 💡 具体案例/数据

- Step-Audio-R1.1：BigBench Audio 准确率 **96.4%**，TTFA **1.51 秒**，超越 Grok、Gemini、OpenAI，登顶 Artificial Analysis 语音推理榜。
- Musical AI：融资 **450 万美元**，Heavybit 领投。
- Suno 多轨导出：从 **~5 分钟** 压缩至 **~10 秒**。
- Synthesizer V 合唱声库：3 款声库，每款 **16 个独立声音**，支持 **6 种语言**（含中/英/日），研发历时 **2 年**。
- HeartCodec：**12.5 Hz** 极低帧率下保持高保真度。

---

### 📝 论文速览

| 论文 | 核心贡献 | 链接 |
|---|---|---|
| ICASSP 2026 ASAE 挑战赛 | AI 生成歌曲主观美学评分预测，赛道1（整体音乐性）+ 赛道2（5个细粒度评分），建立标准化基准 | `https://arxiv.org/abs/2601.07237` |
| 弹性泛音（Elastic Overtones） | 放宽八度=2倍频假设，构建可转调12半音系统，五度二次谐波精确匹配基频三次谐波，恢复纯律音质同时保留12TET转调能力 | `https://arxiv.org/abs/2601.08074` |
| FusID | 模态融合语义ID框架，联合编码跨模态信息，乘积量化转为离散Token，实现零ID冲突，MRR和Recall@k优于基线 | `https://arxiv.org/abs/2601.08764` |
| 扩散模型钢琴音色转换 | 音高编码器+响度编码器作为条件输入扩散解码器，支持古典/爵士/流行多风格，具备实时转换潜力 | `https://arxiv.org/abs/2601.09333` |
| SLAM-LLM | 开源多模态LLM框架，专注语音/音频/音乐，模块化配置编码器+投影器+LLM+PEFT插件，含ASR/AAC/MC高性能配方 | `https://arxiv.org/abs/2601.09385` |
| 合成数据鼓声转录（ADT） | 半监督方法从无标签音频自动整理单次鼓声采样库，仅用MIDI合成训练数据，ENST和MDB测试集达新SOTA | `https://arxiv.org/abs/2601.09520` |
| 线性复杂度音乐自监督学习 | Branchformer+SummaryMixing+随机量化，模型尺寸缩减8.5%~12.3%，MIR任务性能具竞争力 | `https://arxiv.org/abs/2601.09603` |
| 浅层扩散歌声移调修复 | 将移调重构为修复问题，轻量级梅尔空间扩散模型+f0/音量/内容特征条件，自监督训练，显著减少移调伪影 | `https://arxiv.org/abs/2601.10345` |
| LIVI 翻唱检索 | 歌词信息版本识别，训练时用转录+文本嵌入监督，推理时移除转录步骤保持轻量，MRR和Recall@k优于或持平和声系统 | `https://arxiv.org/abs/2601.11262` |

---

### 📝 避坑指南

- ⚠️ Bandcamp 禁令执行依赖用户举报，"生成式 AI"定义模糊，使用 Vocaloid、随机算法等早期技术的实验性音乐存在被误判风险，上传前需评估风险。
- ⚠️ Suno Studio 1.1 的 Stem+Cover 功能需在 Studio 界面操作，普通生成页面不可用。
- ⚠️ Step-Audio-R1.1 本地部署需确认 vLLM 版本兼容性，建议优先用 Docker 镜像避免环境问题。
- ⚠️ HeartCodec 12.5 Hz 极低帧率设计优先保障长结构捕捉，短片段生成效果需实测验证。
- ⚠️ Synthesizer V 合唱声库为付费产品，16 声音×3 款声库需分别购买，部署前确认授权范围。

---

### 🏷️ 行业标签

#AI音乐 #音乐生成 #版权归属 #语音模型 #开源模型 #虚拟歌手 #交互式音乐 #音乐信息检索 #扩散模型 #多模态LLM

---

---
