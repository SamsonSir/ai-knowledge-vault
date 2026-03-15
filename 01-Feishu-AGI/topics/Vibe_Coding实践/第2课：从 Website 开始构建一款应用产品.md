# Vibe_Coding实践

## 3. [2026-01-11]

## 📕 文章 1


> 文档 ID: `TlFlwYnpbiWjdlky8QFcpgzdnrb`

**来源**: 第2课：从 Website 开始构建一款应用产品 | **时间**: 2026-03-13 | **原文链接**: WaytoAGI AI Coding实战训练营第2课

---

### 📋 核心分析

**战略价值**: 用 Vibe Coding（Enter.pro + Supabase）零代码完成一款具备前端申请、后台管理、数据库存储、数据埋点、移动适配的全栈 Web 产品的完整交付流程。

**核心逻辑**:

- **先想后做，流程图是最低成本的验证工具**：在动手前用流程图把学员侧（提交→等待→查看结果）和管理员侧（收单→审核→反馈）两条链路完整模拟一遍，直到每个节点的信息字段都清晰，再开始写 Prompt。
- **MVP 的本质是"最低成本验证假设"**：Granola 早期用人工实时听会议、手写纪要来验证"用户是否需要 AI 纪要"，而不是先造 AI 算法。结论：0-1 阶段不追求完美，只验证核心假设。
- **需求分级 P0/P1 是资源分配的核心决策**：本课案例中"账号收集+工单跟踪"是 P0 必做，"自动充值+品牌透出"是 P1 能做就做，明确优先级避免过度设计。
- **第一版只做纯前端**：先用 Enter.pro 跑通交互流程（无真实数据），验证 UI 路径和字段逻辑没问题，再接数据库。顺序：交互验证 → 数据接入 → 发布 → 迭代。
- **Plan 模式是 Vibe Coding 最重要的技巧之一**：在 Enter.pro 输入框选中 Plan，让 Agent 先输出详细执行计划（将模糊需求具体化 + 拆解实施阶段），确认无误后再执行，避免一把梭出错。
- **Supabase 接入不需要手动建表**：通过 Enter.pro 的 Supabase Connect 插件授权（两步：Organization 授权 → 具体 Project 连接），Agent 自动完成建表、权限配置、数据库访问代码注入。
- **发布 = Publish 一键操作，版本管理是必须有的意识**：Publish 后 30-60s 获得公网域名；每次发布前必须在预览版本测试完整，正式版本出问题可一键回退上一版本。
- **SEO 配置是基础卫生，两步验证**：看浏览器标签页标题是否更新；按 F12 打开 DevTool → Elements，检查 `<meta>` 标签是否有 description/keywords。让 Agent 根据产品实际情况自动补全。
- **数据埋点分两层**：基础层（GA/PostHog 自动采集页面曝光、滚动、通用交互）+ 关键事件层（Custom Event 手动上报，如学员提交申请表单）。原则：宁可多采不可漏采，不要多报重报。
- **移动端适配和品牌升级靠 Prompt 精度**：视觉迭代的瓶颈不是 AI 能力，是人的审美和 Prompt 描述精度。遇到卡点可以借助 Gemini 等工具先生成设计 Prompt，再喂给 Enter.pro 执行。

---

### 🎯 关键洞察

**产品思维的核心是"真实诉求 vs 表面诉求"**：
- 表面诉求：收集学员邮箱 → 工具：问卷
- 真实诉求：让学员账号持续有钱 → 工具：带状态跟踪的申请系统
- 演进诉求：自动触发充值（余额低于阈值时）→ 未来版本

**Vibe Coding 的天花板不是技术，是想法和执行力**：
- 你不需要会写代码，但你必须能清晰表达"我要什么"
- 0-1 阶段的 Prompt 可以很简洁，产品迭代中 0-1 只占极小比例
- 每一轮迭代都是：明确诉求 → 精准 Prompt → 验证结果 → 下一轮

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Enter.pro 新建项目 | 点击 New Project，输入 Prompt，选模型，回车 | 自动完成环境配置、仓库生成、编码、构建，约 3-5 分钟 | 第一版 Prompt 可以很简洁，不追求完美 |
| Enter.pro Plan 模式 | 输入框选中 Plan 后发送 Prompt | Agent 输出详细执行计划，确认后再执行 | 必学技巧，模糊需求先 Plan 再 Execute |
| Supabase Connect | Enter.pro 右上角插件按钮 → Supabase - Connect | Agent 自动建表 `applications`、配置权限、注入数据库访问代码 | 授权分两步：Organization 授权 + 具体 Project 连接，缺一不可 |
| 发布部署 | 右上角 Publish 按钮，等待 30-60s | 获得公网可访问域名，后续发布不换域名 | 发布前必须在预览版本完整测试；出问题可回退版本 |
| 版本管理 | 左侧聊天区域上方时间按钮 → 找 Online 版本 → 加书签 | 标记正式版本，便于回退 | 正式版本 ≠ 最新版本，必须手动标记 |
| SEO 配置 | 让 Agent 根据产品实际情况完成 SEO 配置 | 浏览器标签页标题更新；`<meta>` 标签有 description/keywords | F12 → Elements 验证 `<meta>` 标签是否更新 |
| GA4 接入 | 复制 GA 代码片段，通过对话让 Agent 插入 `index.html` | GA 平台显示"正确检测到 Google 代码"；48小时后数据完整 | 需要科学上网；接入后去 GA 设置媒体资源，勾选"开始采集应用数据" |
| GA Custom Event | `gtag('event', '事件名', {'参数名': '参数值'})` | GA 平台可查到自定义事件数据 | 让 Agent 在关键用户行为（如提交表单）处插入上报代码 |
| PostHog 接入 | 安装 `npx -y @posthog/wizard@latest`，配置环境变量，初始化 Provider，上报关键事件 `posthog.capture('event', {property: 'value'})` | PostHog 平台显示 Complete；可查看用户行为漏斗 | 接入后还需在 PostHog 后台配置授权域名（填正式版本链接） |
| 移动端适配 | 通过 Prompt 描述移动端场景，让 Agent 完成适配 | 手机访问无错位，文案不换行，按钮可点击 | 适配后需用真实手机验证，不能只看模拟器 |

---

### 🛠️ 操作流程

**1. 准备阶段：需求梳理与流程设计**

- 识别真实诉求（不是表面诉求），枚举所有解决方案，选出 P0 优先实现
- 画出完整用户流程图（学员侧 + 管理员侧），把每个节点的字段、状态、出口都想清楚
- 整理成需求文档表格，包含：页面模块、所属系统（前端/后台）、需求详情

本课案例的字段设计：

| 字段 | 类型 | 规则 |
|------|------|------|
| 邮箱地址 | 输入框 | 必填，校验邮箱格式 |
| 名称 | 输入框 | 必填，最多20字符，支持中英文 |
| 所学课程 | 下拉框 | 必填，选项从后端配置读取 |
| 工单状态 | 枚举 | 待处理 / 通过 / 驳回（含驳回理由） |

**2. 核心执行：三轮迭代**

- **v1（纯前端验证）**：用简洁 Prompt 让 Enter.pro 生成纯前端版本，验证交互路径是否符合预期
- **v2（交互精修）**：用完整详细的 Prompt（含用户路径、产品需求、字段规则、分页规则）重新生成，验证交互细节
- **v3（接入数据库）**：
  1. Enter.pro 插件 → Supabase Connect → 完成两步授权
  2. 输入框选 Plan，发送"好，我们需要开始接入数据库，不过在你开始编码前，我需要更加详细的执行计划"
  3. 确认计划后执行，Agent 自动建表、配权限、注入代码
  4. 人肉测试四步：学员提交→数据入库 ✅ / 管理员登录→库有新用户 ✅ / 管理员审核→数据同步 ✅ / 学员状态刷新→完整流程 ✅

**3. 发布与上线**

- 右上角 Publish → 等待 30-60s → 获得公网链接
- 左侧时间按钮 → 找 Online 版本 → 加书签（版本管理）
- 用真实手机重新跑一遍完整流程

**4. 验证与优化（SEO + 埋点 + 移动端 + 品牌）**

- SEO：让 Agent 完成配置，F12 验证 `<meta>` 标签和标签页标题
- GA4：
  1. GA 平台 → 数据流设置 → 选网站 → 填正式链接 → 创建
  2. 复制 gtag 代码，通过 Enter.pro 对话接入
  3. GA 平台测试安装 → 显示"正确检测到 Google 代码"
  4. 让 Agent 在提交表单处插入 Custom Event 上报
- PostHog：
  1. 安装 wizard，配置环境变量 `VITE_PUBLIC_POSTHOG_KEY` 和 `VITE_PUBLIC_POSTHOG_HOST`
  2. 初始化 `PostHogProvider` 包裹根组件
  3. 关键事件上报 `posthog.capture()`
  4. PostHog 后台配置授权域名
- 移动端：Prompt 描述移动端场景 → Agent 适配 → 真机验证
- 品牌升级：提供品牌截图 + 设计要求给 Agent；遇到审美卡点，先用 Gemini 生成设计 Prompt 再喂给 Enter.pro

---

### 💡 具体案例/数据

**Granola MVP 案例**：
- 问题：大多数 AI 工具 100% 转录会议内容，导致信息过载
- 验证方式：用户邀请机器人参会时，团队成员人工实时听会、手写纪要
- 验证结论：用户需要的不是全量转录，而是以关键词为线索组织的结构化笔记
- 产品方案：鼓励用户会议中随手记关键词，AI 以关键词为线索生成纪要

**Enter 团队规模**：截止课程开课约 10 人，有很长时间个位数。结论：早期验证阶段保持精简，中后期随业务需要动态增加。

**GA Custom Event 代码**：
```javascript
// 学员提交申请表单时上报
gtag('event', 'submit_credits_application', {
  'course': '所选课程名称',
  'email': '学员邮箱'
});
```

**PostHog 环境变量配置**：
```
VITE_PUBLIC_POSTHOG_KEY=phc_wOpwAhodveBkWU8mimTubdm14S3sJ4DQaYr6fC9nusP
VITE_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
```

**PostHog 初始化代码**：
```javascript
import { PostHogProvider } from 'posthog-js/react'

const options = {
  api_host: import.meta.env.VITE_PUBLIC_POSTHOG_HOST,
  defaults: '2025-11-30',
} as const

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <PostHogProvider apiKey={import.meta.env.VITE_PUBLIC_POSTHOG_KEY} options={options}>
      <App />
    </PostHogProvider>
  </StrictMode>
)
```

**PostHog 关键事件上报**：
```javascript
posthog.capture('submit_credits_application', { course: '课程名', email: '邮箱' })
```

**GA4 接入代码**：
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YQBK61DYF1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-YQBK61DYF1'); // 换成自己的 Measurement ID
</script>
```

**课程下拉选项（后端配置）**：
```
#0 About Chris
#1 大势不可逆，得 Coding 者必胜
#2 从 Website 开始构建一款商业产品
#3 用一个插件来提高你的办公幸福度
#4 与时俱进做出独属你的第一款 AI 应用
#5 掏家底的新时代"自救"宝典
#6 各产品注册和使用指导
```

**品牌升级 Prompt（Gemini → Enter.pro）**：
```
Context: I'm building a credit application form for enter.pro. Style Requirement:
Zero Border Policy: Remove all border classes. Use background color differences (zinc-900 on black background) and subtle box-shadow to define sections.
Navigation: Remove any "Admin" links or entry points from the UI.
Typography: Use a clean Sans-serif (Inter/Geist). Header should be large with high contrast.
Form Inputs: Design inputs as borderless fields with a subtle bg-zinc-900/50. On focus, add a soft outer glow (drop-shadow) using the primary theme color, no solid borders.
Mobile First: Ensure the form stacks perfectly on mobile. Use w-full for buttons and inputs. Add enough vertical spacing between fields.
Button: A high-contrast primary button with a slight gradient and rounded-full corners, matching the "Enter" aesthetic.
```

---

### 📝 避坑指南

- ⚠️ **Supabase 授权必须完成两步**：Organization 授权 + 具体 Project 连接，只做第一步 Agent 无法操作数据库
- ⚠️ **发布前必须在预览版本完整测试**：Publish 后用户立即可访问，未测试的版本不要发布
- ⚠️ **版本必须手动加书签标记**：最新版本 ≠ 正式版本，出问题靠版本回退救场
- ⚠️ **GA 数据 48 小时后才完整**：接入后不要立刻看报表，实时报告可以即时验证是否接入成功
- ⚠️ **PostHog 接入后必须配置授权域名**：否则数据采集会被拦截，在 PostHog 后台填入正式版本链接
- ⚠️ **Course 选项不要写死在前端代码里**：应从后端配置读取，方便后续增减课程不用改代码重新发布
- ⚠️ **移动端适配必须用真机验证**：模拟器不能完全还原真实手机体验，尤其是触摸交互和字体渲染
- ⚠️ **视觉迭代的瓶颈是 Prompt 精度**：遇到 AI 审美卡点，先用 Gemini 等工具生成专业设计 Prompt，再喂给 Enter.pro，效果更可控
- ⚠️ **Admin 入口不应暴露在前端页面**：后台管理入口不要放在用户侧页面，安全隐患

---

### 🛠️ 课后作业 SOP

**初阶（PRD 设计）**：
- 挑战题：找真实痛点，模仿课程格式写需求文档（飞书文档）
- 开放题：设计动态个人主页，含互动模块（留言板/扫码/简历下载统计）
- 复习题：重新梳理 Credits 申请系统需求逻辑，找逻辑漏洞

**进阶（全栈实现）**：
- 将 PRD 通过 Enter.pro 实现为真实网站
- 必须连接 Supabase，数据真实入库
- 生成公网 URL，手机可正常访问
- 提交：公网 URL + Supabase Table Editor 截图

**高阶（运营与体验）**：
- 必须：接入 GA 或 PostHog，配置至少 1 个自定义事件（如 `click_submit`）
- 必须：完成移动端适配，手机截图验证
- 加分：毛玻璃/渐变/大卡片等有设计感 UI；增加新功能（邮件通知伪代码/博客列表）
- 提交：公网 URL + 数据看板截图 + 手机端截图

---

### 🏷️ 行业标签
#VibeCoding #AIcoding #Supabase #全栈开发 #产品设计 #PRD #GoogleAnalytics #PostHog #SEO #移动端适配 #Enter.pro #MVP #零代码开发

---

---
