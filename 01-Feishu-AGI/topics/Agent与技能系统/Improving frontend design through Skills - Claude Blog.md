# Agent与技能系统

## 62. [2026-02-16]

## 📘 文章 3


> 文档 ID: `VRdywpKrLiievZkuq2ZcbQFennc`

**来源**: Improving frontend design through Skills - Claude Blog | **时间**: 2026-02-16 | **原文链接**: `https://claude.com/blog/improving-frontend-design-through-skills`

---

### 📋 核心分析

**战略价值**: 通过 Claude Skills 机制按需注入设计规范，系统性打破 AI 前端输出的"分布收敛"陷阱，将 AI 生成质量从"能用"提升到"惊艳"。

**核心逻辑**:

- **AI 设计收敛的根因是统计偏好**：训练数据中 Inter 字体、紫色渐变、白色背景出现频率最高 → AI 采样时优先选择高概率模式 → 输出"安全但无聊"的设计，这是机制问题，不是 bug
- **Skills 是"按需插件"而非"常驻内存"**：系统提示每次请求都携带（浪费 tokens、污染上下文），Skills 只在前端任务时加载，精准投放，不干扰 Python 调试等其他任务
- **负面清单比正面指令更有效**：明确禁止 Inter/Roboto/Arial、禁止紫色渐变，比说"用好看的字体"更能约束输出方向
- **防止"二次收敛"**：给了建议后 Claude 会从 Inter 换到 Space Grotesk，但仍然收敛。必须在 skill 中显式写明"你仍然倾向于收敛到 Space Grotesk，避免这个"
- **字体对比原则**：字重用极端值（100/200 vs 800/900，不要 400 vs 600），字号用 3x+ 跳跃（不要 1.5x），行高标题 1.1-1.2、正文 1.6-1.8
- **动画策略**：一个精心编排的页面加载错开动画（staggered reveals）比散落的微交互更有冲击力；CSS 优先，React 项目用 Framer Motion
- **背景分层**：用多层 CSS 渐变叠加（radial-gradient + linear-gradient）+ blend-mode 创造氛围，而非纯色背景
- **Skills 最佳大小**：300-1000 tokens，太小不够详细，太大加载慢且可能超出上下文
- **组合使用**：多个 skill 可叠加，如 `frontend-design + rpg-theme`，但需避免重复指令导致冲突
- **方法论可迁移**：识别收敛模式 → 提供替代方案 → 创建 Skill，同样适用于后端架构、API 设计、文档写作、测试用例生成

---

### 🎯 关键洞察

**为什么 Skills 优于系统提示**：

```
系统提示：每次请求都携带设计规范
→ 调试 Python 时也带着前端 CSS 规范
→ 上下文窗口臃肿
→ 影响非前端任务的输出质量

Skills：
→ 只在前端任务时加载
→ 节省 tokens
→ 上下文干净
→ 可复用、可团队共享
```

**提示词粒度的黄金区间**：
- 太死板（指定 `#2563eb` 这种 hex 色号）→ 失去创意空间
- 太模糊（"做好看点"）→ 等于没说
- 正确做法：给方向和原则（"用高对比度配色，主色 + 鲜明强调色"）

---

### 📦 配置/工具详表

| Skill 文件 | 核心内容 | 适用场景 | 关键注意事项 |
|---|---|---|---|
| `frontend-design.md` | 通用设计原则：字体/配色/动画/背景 | 所有前端项目 | 必须包含"防止二次收敛"的警告语句 |
| `use-interesting-fonts.md` | 禁用字体列表 + 推荐字体分类 + 配对原则 | 注重排版的项目 | 必须附带 Google Fonts `@import` 模板 |
| `rpg-theme.md` | 羊皮纸色调、中世纪字体、魔法粒子动画 | 游戏/奇幻主题 | 颜色用 `#f4e4bc`、`#e8d5a9` 等具体值 |
| `motion-design.md` | CSS keyframes 模板 + Framer Motion 指引 | 交互丰富的应用 | 动画时长：hover 0.2-0.3s，click 0.1-0.2s |
| `atmospheric-backgrounds.md` | 分层渐变 + 噪点纹理 + blend-mode | 视觉要求高的页面 | 避免喧宾夺主，背景服务于内容 |
| `company-design-system.md` | 品牌色 CSS 变量 + 组件模板 + 间距系统 | 生产环境/团队项目 | 团队共享到同一目录，保证一致性 |
| `ecommerce-ui.md` | 产品卡片、信任徽章、突出 CTA | 电商网站 | 移动优先 |
| `saas-dashboard.md` | 侧边栏导航、指标卡片、数据可视化 | 数据密集应用 | 需包含暗色模式支持 |

---

### 🛠️ 操作流程

**1. 准备阶段：创建 Skills 目录**

```bash
# macOS/Linux
mkdir -p ~/.config/claude-code/skills/
cd ~/.config/claude-code/skills/

# 检查配置路径
claude-code --config
```

**2. 核心执行：创建通用前端设计 Skill**

创建 `frontend-design.md`，写入以下内容（约 400 tokens）：

```xml
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

**3. 扩展：字体专项 Skill**

创建 `use-interesting-fonts.md`：

```xml
<use_interesting_fonts>
Typography instantly signals quality. Avoid using boring, generic fonts.

Never use: Inter, Roboto, Open Sans, Lato, default system fonts

Good choices by aesthetic:
- Code: JetBrains Mono, Fira Code, Space Grotesk
- Editorial: Playfair Display, Crimson Pro
- Technical: IBM Plex family, Source Sans 3
- Distinctive: Bricolage Grotesque, Newsreader
- Retro: VT323, Press Start 2P
- Elegant: Cormorant Garamond, Yeseva One

Pairing: High contrast = interesting.
- Display + monospace
- Serif + geometric sans
- Variable font across weights

Use extremes:
- Weight: 100/200 vs 800/900（not 400 vs 600）
- Size: 3x+ jumps（not 1.5x）
- Line height: Tight for headlines (1.1-1.2), Loose for body (1.6-1.8)

Always include:
@import url('https://fonts.googleapis.com/css2?family=[FONT_NAME]&display=swap');
</use_interesting_fonts>
```

**4. 扩展：动画 Skill**

创建 `motion-design.md`，核心 CSS 模板：

```css
/* 页面加载动画 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeInUp 0.6s ease-out forwards; }

/* 错开显示 */
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }

/* 悬停上浮 */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}
```

**5. 扩展：背景 Skill**

创建 `atmospheric-backgrounds.md`，核心模板：

```css
/* 分层渐变背景 */
background:
  linear-gradient(135deg, rgba(76, 29, 149, 0.1) 0%, transparent 50%),
  linear-gradient(225deg, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
  radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 40%);
```

**6. 企业设计系统 Skill**

创建 `company-design-system.md`，核心结构：

```css
:root {
  --primary: #2563eb;
  --primary-dark: #1e40af;
  --secondary: #10b981;
  --danger: #ef4444;
  --bg-main: #ffffff;
  --bg-alt: #f8fafc;
  --text-main: #0f172a;
  --text-muted: #64748b;
}

/* 字体加载 */
/* Plus Jakarta Sans (700,600,500) + Inter (400,500) + JetBrains Mono */
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

/* 按钮 */
.btn { padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; transition: all 0.2s ease; }
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: var(--primary-dark); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(37,99,235,0.3); }

/* 卡片 */
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }

/* 输入框 */
.input { width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 1rem; transition: border-color 0.2s, box-shadow 0.2s; }
.input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }

/* 间距系统：4, 8, 12, 16, 24, 32, 48, 64px */
/* 容器最大宽度：1200px；移动断点：768px */
```

**7. 验证与使用**

```
# 基础使用
"使用 frontend-design skill 创建一个 SaaS 落地页"

# 组合使用
"使用 frontend-design 和 rpg-theme skill 创建一个游戏角色选择界面"

# 指定技术栈（React）
"使用 web-artifacts-builder skill 创建一个 React 任务管理应用"

# 企业规范
"使用 company-design-system skill 创建登录页，要求：深色主题、社交登录按钮、淡入动画"
```

---

### 💡 具体案例/数据

**SaaS 落地页对比**：

| 维度 | 不用 Skill | 用 frontend-design Skill |
|---|---|---|
| 字体 | Inter | Space Grotesk 或其他特色字体 |
| 背景 | 白色纯色 | 深色 + 多层 radial-gradient 光晕 |
| 配色 | 紫色渐变 hero | CSS 变量管理，`--accent: #00ff9d` 鲜明强调色 |
| 动画 | 无 | fadeInUp 0.6s + stagger delay |
| 整体感 | 一眼 AI 生成 | 有设计感 |

**白板应用对比**（web-artifacts-builder）：

| 维度 | 不用 Skill | 用 Skill |
|---|---|---|
| 功能 | 基础绘图 | 矩形/圆形/线条/文本插入 |
| UI | 粗糙 | 完善的工具栏和交互反馈 |

**任务管理应用对比**：

| 维度 | 不用 Skill | 用 Skill |
|---|---|---|
| 功能 | 简单待办列表 | 标题+描述+截止日期+分类+日期选择器 |
| 表单 | 无验证 | 完善的表单验证和视觉反馈 |

---

### 📝 避坑指南

- ⚠️ **二次收敛陷阱**：给了字体建议后，Claude 会从 Inter 换到 Space Grotesk，但仍然每次都选 Space Grotesk。必须在 skill 中显式写"你仍然倾向于收敛到 Space Grotesk，避免这个"
- ⚠️ **Skill 文件过大**：超过 1000 tokens 会加载慢且可能超出上下文，精简到 300-1000 tokens 最佳
- ⚠️ **多 Skill 冲突**：组合使用时若两个 skill 有重复指令（如都定义了字体规范），可能产生冲突，保持每个 skill 职责单一
- ⚠️ **Claude.ai 需手动激活**：Claude.ai 目前不支持自动触发，每次必须在对话中明确说"使用 X skill"；Claude Code 可配置自动触发规则
- ⚠️ **指令粒度过细**：直接指定 hex 色号会限制创意空间，给方向和原则而非具体数值
- ⚠️ **Skill 中缺少代码示例**：强烈建议在 skill 中同时提供"应该这样写"和"不要这样写"的代码对比，效果远好于纯文字描述

---

### 🏷️ 行业标签

#Claude #Skills #前端设计 #AI提示词工程 #CSS #React #设计系统 #工作流优化

---

---
