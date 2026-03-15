# AI编程与开发工具

## 42. [2026-03-01]

## 📓 文章 6


> 文档 ID: `AMi1wIjVriBXDzkOPhdcN1fmnOf`

**来源**: 2万字复盘：我们用 AI 编程做出商业级视频 Agent 平台 | **时间**: 2026-03 | **原文链接**: 无公开链接

---

### 📋 核心分析

**战略价值**: 一个 AI 视频 Agent 平台从 v0.1 到 v4.0.6 的完整工程复盘，涵盖技术架构决策、AI 编程工具选型、规范体系建设、创业认知升级的全链路可复用方法论。

**核心逻辑**:

- **技术栈选型**：前端 Next.js 15.1 + React 19 + TypeScript 5.8 + Tailwind CSS；后端 Vercel Serverless + Next.js App Router（41 个 API 端点）；数据层 Supabase PostgreSQL + Cloudflare R2；AI 模型集成 Gemini 3.1 Pro/Flash Image、Sora 2、Vidu、火山引擎 SeeDream/SeeDance、即梦，共 6 个模型
- **规模真实数据**：22+ 独立服务文件、97 个方法封装在单一 `dataService.ts`、28 个 Function Calling 工具支持并行执行、22 个 Custom Hooks（Chat 相关 12 个）、30+ 版本迭代、docs/ 目录 30+ 份架构文档
- **Skills 系统驯化 AI 审美**：在 `.agent/skills/frontend-design/SKILL.md`（317 行）中结构化定义设计规范（色彩体系、字体、间距、动效、组件语言），AI 读取后输出的 UI 严格遵循 Premium Glass 规范（高斯模糊 + 极细内描边 + 克制 hover 动效），彻底消除"AI 味"千篇一律问题
- **Agent 手动确认哲学**：用户发指令 → Agent 解析意图 → 展示执行计划 → 用户确认 → 才执行。消耗积分操作（如批量生成视频）强制弹窗预估确认，解决操作门槛高、Agent 崩溃影响大、烧光积分三个问题
- **模型无关架构**：统一 `sora_tasks` 表用 `provider` 字段区分 `sora/vidu/jimeng/volcano/runway`，统一任务状态管理（queued → processing → completed），统一 R2 持久化管道，具体模型差异封装在独立 Service 文件。新增模型只需新增一个 Service，前端和任务管理逻辑完全复用
- **双模型工作流**：Claude Opus/Sonnet via Antigravity 负责方案设计、后端核心逻辑、复杂 Bug 诊断、多文件重构；Gemini 最新模型 via Antigravity 负责前端网页设计优化、UI/UX 细节、CSS/Tailwind 美化、组件交互优化
- **"收菜式"开发取代 Vibe Coding**：阶段一人类主导深度设计（架构蓝图 + 功能细节文档 + 任务拆解）→ 阶段二 AI 主导自动实现（人类不盯着，去做其他事）→ 阶段三人类主导验收测试（第二天"收菜"+ 全量回归）
- **任务拆解粒度标准**：每个任务必须包含明确的输入、输出、约束，参考现有代码风格，细到"任何合格程序员都能无歧义执行"的粒度（见下方操作流程中的真实案例）
- **文档即 AI 操作系统**：README.md（700+ 行）+ AGENTS.md（750 行）+ CLAUDE.md（1600+ 行）+ docs/ 30+ 文件，文档越详细准确，AI 产出越像项目原生代码
- **3 次失败停止原则**：连续 3 次尝试失败后必须停止，记录失败原因，研究 2-3 个替代方案，质疑根本假设——是否用了错误的抽象层级

---

### 🎯 关键洞察

**补丁地狱的根因分析**（2026 年 1 月，v3.8.x 密集迭代期）：

| 版本 | 问题 | 根因 | 解决方案 |
|------|------|------|---------|
| v3.8.2 | Vercel 413 错误，Grid 图片上传失败 | 4.5MB payload 限制 | 实现 R2 预签名直传 |
| v3.8.5 | 生产环境 FUNCTION_INVOCATION_TIMEOUT | 即梦 API 同步阻塞 | 改为客户端轮询 |
| v3.9.0 | 拖拽分镜图片刷新后丢失 | 无即时持久化机制 | "所见即所得"即时持久化重构 |
| v3.9.3 | Vidu/Sora 参考图状态互相污染 | 单体 ChatPanel 状态耦合 | 彻底重构为隔离 Hook 架构 |
| v3.9.6 | Gemini 参考图 VPN 下传不过去 | 直接传 blob URL | URL 优先 + 自动降级策略 |

90% 的坑来自前期架构设计不够深入。

**ChatPanel 重构前后对比**：

```
// 重构前：ChatPanel.tsx 几千行全耦合

// 重构后：hooks/chat/
├── useChatGeneration.ts          // 生成请求调度
├── useChatHistory.ts             // 历史记录管理
├── useChatScroll.ts              // 滚动行为
├── useChatActions.ts             // 操作回调
├── useChatModals.ts              // 弹窗状态
├── useChatReferenceInteractions.ts  // 拖拽/上传交互
├── useApplyVideoToShot.ts        // 视频应用逻辑
├── useAutoReference.ts           // @提及自动检测
├── useVideoModeReferences.ts     // 视频模式参考图
├── useStartEndFrames.ts          // 首尾帧管理
├── useVideoReferences.ts         // 各模式独立参考图
└── useReferenceCallbacks.ts      // 参考图操作回调
```

**临时 URL 持久化必须是底层基础设施**：`blob:` 和 `data:` URL 刷新即失效，早期直接存入数据库导致大量"图片丢失"bug。正确做法：

```typescript
// 任何 local URL 在赋值给数据模型之前，自动转为 R2 链接
const persistentUrl = await ensurePersistedImageUrl({ 
  url: localBlobUrl, 
  ...folderContext 
});
updateShot(shotId, { referenceImage: persistentUrl });
```

**架构收敛关键动作**（2026 年 2 月，v4.0.x）：
1. ChatPanel Hook 大重构（v4.0.0）：单体组件拆成 12 个独立 Hook
2. Cron 异步架构（v4.0.1）：Sora 状态检查和 R2 上传解耦为两个独立定时任务
3. 事务原子性（v4.0.1）：核心删除操作迁移到 PostgreSQL 存储过程，零数据不一致
4. Hybrid Auth（v4.0.4）：解决登录状态水合延迟问题
5. Premium Glass 设计体系（v4.0.4-v4.0.6）：确立统一 UI 规范

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Skills 系统 | `.agent/skills/frontend-design/SKILL.md`（317 行），含 DO/DON'T 规范清单 | AI 输出 UI 有设计感，无"AI 味" | 需结合 ChatGPT Thinking 深度分析竞品截图后提炼，不能凭空写 |
| 统一视频任务表 | `sora_tasks` 表增加 `provider: 'sora' \| 'vidu' \| 'jimeng' \| 'volcano' \| 'runway'` | 新增模型只需新增 Service 文件 | 早期为每个模型单独建表是错误做法 |
| 三级聊天历史 | Project 级（Planning）/ Scene 级（Grid 生成）/ Shot 级（Pro 模式） | 历史记录不混淆 | 直接修改 `project.chatHistory` 已迁移至 `chat_messages` 表，严禁旧方式 |
| 积分二次确认 | Agent 预检意图 → 积分预估 → UI 弹窗确认 → 同意后执行 | 防止一句话烧光积分 | 需处理模型抽风跳过 ToolCall 直接回复文本的情况，中间件自动检测阻止虚假执行 |
| R2 预签名直传 | 绕过 Vercel 4.5MB payload 限制 | 大图上传不报 413 | 必须在 v0.1 阶段就规划，否则后期改造成本极高 |
| 客户端轮询 | 替代同步阻塞 API（如即梦） | 避免 Serverless 超时 | 同步阻塞 API 在 Vercel 上必然触发 FUNCTION_INVOCATION_TIMEOUT |
| Antigravity Tools | 接入 Claude Opus/Sonnet + Gemini 最新模型 | 双模型分工，效率倍增 | 闲鱼购买 Google Pro 年会员

---

---
