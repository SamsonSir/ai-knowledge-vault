# Agent与技能系统

## 📙 文章 4

> 文档 ID: `UXGxwQ2fuiBFJKkm1GAcVMkwn7b`

 > **来源**: Anthropic Claude Code 团队工程师 Thariq Shihipar 实战经验总结  
> **发布时间**: 2026年3月18日  
> **原文链接**: https://mp.weixin.qq.com/s/PEisnE_C... / https://x.com/trq212/status/2033949937936085378

---

### 📋 核心分析

**战略价值**: 来自 Anthropic 内部的 Skills 实战方法论，系统梳理了 9 大 Skill 类型与 10+ 编写技巧，为团队规模化使用 Claude Code 提供可落地的分类框架与最佳实践。

**核心逻辑**:
- Skills ≠ Markdown 文件，而是包含脚本、资源、配置的完整文件夹结构，支持动态钩子与渐进式上下文披露
- 高质量 Skills 的关键在于"打破 Claude 默认思维模式"，而非重复常识
- 内部实践验证：最有用的 Skills 均从简单版本迭代演化而来，核心在于持续积累"踩坑点"
- 规模化分发需平衡"提交到仓库"与"插件市场"两种模式，避免上下文膨胀

---

### 🎯 关键洞察

**1. 类型化思维降低决策成本**

Anthropic 内部数百个活跃 Skills 可归为 9 类：库/API 参考、产品验证、数据获取与分析、业务流程自动化、代码脚手架、代码质量审查、CI/CD 部署、运维手册、基础设施运维。清晰的类型归属是 Skill 可用性的首要指标——横跨多类的 Skills 往往让人困惑。

**2. "踩坑点"章节是信息密度最高的部分**

任何 Skill 都应包含专门的 gotchas/footguns 章节，记录 Claude 实际使用中的失败模式。这与传统文档相反：不写"应该怎么做"，而写" Claude 容易在这里犯错"。该章节应随实际使用持续迭代。

**3. 渐进式披露解决上下文窗口约束**

利用文件系统结构实现 Context Engineering：将详细 API 签名拆至 `references/api.md`，模板放 `assets/`，数据获取脚本放 `lib/`。告知 Claude 文件存在即可，无需一次性加载全部内容。这是 2025 年 LLM 应用架构的核心技术之一。

**4. Description 字段的语义陷阱**

Description 不是功能摘要，而是触发条件。Claude 通过扫描所有 Skills 的 description 判断"这个请求该用哪个 Skill"。有效描述应写成 if-then 形式（如"当你需要调试生产环境服务中断时"），而非"这是一个调试工具"。

**5. 按需钩子实现安全与效率的平衡**

通过 `On Demand Hooks` 注册会话级行为：如 `/careful` 仅在操作生产环境时激活危险命令拦截，`/freeze` 仅在调试时限制编辑范围。避免全局开启导致的摩擦，同时保留关键场景的保护能力。

---

### 📦 可执行模块

| 模块 | 内容描述 | 适用场景 |
|------|---------|---------|
| **Skill 类型自检清单** | 对照 9 大类型检查团队覆盖缺口 | 团队 Skills 体系规划阶段 |
| **渐进式披露模板** | 标准文件夹结构：`SKILL.md` + `references/` + `assets/` + `scripts/` | 新建任何 Skill 时 |
| **踩坑点迭代工作流** | 记录 Claude 失败案例 → 分类 → 更新 Skill → 验证修复 | Skill 持续优化 |
| **description 改写公式** | [触发场景] + [具体任务] + [预期输出] | 所有 Skill 元数据编写 |
| **数据持久化方案** | 使用 `${CLAUDE_PLUGIN_DATA}` 存储跨版本数据 | 需要记忆功能的 Skills |
| **内部市场治理机制** | 沙盒文件夹 → Slack 推荐 → 关注度验证 → PR 转正 | 规模化 Skills 分发 |

---

### 🔗 相关资源

- **原文链接**: https://x.com/trq212/status/2033949937936085378
- **官方文档**: https://code.claude.com/docs/en/skills
- **Skill Creator 工具**: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
- **Agent Skills 课程**: https://anthropic.skilljar.com/introduction-to-agent-skills
- **前端设计 Skill 示例**: https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
- **插件市场文档**: https://code.claude.com/docs/en/plugin-marketplaces
- **Skill 使用统计钩子示例**: https://gist.github.com/ThariqS/24defad423d701746e23dc19aace4de5

---
