# Vibe_Coding实践

## 8. [2026-01-20]

## 📘 文章 3


> 文档 ID: `RpoAw0j33ijD6KkSoYZcVcdUnXg`

**来源**: 小白 Vibe Coding 发行全平台&可变现应用指南 | **时间**: 2026-01-20 | **原文链接**: https://mp.weixin.qq.com/s/VcaM3X57...

---

### 📋 核心分析

**战略价值**: 用 Youware（零代码 Vibe Coding 平台）从零构建一个带 AI 后端、全平台 PWA、登录/邀请码系统、Stripe 支付、自定义域名的完整可变现产品的完整操作路径。

**核心逻辑**:

- **产品原型来自真实需求验证**：马伯庸和 Karpathy 都在用 Append-only 纯事实日记法，单文件、无分类、低摩擦，一年记录量不超过几万字，完全在主流模型上下文窗口内，天然适合 AI 全量分析。
- **模型选型策略**：构建核心逻辑阶段用 Claude Sonnet（代号 Sonnet4.5），UI 样式打磨阶段切换为 Gemini 3 Pro，两个模型各司其职，不要混用。
- **数据库设计要先于 Prompt**：日记应用需建两张表——`Diary_entries`（原文）和 `Diary_tags`（原文+标签），导出时读 entries 表，展示时读 tags 表，逻辑清晰才能让模型正确生成。
- **API Key 安全问题通过 YouBase Secrets 解决**：以前 Vibe Coding 无后端只能把 API Key 暴露在前端，YouBase 的 Secrets 模块专门存储 API Key，模型完成集成后会主动索要 Key 并自动写入 Secrets，不需要手动操作。
- **AI 标签能力接入方式**：告诉 Youware「用户创建日记后调用 openrouter 的 XX 模型分析内容并创建日期、地点、人物等标签」，模型会自动查询 openrouter 文档完成集成，也可以手动粘贴文档给它。
- **Coview 解决「不会描述 UI 位置」的核心痛点**：点击输入框右下角圆点录制按钮，边说话边用鼠标指向需要修改的位置，结束后 Youware 自动将视频+音频内容转化为专业术语 Prompt 再交给模型执行，彻底消除自然语言描述不精准的问题。
- **UI 一致性方案**：找一张与目标产品风格相似的截图或设计稿，发给 Youware 并说「分析这个设计稿，提取其中的设计元素，变成设计 Token 以及组件设计，为平台上的所有设计应用修改，后续修改也基于这套组件和设计样式」，一次性建立全局设计系统。
- **登录+邀请码系统一句话生成**：告诉 Youware「为项目添加登录注册系统，创建邀请码系统，邀请码单独存在一个数据表里，没有核验过邀请码的禁止登录」，系统自动生成 `invitation_codes` 表，可在 YouBase 页面直接管理和复制邀请码。
- **谷歌登录集成路径**：YouBase → Users → 右上角 Auth Settings → 选择 Google 登录 → 按指引视频完成 OAuth 配置。
- **PWA 全平台分发一句话搞定**：告诉 Youware「将这个网页打包成 PWA 应用，并且做好移动端适配」，用户即可将网站安装到 iOS/Android/Mac/Windows 桌面，独立图标、独立窗口、支持离线，无需上架应用商店。
- **Stripe 支付集成**：先设计付费体系并让 Youware 生成合规页面（隐私协议等），再说「帮我集成 Stripe 的支付服务」，集成完毕后填写 Stripe Token，自动存入 Secrets。
- **自定义域名绑定**：发布时点击右上角 Update → 弹窗 Domain 位置点击箭头 → 新窗口点击「Add Domain」→ 输入域名 → 复制生成的 DNS 参数 → 去域名服务商添加对应记录，不会操作可直接在 Chat 模式问 Youware。

---

### 🎯 关键洞察

**为什么 Append-only 日记适合 AI 时代**：
- 只记事实、不分类 → 摩擦极低 → 坚持率高
- 单文件结构 → 一年记录量 < 几万字 → 低于 GPT-4/Claude 等主流模型上下文上限
- 可以直接把整年日记丢给任意模型做全量分析，相当于「只属于你的 ChatGPT 记忆」，且不依赖任何特定平台

**为什么 YouBase 是 Vibe Coding 的关键基建**：
- 解决了「无后端 → API Key 只能放前端 → 安全漏洞」这个 Vibe Coding 最大的工程问题
- 内置用户系统（注册/登录/Google OAuth）、数据库、Secrets 管理，让非技术用户也能构建真正可分发的产品
- 自动修复不扣积分，降低试错成本

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/操作 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 项目创建 | 侧边栏 Create → 模式切换为 Code | 进入代码生成模式 | 默认模式不是 Code，需手动切换 |
| 模型选择 | 核心逻辑用 Sonnet4.5，UI 优化用 Gemini 3 Pro | 各阶段最优输出 | 不要全程用同一个模型 |
| YouBase 开通 | 描述需求后模型会提示点击按钮开通 | 自动创建数据库和表 | 需主动触发，不会自动开通 |
| 数据库查看 | 预览区上方云朵图标 | 查看 Diary_entries / Diary_tags 等表 | — |
| API Key 存储 | YouBase → Secrets | Key 安全存储，不暴露前端 | 模型集成完会主动索要 Key |
| AI 标签接入 | 指定 openrouter 模型，描述标签类型（日期/地点/人物） | 保存时自动打标签 | 可附上 openrouter 文档给模型参考 |
| Coview | 输入框右下角圆点按钮 → 录屏+语音 → 结束 | 模型自动理解 UI 修改需求 | 说话时鼠标要指向目标位置 |
| 设计系统 | 发截图 + 固定 Prompt（见核心逻辑第7点） | 全局 UI 风格统一 | 一次性建立，后续修改自动沿用 |
| 登录/邀请码 | 一句话 Prompt（见核心逻辑第8点） | 生成登录页+邀请码表+核验逻辑 | 邀请码在 YouBase invitation_codes 表管理 |
| Google 登录 | YouBase → Users → Auth Settings → Google | OAuth 登录 | 需按指引视频完成 Google Cloud 配置 |
| PWA 打包 | 告诉 Youware「打包成 PWA 并做移动端适配」 | iOS/Android/桌面端均可安装 | 无需上架应用商店 |
| Stripe 支付 | 先做合规页面，再说「集成 Stripe」，填写 Token | 支付功能上线 | 合规页面（隐私协议等）必须先做好 |
| 自定义域名 | Update → Domain → Add Domain → 复制 DNS 参数到域名服务商 | 独立域名访问 | 不会操作可直接问 Youware Chat |

---

### 🛠️ 操作流程

1. **准备阶段**
   - 确定产品核心链路（以日记为例：输入 → 存原文 → AI 打标签 → 检索/导出）
   - 准备好 openrouter API Key 和 Stripe Token
   - 找一张目标风格的设计截图备用

2. **核心执行**
   - 侧边栏 Create → 切换 Code 模式 → 选 Sonnet4.5
   - 描述核心需求，明确数据库表结构（entries + tags 两张表）
   - 点击开通 YouBase，确认数据库自动创建
   - 添加 AI 标签能力：指定 openrouter 模型 + 标签类型，填写 API Key 到 Secrets
   - 添加登录+邀请码系统（一句话 Prompt）
   - 可选：开启 Google OAuth（Auth Settings）

3. **UI 打磨阶段**
   - 切换模型为 Gemini 3 Pro
   - 发设计截图 + 设计系统 Prompt，建立全局 Token
   - 用 Coview 录屏指点具体 UI 修改位置

4. **分发与变现**
   - 告诉 Youware 打包 PWA + 移动端适配
   - 做合规页面 → 集成 Stripe → 填写 Token
   - 绑定自定义域名（Add Domain → 配置 DNS）
   - 在 YouBase Users 页面管理用户和邀请码

5. **验证**
   - 手机浏览器访问，测试「添加到桌面」是否生效
   - 检查 Secrets 中 API Key 是否正确存储
   - 在 invitation_codes 表复制邀请码，测试注册流程

---

### 💡 具体案例/数据

- 产品名：Vibe Diary，线上地址：diary.guizang.ai
- 功能清单：AI 标签（时间/地点/人物）、Todo 模式（AI 自动判断是否待办）、莫兰迪色系每日不同颜色卡片、关键字+日期+标签三维检索、Markdown 单文件导出、邀请码注册系统
- 已发放邀请码给部分朋友，实际留存率超预期（「粘性这么高」）
- 设计风格：藏师傅设计系统，莫兰迪色系

---

### 📝 避坑指南

- ⚠️ API Key 绝对不能放前端，必须通过 YouBase Secrets 存储，否则会泄露
- ⚠️ 数据库表结构要在第一次 Prompt 里说清楚，后期改表结构成本很高
- ⚠️ Stripe 集成前必须先完成合规页面（隐私协议、服务条款），否则 Stripe 审核会拒绝
- ⚠️ Coview 录制时鼠标必须指向目标位置，只说话不指位置效果会打折
- ⚠️ 设计系统 Prompt 要在 UI 大改之前一次性建立，后期补做会有样式冲突
- ⚠️ PWA 离线能力依赖 Service Worker，打包后需实际在手机上测试「断网是否可用」

---

### 🏷️ 行业标签

#VibeCoding #Youware #YouBase #PWA #NoCode #AIProduct #Stripe支付 #全平台分发 #AI日记 #Coview

---

---
