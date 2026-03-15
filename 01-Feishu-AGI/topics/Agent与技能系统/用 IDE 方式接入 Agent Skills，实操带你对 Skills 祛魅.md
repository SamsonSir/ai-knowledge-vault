# Agent与技能系统

## 10. [2026-01-15]

## 📔 文章 5


> 文档 ID: `RL2ewVyePioyiLkvVyOcKqeUnpc`

**来源**: 用 IDE 方式接入 Agent Skills，实操带你对 Skills 祛魅 | **时间**: 2026-01-15 | **原文链接**: https://mp.weixin.qq.com/s/GUtYULF6...

---

### 📋 核心分析

**战略价值**: 用 Trae IDE 可视化接入 Anthropic 官方 Agent Skills + OpenSkills 工具链，完整演示从环境搭建、技能调用、自建技能到多技能组合的全流程，彻底拆解其"按需加载"底层机制。

**核心逻辑**:
- Agent Skills 本质是三文件标准：`SKILL.md`（必须）+ 实现代码（可选）+ 依赖文件（可选），不是黑科技
- OpenSkills 是配套 CLI 管理工具，两者关系：Agent Skills = 书，OpenSkills = 图书管理员，AGENTS.md = 目录，AI = 读者
- 核心机制是"渐进式披露"：Stage 1 只读 AGENTS.md（每技能约 50 tokens），Stage 2 用户触发后才调用 `openskills read skill_name` 注入完整 SKILL.md（数千 tokens），实现 100 个技能不撑爆 Context Window
- AGENTS.md 放在项目根目录后，Trae 3.5.20+ 可在设置中配置为"上下文文件"自动加载；旧版本也可能通过约定俗成机制生效
- AI 不一定真正调用了技能，可能用通用能力模拟执行——需主动追问确认，看到 AI 发起 `openskills read` Tool Call 才算真调用
- `skill-creator` 是官方提供的"创建技能的技能"，SKILL.md 的 `description` 字段是触发机制核心，必须写清楚功能、触发场景、使用条件
- 技能创建后必须执行 `openskills sync` 同步到 AGENTS.md，否则 AI 不知道该技能存在
- 多技能组合时，在 prompt 中明确指定技能名称（如"必须至少使用 content-refiner 和 docx 两个技能"），AI 会依次读取两份 SKILL.md 并协同执行
- 技能质量需迭代：一次生成不代表好用，需在真实任务中测试，根据反馈修改 SKILL.md 的 SOP 描述
- SkillsMP 技能市场（https://skillsmp.com/zh）已有 6 万+ 技能，可搜索现成技能直接用或二次改造

---

### 🎯 关键洞察

**为什么"渐进式披露"是核心设计哲学**：
传统做法把所有技能文档一次性塞入 Context → 爆炸。OpenSkills 的两阶段策略：先给 50 tokens 的摘要目录，只有 AI 判断需要某技能时才注入完整文档。这使得安装 100 个技能的 token 消耗等同于只安装 1 个，且 AI 执行时专注度更高（上下文无噪音）。

**为什么 description 字段决定技能能否被触发**：
AI 在 Stage 1 只能看到 `name` 和 `description`，这是唯一的匹配依据。description 写得模糊 → AI 不知道何时调用 → 技能形同虚设。官方建议格式：`"Use when Claude needs to... for: (1)... (2)..."`，把所有触发场景都写进 description，正文只写操作指南。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 环境检查 | `node --version; npm --version` | 确认 Node/npm 可用 | OpenSkills 依赖 Node 环境，缺失需先安装 |
| 安装 OpenSkills | `npm install -g openskills` | 全局可用 openskills CLI | 需要 npm 全局权限 |
| 创建技能目录 | `mkdir ".claude/skills"` | 标准技能存放路径 | 官方约定路径，不要改 |
| 生成索引 | `openskills sync` | 生成/更新 AGENTS.md | 每次新增技能后必须重新执行；交互时按 `a` 全选，回车确认 |
| 下载官方示例 | `git clone https://github.com/anthropics/skills.git` 或直接下载 `https://github.com/anthropics/skills/archive/refs/heads/main.zip` | 获取官方示例技能库 | 下载后将所有示例复制到 `.claude/skills/` 目录下 |
| SKILL.md 结构 | YAML frontmatter（name + description 必须）+ Markdown 正文 | AI 识别并调用技能 | 正文保持 500 行以内；接近上限时拆分到 references/ |
| Trae 上下文配置 | 设置中将 AGENTS.md 配置为"上下文文件" | 每次对话自动加载技能目录 | Trae 3.5.20+ 支持；技能不生效优先检查此项 |
| 技能文件结构 | `skill-name/SKILL.md`（必须）、`scripts/`、`references/`、`assets/` | 标准化技能包 | 禁止包含 README.md、安装指南、变更日志 |
| 打包技能 | `python package_skill.py <path/to/skill-folder>` | 生成 .skill 文件（实为 zip） | 自动验证 YAML 格式、命名规范、描述完整性；验证失败报错退出 |
| 初始化新技能 | `python init_skill.py <skill-name> --path <output-directory>` | 生成标准目录结构和模板 | 技能已存在时跳过，直接迭代 |

---

### 🛠️ 操作流程

**1. 准备阶段：搭建环境（约 20 分钟）**

```bash
# 检查环境
node --version; npm --version

# 安装 OpenSkills
npm install -g openskills

# 创建技能目录
mkdir ".claude/skills"

# 初始化空索引（理解 AGENTS.md 生成机制用）
openskills sync

# 下载官方示例并复制到技能目录
# 解压后将所有示例文件夹复制到 .claude/skills/

# 同步官方示例到索引
openskills sync
# 交互提示：按 a 全选，回车确认
```

Trae 设置：将 AGENTS.md 配置为上下文文件（Trae 3.5.20+）。

**2. 核心执行：调用技能**

在对话框直接用自然语言描述任务，明确指定技能名：
```
使用技能 pdf 将 `/path/to/AGENTS.md` 输出为 pdf 文档
```

验证是否真正调用技能（追问 AI）：
```
如何确定你刚才是按 pdf 技能执行的，还是用大模型通用能力执行的？
```
看到 AI 发起 `openskills read pdf` Tool Call = 真调用。

**3. 创建自定义技能（用 skill-creator）**

```
请用 skill-creator 创建一个技能，用于[描述你的需求]。
要求：[具体约束，如输入格式、输出格式、不修改原稿等]
```

如果 AI 没调用 skill-creator，明确追问：
```
我要确认下，你刚才创建技能是用 skill-creator 创建的吗？还是用大模型通用能力创建的？
```

创建完成后同步索引：
```bash
openskills sync
# 按 a 全选，回车确认
```

**4. 多技能组合**

在 prompt 中明确指定多个技能名并要求强制使用：
```
用 content-refiner 技能对 `/path/to/file.docx` 进行优化，
其中原稿是 word 文件，可以使用 docx 技能进行相关处理操作。
要求必须至少使用这两个技能。
```

观察 AI 是否依次读取两份 SKILL.md（出现两次 `openskills read` = 正确执行）。

**5. 验证与优化**

- 在真实任务中测试技能效果
- 发现问题 → 修改 SKILL.md 的 SOP 描述或 description 字段
- 增加 references/ 中的模板示例
- 重新执行 `openskills sync` 更新索引

---

### 💡 具体案例/数据

**案例 1：pdf 技能调用**
- 任务：将 AGENTS.md 转为 PDF
- 结果：AI 调用了 pdf 技能，但 pdf 技能不支持 md 格式，AI 参考技能中的开发手册，额外调用通用编码能力生成了 `md_to_pdf.py` 脚本补全，最终自动交付
- 说明：技能能力有限时，AI 会混合使用技能 + 通用能力兜底

**案例 2：自建 content-refiner 技能**
- 需求：文章内容梳理、校对、排版，优化逻辑，适配社区/公众号/视频口播稿，支持 word 和 md 输入，不修改原稿生成新稿
- 结果：用 skill-creator 生成了只含 SKILL.md 的技能包（纯 SOP 流程，无脚本）
- 注意：第一次 AI 用通用能力创建，需明确要求"请用 skill-creator 创建"才触发技能

**案例 3：content-refiner + docx 双技能组合**
- 任务：优化 word 文档并输出优化后的 word 文件
- 执行：AI 依次读取 content-refiner/SKILL.md 和 docx/SKILL.md，协同执行
- 验证：观察到 AI 发起两次 `openskills read` Tool Call

**skill-creator 的 description 字段参考写法**：
```
Guide for creating effective Claude skills that extend capabilities with specialized 
knowledge, workflows, and tool integrations. Use when users want to: (1) Create a new 
skill from scratch, (2) Improve or refactor an existing skill, (3) Package domain 
expertise into reusable form, (4) Understand skill design principles and best practices, 
(5) Initialize, validate, or package skills using provided scripts.
```

---

### 📝 SKILL.md 编写 SOP（6步）

**Step 1：通过具体示例理解技能**
- 收集 3-5 个具体使用场景
- 确认功能范围
- 使用模式已清晰时可跳过

**Step 2：规划可复用资源**
- `scripts/`：需要重复执行的代码
- `references/`：参考文档、API 规范、模式
- `assets/`：模板、图标等输出文件

**Step 3：初始化技能目录**
```bash
python init_skill.py <skill-name> --path <output-directory>
```

**Step 4：编写 SKILL.md**
- YAML frontmatter：`name`（必须）+ `description`（必须，触发机制核心）
- 正文：祈使句/不定式，保持 500 行以内，只写操作指南，详细内容放 references/
- 禁止包含：README.md、安装指南、变更日志

**Step 5：打包验证**
```bash
python package_skill.py <path/to/skill-folder>
```
自动验证：YAML 格式、必需字段、命名规范、目录结构、描述完整性、资源引用

**Step 6：迭代优化**
- 真实任务中测试 → 发现低效点 → 修改 SKILL.md → 重新测试

---

### 📦 三种技术对比

| 维度 | API | MCP | Agent Skills |
|------|-----|-----|-------------|
| 形象比喻 | 外卖服务 | 连锁餐厅标准 | 家里的菜谱本 |
| 数据位置 | 远程服务器 | 远程/本地均可 | 本地文件 |
| 网络依赖 | 必须联网 | 视实现而定 | 无需联网 |
| 适用场景 | 实时数据（天气/股票/新闻）、云端计算 | 跨工具复用、标准化协议通信、可复用服务生态 | 本地文件处理（PDF/Excel/图片）、快速原型、个人定制 |
| 冲突关系 | 可共存 | 可共存 | 可共存 |

---

### 📝 避坑指南

- ⚠️ 技能不生效，优先检查 Trae 设置中是否启用了 AGENTS.md 作为上下文文件
- ⚠️ 每次新增或修改技能后必须重新执行 `openskills sync`，否则 AGENTS.md 不更新，AI 看不到新技能
- ⚠️ AI 可能用通用能力模拟执行而非真正调用技能，需主动追问确认，或观察是否出现 `openskills read` Tool Call
- ⚠️ description 字段写得模糊是技能不被触发的最常见原因，必须包含具体触发场景和关键词
- ⚠️ SKILL.md 超过 500 行时需拆分，详细内容移入 references/ 目录，避免单次注入 token 过多
- ⚠️ 避免深层嵌套引用，references 保持一层深度
- ⚠️ 所有脚本必须实际运行测试，不能只写不验证
- ⚠️ Trae 版本较旧或项目中有其他提示词规则时，可能干扰技能调用，需在 prompt 中明确指定技能名

---

### 🏷️ 行业标签
#AgentSkills #OpenSkills #Claude #Trae #IDE #MCP #AI工具链 #提示词工程 #本地AI #技能市场

---

---
