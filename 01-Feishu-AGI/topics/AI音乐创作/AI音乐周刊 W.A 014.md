# AI音乐创作

## 8. [2026-02-09]

## 📓 文章 6


> 文档 ID: `PQTpwZaR1ikW3MkGnONcox4Vnre`

**来源**: AI音乐周刊 W.A 014 | **时间**: 2026-02-07 | **原文链接**: https://mp.weixin.qq.com/s/7iBZNi1QRxgBwmqoDVWr-w

---

### 📋 核心分析

**战略价值**: 本期周刊覆盖 2026 年 2 月第一周 AI 音乐生态的全面爆发——资本、工具、版权、学术四条线同步推进，是当前 AI 音乐产业格局的高密度快照。

**核心逻辑**:

- **AudioShake 五模型矩阵**：1 月 29 日发布，新增主唱/和声分离（Lead vs Backing）、电吉他/木吉他二分法、Keys 键盘模型（合成器/管风琴/电钢）、更新版高保真 Piano 模型，共 5 款。卡拉 OK 公司 Singa 已率先采用主唱分离功能。所有模型已上线 AudioShake Live、Indie 平台及 API。
- **Apple 收购 Q.ai**：2 月 2 日完成，估值 16-20 亿美元，为 Apple 史上第二大并购（仅次于 Beats 30 亿美元）。核心技术是通过"面部皮肤微动"识别"无声语音（Silent Speech）"，未来 AirPods/智能眼镜用户仅凭嘴部动作即可下达指令。创始人 Aviad Maizels 前作 PrimeSense 已成为 Face ID 基础。约 100 名员工整体并入 Apple 硬件技术部门。
- **LALAL.AI VST 插件**：2 月 3 日发布，支持 Ableton Live、FL Studio 等主流 VST3 宿主，调用 Lyra 模型本地处理，消除云端上传/下载摩擦。当前仅支持人声/伴奏分离，6 种乐器多轨分离功能开发中。仅向 Premium 订阅用户开放。
- **UMG vs Suno 公关战**：2 月 3 日爆发。Suno 首席音乐官 Paul Sinclair 主张"开放工作室"——AI 应赋能粉丝自由创作；UMG 高管 Michael Nash 坚持"围墙花园"——禁止用户将生成衍生作品下载并分发至 Spotify 等外部平台。UMG 已迫使 Udio 接受禁止下载条款，但 Suno 坚持开放并获华纳音乐（WMG）支持，UMG 同时对 Suno 提起诉讼。
- **ACE-Step 1.5 开源**：2 月 4 日登陆 Hugging Face、ModelScope、ComfyUI。显存占用 <4GB，RTX 3090 生成完整歌曲（10 秒至 10 分钟）<10 秒，A100 上 <2 秒。质量定位介于 Suno v4.5 与 v5 之间。架构：LM（思维链 CoT 规划歌词/元数据蓝图）+ DiT（音频生成），对齐通过内在强化学习实现，无需外部奖励模型。支持 50+ 语言、LoRA 风格微调（仅需几首歌）、翻唱、局部重绘。
- **Musical AI 融资**：2 月 4 日完成 450 万美元，Heavybit 领投，BDC 和 Build Ventures 跟投。成立于 2023 年，洛杉矶。核心是版权归因（Attribution）基础设施：版权持有者可实时监控并执行下架；AI 公司获取合规训练数据并根据归因报告向创作者支付版税。CEO Sean Power 称已实现"Turnkey"级追踪流程。
- **SIQA 合规榜单**：2 月 4 日发布全球首个 AI 音乐周榜，含"AI Music Top 100"原创榜与"Top 100 AI Covers"翻唱榜。门槛：必须标注 AI 生成/辅助、正确署名、严禁克隆真实公众人物（在世或已故）声音、不得冒充真实艺术家。
- **ElevenLabs D 轮**：2 月 4 日，5 亿美元，红杉领投，a16z 和 ICONIQ 跟投，估值 110 亿美元（一年内翻三倍）。2025 年 ARR 超 3.3 亿美元。战略重心转向 ElevenAgents（企业对话式 AI 平台），已服务德国电信、Revolut、乌克兰政府。联合创始人 Mati Staniszewski 明确 IPO 目标。
- **Suno Studio 1.2**：2 月 6 日发布，四项核心更新：①去除混响获取干声（生成两个版本供选择）；②Warp 标记时间伸缩（支持量化至 1/4、1/8 网格）；③多拍号支持（3/4、6/8 等，打破 4/4 限制）；④备选版本管理（同轨试听所有 Takes，红点标记未听版本，一键复制到主轨道）。
- **Metamorph 1.1**：AutoTune 家族产品，核心更新为全面兼容 RVC 模型（可导入社区或个人训练模型，支持自定义名称与色彩标签）、智能音域匹配（自动映射至目标模型黄金音域）、全局拖拽机制。Metamorph 正版用户及 AutoTune Unlimited 订阅用户免费升级。

---

### 🎯 关键洞察

**ACE-Step 1.5 的架构突破逻辑**：
传统音乐生成模型要么依赖纯扩散（质量高但可控性差），要么依赖纯语言模型（可控但音质受限）。ACE-Step 1.5 的 LM+DiT 混合架构解决了这一矛盾：LM 通过 CoT 先生成"歌曲蓝图"（歌词+元数据+结构说明），再由 DiT 执行音频生成。关键在于对齐机制采用内在强化学习（无外部奖励模型），避免了 RLHF 引入的人类偏好偏差。结果：消费级硬件（<4GB 显存）实现商业级质量，LoRA 微调门槛极低。

**UMG vs Suno 的本质是分发权之争**：
UMG 的"围墙"策略核心不是反对 AI 创作，而是阻止 AI 生成内容绕过版权体系直接进入 Spotify 等分发渠道，与人类艺术家争夺流媒体收益。Suno 的开放路线则押注 UGC 生态（类比 YouTube 时代），认为开放才能做大市场。华纳支持 Suno 说明大厂内部对此策略存在分歧。Musical AI 的版权归因基础设施恰好是这场博弈的"第三条路"——技术上实现追踪与分成，而非封堵。

**ElevenLabs 的战略转型信号**：
从"文本转语音"工具转向"全栈音频生态"，ElevenAgents 的企业客户（德国电信、Revolut、乌克兰政府）说明其已从 B2C 工具转向 B2B 基础设施。110 亿估值对应 3.3 亿 ARR，约 33x PS，反映市场对其平台化潜力的定价。

---

### 📦 配置/工具详表

| 工具/产品 | 核心功能 | 关键参数/限制 | 获取方式 |
|----------|---------|------------|---------|
| ACE-Step 1.5 | 本地音乐生成，LM+DiT 架构 | 显存 <4GB，RTX 3090 <10s/曲，支持 50+ 语言，LoRA 微调 | https://github.com/ace-step/ACE-Step-1.5 / https://acemusic.ai/ |
| AudioShake 新模型 | 主唱/和声分离、电/木吉他分离、Keys 模型、Piano 模型 | 共 5 款新模型 + 1 款更新 | https://developer.audioshake.ai/ |
| LALAL.AI VST | DAW 内直接调用 Lyra 模型分轨 | 仅 Premium 用户；当前仅人声/伴奏；VST3 宿主 | https://www.lalal.ai/ |
| Suno Studio 1.2 | 干声导出、Warp 时间伸缩、多拍号、备选版本管理 | 支持 3/4、6/8 等拍号；量化至 1/4、1/8 网格 | Suno Studio 内更新 |
| Metamorph 1.1 | RVC 模型兼容、智能音域匹配、全局拖拽 | 正版用户及 AutoTune Unlimited 免费升级 | https://www.antarestech.com/products/creative-vocal-effects/metamorph |
| YooHe | AI 音乐创作/生成/编辑/分轨，集成 ACE-STEP 1.5 | 精准分离 38 种独立音轨；公测免费 | https://www.yoohe.net/login?inviteCode=ac5e0323 |
| Musical AI | 版权归因基础设施，连接版权方与 AI 公司 | 实时监控+版税分成 | 企业 API 接入 |
| ROLI AI Music Coach | 红外视觉手部姿态识别 + 40 语言语音交互钢琴教学 | 需 Airwave 硬件；封闭测试 2 月 5 日开启，公测 3 月底 | Airwave 用户申请 |

---

### 🛠️ 操作流程：本地部署 ACE-Step 1.5

1. **准备阶段**
   - 硬件要求：显存 ≥4GB 的 NVIDIA GPU（RTX 3090 为参考机型）
   - 平台选择：Hugging Face / ModelScope / ComfyUI 三选一
   - 访问项目：https://github.com/ace-step/ACE-Step-1.5

2. **核心执行**
   - 按 README 拉取模型权重（<4GB 显存占用）
   - 输入格式：自然语言 Prompt → LM 通过 CoT 生成歌词+元数据蓝图 → DiT 执行音频生成
   - 支持参数：语言（50+）、时长（10 秒至 10 分钟）、风格 LoRA（仅需几首歌训练）
   - 高级功能：翻唱模式、局部重绘（Inpainting）、人声转背景乐

3. **验证与优化**
   - 生成速度基准：RTX 3090 <10 秒/完整曲，A100 <2 秒
   - 质量基准：介于 Suno v4.5 与 v5 之间
   - 风格定制：训练 LoRA 微调，仅需少量参考曲目即可捕捉个人风格
   - 在线试玩验证效果：https://acemusic.ai/

---

### 🛠️ 操作流程：Suno Studio 1.2 干声导出到 DAW

1. **准备阶段**：在 Suno Studio 内生成目标音频
2. **核心执行**：
   - 选择"Remove FX / Dry Stems"→ 系统生成两个干声版本 → 选择满意版本
   - 如需调整律动：启用 Warp 标记，拖拽调整 Timing；使用 Quantize 对齐至 1/4 或 1/8 网格
   - 如需特殊拍号：在生成前设置 3/4、6/8 等拍号，网格显示随之变化
3. **验证与优化**：
   - 导出干声至 DAW（Ableton/FL Studio 等）进行专业混音
   - 备选版本管理：同轨查看所有 Takes，红点标记未听版本，满意则"复制到主轨道"

---

### 💡 具体案例/数据

- **AudioShake + Singa**：卡拉 OK 公司 Singa 已采用 AudioShake 主唱/和声分离模型，在保留背景和声的同时精准去除原唱。
- **ACE-Step 1.5 性能数据**：A100 <2 秒/曲，RTX 3090 <10 秒/曲，显存 <4GB，质量介于 Suno v4.5 与 v5 之间。
- **ElevenLabs 财务数据**：2025 年 ARR 超 3.3 亿美元，D 轮估值 110 亿美元（一年内翻三倍），本轮融资 5 亿美元。
- **Musical AI**：成立于 2023 年，本轮 450 万美元，Heavybit 领投。
- **Q.ai 并购**：估值 16-20 亿美元，Apple 史上第二大并购；约 100 名员工并入；创始人 Aviad Maizels 前作 PrimeSense → Face ID。
- **BASS 基准**：包含 2658 个问题，涉及 1993 首歌曲，138 小时以上音频，覆盖 12 个任务，评估 14 个开源及前沿多模态 LM。
- **AI-OpenBMAT 数据集**：3294 个一分钟音频片段（54.9 小时），使用 Suno v3.5 生成风格匹配续作；现有检测模型在广播场景（背景音乐+短时长）下 F1 分数降至 60% 以下。

---

### 📝 避坑指南

- ⚠️ **LALAL.AI VST 当前版本限制**：初期仅支持人声/伴奏二分离，6 种乐器多轨分离尚在开发中，不要期望现阶段实现完整乐器分轨。
- ⚠️ **ACE-Step 1.5 显存边界**：官方标注 <4GB，但实际生成长曲（接近 10 分钟）时显存占用可能接近上限，建议先用短曲测试。
- ⚠️ **Suno Studio 1.2 干声版本选择**：系统生成两个干声版本，需人工试听对比，不是唯一确定性输出。
- ⚠️ **SIQA 榜单红线**：克隆真实公众人物声音（无论在世或已故）是硬性禁区，违规内容不会入榜，且面临法律风险。
- ⚠️ **UMG 诉讼风险**：Suno 目前仍处于 UMG 诉讼中，使用 Suno 生成内容进行商业分发需关注后续判决对分发权的影响。
- ⚠️ **AI 音乐检测盲区**：现有检测模型在广播场景（音乐被语音掩盖、片段短于完整曲目）下性能大幅下降（F1 <60%），广播/影视场景的 AI 内容合规核查不能依赖现有工具。
- ⚠️ **音乐 LLM 损失函数陷阱**：标准交叉熵损失在遇到系统性损坏音乐时反而会下降，不能单独用损失绝对值评估生成质量，应关注损失曲线形状（轮廓）而非绝对值。

---

### 📝 论文速查表

| 论文 | 核心贡献 | 链接 |
|-----|---------|------|
| WEALY | 基于 Whisper 解码器嵌入的可复现歌词匹配流程，达到 SOTA 水平 | https://arxiv.org/abs/2510.08176 |
| ACE-Step v1.5 | LM+DiT 混合架构，内在 RL 对齐，消费级硬件商业级质量 | https://arxiv.org/abs/2602.00744 |
| LSA-Probe | 白盒成员推理攻击，通过反向扩散几何属性检测训练数据版权合规 | https://arxiv.org/abs/2602.01645 |
| 噪声降低损失悖论 | 损失曲线形状（非绝对值）才是音乐质量的有效代理指标 | https://arxiv.org/abs/2602.02738 |
| 元数据 LLM 描述生成 | 元数据预测→LLM 转换，训练后可灵活更改风格化，支持元数据填充 | https://arxiv.org/abs/2602.03023 |
| D3PIA | 离散扩散+邻域注意力，基于主旋律谱生成钢琴伴奏，POP909 基准 | https://arxiv.org/abs/2602.03523 |
| BASS | 2658 题/1993 首歌/138 小时，评估音频 LM 音乐结构与语义推理 | https://arxiv.org/abs/2602.04085 |
| AI-OpenBMAT | 广播场景 AI 音乐检测数据集，揭示现有检测器在广播环境下的失效 | https://arxiv.org/abs/2602.06823 |

---

### 🏷️ 行业标签
#AI音乐 #音频分离 #开源模型 #版权归因 #语音AI #音乐生成 #DAW工具 #ACEStep #ElevenLabs #Suno #UMG #RVC #VST插件 #音乐教育 #无声语音

---

---
