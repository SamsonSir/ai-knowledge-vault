# AI图像与视频创作

## 15. [2026-01-30]

## 📓 文章 6


> 文档 ID: `MxHuwawNmiIRC9kKbaSc936PnBP`

**来源**: 小松鼠：一句话，三分钟，生成视频-最强视频Skill-Remotion | **时间**: 2026-01-30 | **原文链接**: `https://mp.weixin.qq.com/s/wrlxs_0t...`

---

### 📋 核心分析

**战略价值**: 用 Claude Code + Remotion Skill，非视频从业者可在 3 分钟内通过自然语言描述生成程序化 MP4 科普视频，彻底绕过 PR/AE 的学习曲线。

**核心逻辑**:

- Remotion 本质是「把视频当网页写」：每一帧 = React 组件在特定时间点的渲染结果，最终由系统按帧截图拼成 MP4
- 渲染机制：第 0 帧截图 → 第 1 帧截图 → … → 第 N 帧截图，1800 帧 = 60 秒视频（30fps）
- 动画全部是数学计算：`interpolate(frame, [0, 30], [0, 1])` 表示第 0 帧透明度 0 → 第 30 帧透明度 1，中间值自动插值
- `spring({ frame, fps: 30, config: { damping: 100 } })` 模拟物理弹簧效果，无需手调关键帧
- 场景切换通过 `frame` 变量的范围判断实现：`{frame >= 150 && frame < 450 && <Scene2 />}`，30fps 下 150 帧 = 5 秒
- 安装 Remotion Skill 后，Claude 自动掌握 `interpolate`、`spring`、`<Sequence>`、`<AbsoluteFill>` 等 API，可直接用自然语言驱动
- 3D 效果通过 Three.js 集成实现：30 行代码完成三维坐标系 + 发光球体 + 连线 + 自动旋转摄像机 + 30 个粒子
- 修改闭环极短：改代码 → 保存 → 浏览器自动刷新，全程不超过 5 秒看到效果
- 批量生产可完全无人值守：写一个模板组件，循环遍历数据数组，晚上挂机渲染，早上收视频文件
- 视频源码可 Git 管理、多人协作，这是传统二进制 MP4 文件做不到的

---

### 🎯 关键洞察

**为什么 Remotion 比传统剪辑软件更适合程序员/AI 用户？**

原因：传统剪辑（PR/AE）的操作单元是「时间轴上的关键帧」，修改一个参数只影响一个元素；Remotion 的操作单元是「组件 + 数学函数」，修改一个变量可以同步更新所有依赖它的动画。

动作：把视频创作从「手工调参」变成「声明式编程」，AI 可以直接生成完整可运行代码。

结果：作者（完全不懂视频制作）用 3 分钟生成了包含 8 个场景、3D 向量空间可视化、打字机效果的 Embedding 科普视频，主逻辑文件 600+ 行全部由 Claude 自动生成。

**核心限制**：AI 一键出片依然不稳定，配音、口播、字幕仍需人工二次加工。Remotion 解决的是「视觉动画生成」这一环，不是全流程自动化。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 安装 Remotion Skill（Claude Code） | `npx add-skill remotion/remotion-best-practices` | Claude 学会 Remotion 组件写法、动画 API、时间轴控制 | 必须先装 Skill，否则 Claude 生成的代码质量不稳定 |
| 安装全平台 Skill（含 Trae 等） | `npx skills add remotion-dev/skills` | 自动为所有主流支持 Skill 的 IDE 安装对应技能，生成一堆文件夹 | 文件夹较多，正常现象 |
| 启动预览服务 | `npm start` | 浏览器打开 `https://localhost:3000`，进入 Remotion Studio | 左侧视频列表选目标视频，下方有时间轴控制器 |
| 渲染最终视频（命令行） | `npm run render:embedding` | 输出 `out/embedding.mp4`，显示进度条 `Rendering frames (x/y)...` | 渲染时间取决于电脑配置，作者用时约 3 分钟 |
| 渲染最终视频（网页） | 点击 Remotion Studio 界面中的「渲染视频」按钮 | 同上 | 两种方式等效 |
| 淡入动画 | `const opacity = interpolate(frame, [0, 30], [0, 1])` | 1 秒淡入（30fps） | 改 `[0, 60]` 变 2 秒淡入 |
| 弹簧动画 | `spring({ frame, fps: 30, config: { damping: 100 } })` | 带回弹感的缩放效果 | `damping` 越大回弹越弱 |
| 旋转动画 | `interpolate(frame, [180, 450], [0, 360 * 2])` | 从第 6 秒到第 15 秒旋转两圈 | 帧数 ÷ 30 = 秒数 |
| 摄像机旋转速度 | `const cameraRotation = frame * 0.01` | 慢速自动旋转 3D 场景 | 改为 `frame * 0.02` 转速加倍 |
| 批量渲染 | `videos.forEach(video => render(<ScienceVideo data={video} />))` | 无人值守批量生成多个视频 | 可挂机过夜运行 |
| 输出格式配置 | `remotion.config.ts` | 控制输出格式、分辨率等 | 由 Claude 自动生成，一般无需手改 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 安装 Skill：`npx add-skill remotion/remotion-best-practices`
- 可选：`npx skills add remotion-dev/skills`（为 Trae 等其他 IDE 同步安装）
- 准备好你的内容原文（如 Markdown 文件），放到本地路径，例如 `d:/ai_learn_demo/ai-explainer/my_self_doc/向量数据库/小松鼠Embedding原文.md`

**2. 核心执行**

- 在 Claude Code 中用自然语言描述需求，直接引用原文路径：

```
@/d:/ai_learn_demo/ai-explainer/my_self_doc/向量数据库/小松鼠Embedding原文.md

这是我的文章原文，请你深度思考，理解如何能够更加适合视频展示，来科普这个知识点。

其中一些三维向量的演示，需要你用到react的一些库，找最合适的来使用。

可以在你理解remotion技能格式的基础上，写一篇文字语稿md保存，然后调用技能，最终生成视频。
```

- 如需酷炫效果，追加提示：「有没有比较酷炫或者非常适合科普的库？比如 three.js，请搜索 GitHub 给我参考答案」
- Claude 自动生成 3 个核心文件 + 2 个配置文件（见下方文件结构）

**3. 预览与调整**

- `npm start` → 打开 `https://localhost:3000`
- 拖动进度条查看任意时间点，点播放看完整效果
- 改代码 → 保存 → 浏览器自动刷新（5 秒内看到效果）
- 不懂代码直接告诉 AI「第 X 场景的标题颜色改成红色」，AI 精准定位代码位置修改

**4. 渲染输出**

- 点击 Studio 界面渲染按钮，或执行 `npm run render:embedding`
- 等待进度条完成，视频保存至 `out/embedding.mp4`

---

### 💡 具体案例/数据

**作者实际生成的 Embedding 科普视频文件结构**：

```
Root.tsx                  # 注册视频组件
EmbeddingVideo.tsx        # 主视频逻辑（600+ 行），后续微调入口
VectorSpace3D.tsx         # 3D 向量空间可视化（Three.js）
package.json              # 添加了渲染命令
remotion.config.ts        # 输出格式设置
```

**8 个场景的帧数分配（30fps）**：

| 场景 | 帧范围 | 时间范围 | 内容 |
|---|---|---|---|
| 场景 1 | 0–150 | 0–5 秒 | 开场动画，标题淡入 |
| 场景 2 | 150–450 | 5–15 秒 | 问题提出：计算机不认识文字只认识数字 |
| 场景 3 | 450–900 | 15–30 秒 | 向量转换，打字机效果显示向量数字 |
| 场景 4–8 | 900+ | 30 秒后 | 后续 5 个场景（原文未展开） |

**3D 向量空间核心代码（VectorSpace3D.tsx）**：

```tsx
export const VectorSpace3D = () => {
  const frame = useCurrentFrame()

  const dogPos = new Vector3(0.2, 0.8, 0.3)  // 狗
  const catPos = new Vector3(0.3, 0.7, 0.4)  // 猫
  const carPos = new Vector3(0.9, 0.1, 0.2)  // 汽车

  const cameraRotation = frame * 0.01  // 自动旋转

  return (
    <ThreeCanvas>
      {/* 坐标轴：X红 Y绿 Z蓝 */}
      <mesh position={dogPos}>绿球</mesh>
      <mesh position={catPos}>蓝球</mesh>
      <mesh position={carPos}>红球</mesh>
      <line>狗猫之间距离线（黄色）</line>
      {[...Array(30)].map(() => <粒子 />)}
    </ThreeCanvas>
  )
}
```

**批量生产模板**：

```tsx
const videos = [
  { title: "Embedding", duration: 90 },
  { title: "向量数据库", duration: 120 },
  { title: "RAG", duration: 60 }
]

videos.forEach(video => {
  render(<ScienceVideo data={video} />)
})
```

**5 个卡片依次飞入（每个延迟 10 帧）**：

```tsx
cards.map((card, i) => {
  const delay = i * 10
  const opacity = interpolate(frame - delay, [0, 20], [0, 1])
  return <Card opacity={opacity} />
})
```

---

### 📝 避坑指南

- ⚠️ AI 一键出片不稳定：配音、口播、字幕仍需人工二次加工，Remotion 只解决视觉动画生成这一环
- ⚠️ Skill 必须先装：不装 Remotion Skill 直接让 Claude 写 Remotion 代码，质量和稳定性明显下降
- ⚠️ `npx skills add remotion-dev/skills` 会生成大量文件夹：这是为多 IDE 适配，属正常现象，不要误删
- ⚠️ 帧数换算别搞错：30fps 下，帧数 ÷ 30 = 秒数；150 帧 = 5 秒，450 帧 = 15 秒，900 帧 = 30 秒
- ⚠️ 渲染时间取决于硬件：作者渲染约 3 分钟，复杂 3D 场景更长，建议挂机等待
- ⚠️ 修改代码不需要懂 React：直接用自然语言告诉 AI 要改什么，AI 会精准定位代码位置

---

### 🏷️ 行业标签

#Remotion #ClaudeCode #程序化视频 #ReactVideo #AIGC #科普视频 #ThreeJS #视频自动化 #AISkill #内容生产

---

---
