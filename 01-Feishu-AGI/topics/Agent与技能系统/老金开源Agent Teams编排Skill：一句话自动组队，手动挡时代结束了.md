# Agent与技能系统

## 60. [2026-02-14]

## 📓 文章 6


> 文档 ID: `ZI2UwBttWiZTASkKDYycbfTjn1b`

**来源**: 老金开源Agent Teams编排Skill：一句话自动组队，手动挡时代结束了 | **时间**: 2026-02-14 | **原文链接**: https://mp.weixin.qq.com/s/mZDH7VFs...

---

### 📋 核心分析

**战略价值**: 将Claude Code多Agent编排逻辑封装成216行的`agent-teams-playbook` Skill，实现从"手动拼提示词组队"到"一句话自动判断场景、组队、执行、质检、交付"的全流程自动化。

**核心逻辑**:

- **角色定位是"技术联合创始人"而非"任务分配器"**：Skill第一行定义为`Technical Co-Founder级别的Agent Teams协调器`，具备质疑需求、界定范围、选择策略、把控质量、交付移交5项能力，而非机械分配任务。
- **内置5场景决策树，自动判断不需要人工选择**：简单任务(1-2步)→提示增强；中等任务有现成Skill→Skill复用；中等任务无Skill→计划+评审（默认最常用）；复杂任务需分工→Lead-Member；超复杂任务→复合编排。
- **模型按任务复杂度自动分配以控制成本**：haiku处理简单任务（格式化、文件搜索）；sonnet处理常规编码；opus处理需要深度思考的架构设计。同等产出，用对模型可显著降低token消耗。
- **5阶段工作流全自动驱动，人工只在阶段1确认一次**：Discovery（任务分析+范围确认）→团队组建→并行执行→质量把关&产品打磨→结果交付&部署移交。
- **质量把关有明确标准和打回机制**：不只检查"能不能跑"，还检查边界处理（异常覆盖）、专业度（命名规范、错误提示）、完整性（文档/配置/示例）。最多打回2轮，2轮不过通知人工介入。
- **Agent数量硬性上限5个**：Agent多了沟通成本指数级增长，这是写进代码的底线之一。
- **Subagent vs Agent Team有明确选择标准**：Subagent是单向汇报（Agent→协调器），任务间无依赖时用，90%场景够用；Agent Team是双向通信（Agent↔Agent），任务间需互相协调时才用，成本更高（每条消息消耗token）。
- **内置Skill回退链，依赖不可用时自动降级不报错**：find-skills可用→搜索匹配Skill→找到则调用；找不到→回退本地Skill→本地也没有→通用Agent。planning-with-files不可用→跳过生成文件步骤。
- **7条设计底线全部写进代码**：①先澄清目标再组队；②队伍≤5人；③关键节点必须有质量闸门；④不默认任何工具可用；⑤不做不切实际的成本承诺；⑥遇问题给选项不替用户决定；⑦危险操作（大规模变更/删除）必须用户确认。
- **"后续建议"机制防止需求遗漏**：阶段1被砍掉的"add-later"内容，在阶段5交付时会列出来提醒下一步可以做什么。

---

### 🎯 关键洞察

**为什么是"并行外脑+汇总压缩"而不是"单脑扩容"**：
每个teammate是独立的Claude Code实例，各自有独立上下文窗口，能互相沟通，用户也能直接切过去对话。这意味着它的价值是"多个专家并行思考"，而不是"一个大脑想更多"。理解这一点才能用对场景——需要并行处理多个独立子任务时收益最大，串行依赖任务收益有限。

**场景3（计划+评审）为什么是默认最常用**：
流程是"出计划→用户确认→并行执行→Review"，这个流程在"任务中等复杂、没有现成Skill"时触发，覆盖了日常开发中绝大多数重构、新功能开发场景。用户只需在计划确认环节介入一次，其余全自动。

---

### 📦 配置/工具详表

| 工具/Skill | 安装命令/仓库 | 作用 | 与编排器的关系 |
|-----------|-------------|------|--------------|
| agent-teams-playbook | `https://github.com/KimYx0207/agent-teams-playbook` | 核心编排器，216行 | 主体 |
| find-skills（必装1） | `npx skills add KimYx0207/findskill@find-skills -y` 或手动：`https://github.com/KimYx0207/findskill` | 从社区索引搜索数百个开源Skill | 阶段2组队时自动调用，不可用则降级 |
| planning-with-files（必装2） | `npx skills add anthropic-ai/planning-with-files -y` 或手动：`https://github.com/OthmanAdi/planning-with-files` | 自动生成task_plan.md、findings.md、progress.md | 各阶段写入进度文件，不可用则跳过 |
| superpowers（进阶） | `https://github.com/obra/superpowers` | Jesse Vincent(obra)做的14个开发工作流Skill | 作为专业Agent被编排器调用 |
| everything-claude-code（进阶） | — | 专业Agent类型库，含tdd-guide、code-reviewer等subagent_type | 阶段2给角色指定subagent_type |

**superpowers 14个Skill与编排阶段对应关系**：

| Skill名 | 建议用于阶段 | 作用 |
|--------|------------|------|
| brainstorming | 阶段1 | 需求澄清、方案设计 |
| writing-plans | 阶段2 | 拆解任务、写实施计划 |
| dispatching-parallel-agents | 阶段3 | 并行派发Agent |
| subagent-driven-development | 阶段3+4 | 子Agent驱动开发+两阶段Review |
| test-driven-development | 阶段3（实现者用） | RED-GREEN-REFACTOR |
| requesting-code-review | 阶段4 | 代码审查 |
| finishing-a-development-branch | 阶段5 | 合并/PR/清理 |

---

### 🛠️ 操作流程

**1. 准备阶段：安装前置依赖**

```bash
# 必装1：find-skills（Win兼容版）
npx skills add KimYx0207/findskill@find-skills -y

# 必装2：planning-with-files
npx skills add anthropic-ai/planning-with-files -y
```

手动安装方式（两个Skill通用）：把对应仓库的`SKILL.md`放到`.claude/skills/<skill-name>/`目录下。

**2. 核心执行：安装agent-teams-playbook**

```bash
# 第1步：创建目录
mkdir -p .claude/skills/agent-teams-playbook

# 第2步：从GitHub仓库复制SKILL.md（216行）放入目录
# 仓库地址：https://github.com/KimYx0207/agent-teams-playbook
# 路径：.claude/skills/agent-teams-playbook/SKILL.md

# 第3步：无需任何依赖、环境变量、服务启动，放进去即可用
```

**3. 触发使用**

```bash
# 自然语言触发（任意说法均可）
"拉团队帮我重构认证模块"
"帮我组个Agent团队做代码审查"
"用多Agent并行处理这个任务"
"agent swarm帮我搞定这个需求"

# 直接指定场景（跳过决策树）
"用场景4帮我做用户系统"
```

**4. 验证与优化：TDD团队蓝图示例**

阶段2组建团队时，给不同角色指定subagent_type：

| 角色 | 职责 | 模型 | subagent_type |
|-----|------|------|--------------|
| 架构师 | 设计接口和模块划分 | opus | Explore |
| 实现者A | TDD实现认证模块 | sonnet | everything-claude-code:tdd-guide |
| 实现者B | TDD实现权限模块 | sonnet | everything-claude-code:tdd-guide |
| 审查员 | Code Review | sonnet | everything-claude-code:code-reviewer |

---

### 💡 具体案例/数据

**终极五件套完整链路**（需手动安装各Skill）：

```
find-skills            →  自动发现可用的社区Skill
        ↓
planning-with-files    →  生成结构化计划文件
        ↓
agent-teams-playbook   →  基于计划文件组队+编排
        ↓
superpowers skills     →  每个Agent用专业Skill执行
        ↓
tdd-guide              →  实现者遵循TDD流程
```

**"帮我做个用户系统"的完整执行路径**：
1. find-skills搜索有没有专门做用户系统的Skill
2. planning-with-files生成task_plan.md + findings.md
3. 编排器判断场景（场景4：Lead-Member）、组建团队
4. 架构师用brainstorming设计方案
5. 实现者用tdd-guide写代码（RED→GREEN→IMPROVE）
6. 审查员用code-reviewer做Code Review
7. 收尾员用finishing-a-development-branch处理合并和部署

**planning-with-files与编排器的阶段对应**：

| 阶段 | 编排器负责 | planning-with-files负责 |
|-----|----------|------------------------|
| 阶段1：任务分析 | 决策场景、选协作模式 | 生成task_plan.md |
| 阶段2：团队组建 | 分配角色、选模型 | 生成findings.md |
| 阶段3：并行执行 | 协调多Agent并行 | 各Agent更新progress.md |
| 阶段4-5：质检+交付 | 质量把关+交付 | 最终状态写入文件 |

---

### 📝 避坑指南

- ⚠️ **不建议让AI全自主决定**：阶段1的范围确认不是走过场，AI不懂你的细节需求，跳过确认很容易跑偏。可以说"OAuth也要做"来调整计划，但不建议说"不需要问我，你自己全决定"。
- ⚠️ **Agent Team不是默认选项**：Agent Team双向通信每条消息都消耗token，90%场景Subagent单向汇报就够了，只有任务间真的需要互相沟通时才升级到Agent Team。
- ⚠️ **前置Skill建议手动安装，不要放进SKILL.md**：否则每次触发编排器都会重复安装，浪费token。
- ⚠️ **质量把关最多打回2轮**：2轮还不过会通知人工介入，不会无限循环。
- ⚠️ **superpowers是工具库，agent-teams-playbook是编排器**：两者互补不竞争，superpowers的每个Skill干一件具体的事，编排器决定什么时候用哪个Skill、怎么组合。

---

### 📚 往期教程导航

| 主题 | 链接 |
|-----|------|
| Agent Teams多Agent协作框架 | `https://my.feishu.cn/wiki/CAsLwb5BBiVztakm0h9cGnucnRc` |
| everything-claude-code专业Agent类型库 | `https://my.feishu.cn/wiki/Jqf3wAPh2ixRifkssykcnNJOnkg` |
| find-skills详细教程 | `https://my.feishu.cn/wiki/HVU6wTCRoiThWAkgyLac7w3Yncb` |
| planning-with-files详细教程 | `https://my.feishu.cn/wiki/QG5Aw1fpZikJP5kHyhrcwRlznMc` |
| superpowers 14个执行Skill | `https://my.feishu.cn/wiki/Y2gqwjSQbiygUgkNuvMcEU4nnLd` |

建议阅读顺序：先看框架（1）→ 掌握Skill发现机制（3）→ 按需深入（2、4、5）

开源知识库：`https://tffyvtlai4.feishu.cn/wiki/OhQ8wqntFihcI1kWVDlcNdpznFf`

---

### 🏷️ 行业标签
#ClaudeCode #AgentTeams #多Agent编排 #Skill开发 #AI工作流 #TDD #开源工具

---

---
