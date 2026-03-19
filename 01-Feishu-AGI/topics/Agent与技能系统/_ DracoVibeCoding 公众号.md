# Agent与技能系统

## 📒 文章 7

> 文档 ID: `QoLGw3Gj0iHS3kk8PWjcx4QZnxc`

 > **来源**: DracoVibeCoding 公众号  
> **发布时间**: 2026年3月17日  
> **原文链接**: https://mp.weixin.qq.com/s/rFecRxZ1...

---

### 📋 核心分析

**战略价值**: 厘清 OpenClaw 多 Agent 架构中 Skill 的分层发现机制与共享边界，为大规模 Multi-Agent 协作提供可维护的技能管理工程范式。

**核心逻辑**:
- Tool 是"能力层"（能不能做），Skill 是"方法层"（怎么做）
- Skill 采用三层发现机制：全局安装层 → 共享层 → Workspace 私有层
- Sub-Agent 并非 Main Agent 的完全克隆，而是按目标 Agent 配置启动的独立会话实例
- Skill 共享遵循"显式公共层优先，私有层不默认继承"原则

---

### 🎯 关键洞察

**Skill 与 Tool 的本质分离**
Tool 是原子操作能力（read/write/exec/browser），Skill 是编排这些能力的"作战手册"（SKILL.md + references/ + scripts/）。Agent 看得见 Skill 不等于能执行，还需校验 Tool 权限、文件路径可达性、技能过滤规则三重约束。

**三层发现机制的工程含义**
| 层级 | 典型路径 | 共享范围 | 适用场景 |
|:---|:---|:---|:---|
| 全局安装层 | `.../node_modules/openclaw/skills` | 全系统 | 官方基础能力 |
| 共享层 | `~/.openclaw/skills`, `~/.agents/skills` | 跨 Agent | 团队公共工作流 |
| 私有层 | `~/.openclaw/workspace/skills`, `~/.openclaw/agency-agents/<id>/skills` | 单 Agent | 角色定制流程 |

**Sub-Agent 的继承边界**
Sub-Agent 继承的是目标 Agent 的身份配置、workspace、tools policy、model 设置，而非 Main Agent 的 Skill 集合。Skill 可见性取决于运行时发现范围，而非父子关系。

**同名 Skill 的优先级陷阱**
系统未公开声明层间覆盖优先级，实践中需主动标注 Skill 来源（官方内置/本机共享/Agent 私有/本地覆盖），避免"修改不生效"的排障成本。

---

### 📦 可执行模块

| 模块 | 内容描述 | 适用场景 |
|:---|:---|:---|
| **Skill 分层放置决策** | 公共能力 → `~/.openclaw/skills`；角色专用 → `~/.openclaw/agency-agents/<id>/skills` | 初始化 Multi-Agent 目录结构 |
| **Skill 可发现性验证** | 不依赖目录推断，抽样实测 Sub-Agent 运行时能否读取目标 Skill | 调试 Skill 共享异常 |
| **Skill 来源标注规范** | 在 SKILL.md 头部声明来源层级与覆盖关系 | 长期维护 Skill 版本一致性 |

---

### 🔗 相关资源

- **原文链接**: https://mp.weixin.qq.com/s/rFecRxZ1...
- **前置阅读**: 
  - 《从底层机制一文讲透：OpenClaw🦞如何运行多Agents》
  - 《我在企微里养了130个AI员工：OpenClaw+The Agency实战全记录》
- **相关工具**: OpenClaw, The Agency (Multi-Agent 编排框架)

---
