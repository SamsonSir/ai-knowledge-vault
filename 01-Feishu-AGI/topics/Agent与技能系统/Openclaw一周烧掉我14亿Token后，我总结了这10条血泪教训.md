# Agent与技能系统

## 73. [2026-02-22]

## 📔 文章 5


> 文档 ID: `Ap7JwRbJIiC3lKkWZq8cmAWRnwc`

**来源**: Openclaw一周烧掉我14亿Token后，我总结了这10条血泪教训 | **时间**: 2026-02-20 | **原文链接**: `https://mp.weixin.qq.com/s/FUYc0zpj...`

---

### 📋 核心分析

**战略价值**: 用14亿token的实战代价，总结出一套让OpenClaw从"玩具"变成"睡后自动产出"的完整运维体系——核心是把agent当基础设施而非聊天机器人来设计。

**核心逻辑**:

- **模型路由是成本控制的命门**：把所有任务都压在Opus/Codex上是最大的token浪费。Sonnet 4.6 OSWorld得分72.5%，几乎追平Opus 4.6的72.7%，但成本只有五分之一，是日常agent主力的最优解。
- **Skill文件是agent行为的护栏**：没有Skill文件，agent会在同一个失败方法上循环六次、乱改配置文件、跳过文档自己瞎编。Skill文件放在`workspace/skills/`，必须手写，因为只有你知道自己的技术栈和agent会以什么方式搞砸。
- **Soul.md定义决策循环，不是待办清单**：它规定agent的操作系统——规划纪律（非琐碎任务先进规划模式）、执行循环（构建→测试→记录→决策）、升级规则（同一问题失败三次立即停止重新规划）。
- **Todo.md是自扩展任务树**：agent执行时自动分解子任务、更新状态、发现后续工作并生成新任务。睡前一个大任务，早上可能变成三四个已完成的子任务。
- **ProgressLog.md是晨间简报**：每轮构建-测试循环都记录——试了什么、通过/失败、学到了什么。早上喝咖啡时打开，不用翻会话记录就知道昨晚发生了什么。
- **Cron job是真正的后台运行机制**：会话关闭后agent失忆，长任务必须用定时任务驱动。三个定时任务（凌晨2/4/6点）轮流唤醒agent检查Todo.md，最坏情况闲置两小时就被戳醒。
- **文件就是记忆**：长会话上下文会被压缩，agent会悄悄丢失之前的决策和状态，然后重新推导一遍（有时得出不同结论）。解决办法是把所有重要信息写进workspace的markdown文件，相当于给每天早上失忆的员工写入职文档。
- **模型聊天质量 ≠ Agent质量**：工具调用可靠性才是agent工作的核心指标。一个能写诗的模型，在需要调用函数、解析结果、决定下一步时可能直接卡死。
- **集成要逐个叠加**：每个集成是独立故障点。从一个简单定时任务开始，稳定跑一周再加下一个。出问题跑`openclaw doctor --fix`。
- **Dev和Ops agent要分离**：Codex/Claude Code专门写代码调试，OpenClaw专门做监控调度通信，两者不共享上下文，防止互相污染。

---

### 🎯 关键洞察

**为什么配置本身就是产品工作**：
- 原因：agent没有内置的"你的项目"知识，它是一个能力强但极度死板的执行器，没有规则就靠猜。
- 动作：写Skill文件（行为护栏）+ Soul.md（决策操作系统）+ 文件记忆体系（对抗上下文压缩）。
- 结果：从"布置任务走开回来发现卡死"变成"睡觉时自动产出成果"。

**为什么文件记忆比向量记忆更基础**：
- 向量记忆（`openclaw memory status/search`）是高级功能，但最基础的记忆是workspace里的markdown文件。
- 透明度和可审计性比单纯的回忆更重要——你必须能看到agent"知道"关于你和项目的什么，否则你在信任一个有shell访问权限的黑盒子。
- 作者自建的Gigabrain系统已索引911+条记忆，每次对话、每个决策、每个偏好都被存储并可搜索。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 模型路由分层 | 见下方JSON配置块 | 自动降级，控制成本 | 不要把心跳/状态ping跑在Opus上 |
| Skill文件 | 放在`workspace/skills/`，手动编写 | 砍半错误率 | 必须自己写，没有通用模板 |
| Soul.md | 定义执行循环和升级规则 | agent有稳定行为模式 | 不是待办清单，是操作系统 |
| Todo.md | 实时任务树，agent自动更新 | 任务自扩展，早上有进度 | 需在Soul.md里强制agent维护它 |
| ProgressLog.md | 每轮循环记录试了什么/结果/学到什么 | 晨间简报，无需翻会话 | 需在Soul.md里强制agent写入 |
| Cron job | 见下方cron命令块 | 真正的后台运行 | 会话关闭=失忆，必须用cron驱动 |
| 安全审计 | `openclaw security audit --fix` | 标记暴露的认证和权限 | ClawHub有1184+个恶意Skill，必须审计 |
| 记忆系统 | `openclaw memory status/search` | 跨会话上下文保留 | 基础记忆还是靠markdown文件 |

**模型路由JSON配置**：
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6",
        "fallbacks": [
          "anthropic/claude-opus-4-6",
          "openrouter/moonshotai/kimi-k2.5"
        ]
      }
    }
  }
}
```

---

### 🛠️ 操作流程

1. **准备阶段**：
   - 建立workspace文件结构（见下方目录树）
   - 写Soul.md（定义执行循环、规划纪律、升级规则）
   - 写Skill文件（针对你的技术栈和agent的具体出错方式）
   - 配置模型路由JSON，主力Sonnet 4.6，后备Opus 4.6和Kimi K2.5

2. **核心执行**：
   - 用`/model`命令在聊天中随时切换模型
   - 布置任务时让agent先更新Todo.md再开始执行
   - 每轮循环强制写入ProgressLog.md
   - 配置三个cron job（凌晨2/4/6点）：
     ```bash
     openclaw cron add --name "overnight-2am" --cron "0 2 * * *" --message "Check Todo.md. Pick up incomplete tasks. Log progress."
     openclaw cron add --name "overnight-4am" --cron "0 4 * * *" --message "Continue working through Todo.md. Update progress-log."
     openclaw cron add --name "overnight-6am" --cron "0 6 * * *" --message "Final check. Summarize all overnight work."
     openclaw cron list
     ```

3. **验证与优化**：
   - 每次加新集成前，确认上一个稳定跑了至少一周
   - 定期跑安全审计：
     ```bash
     openclaw doctor --deep --fix --yes
     openclaw security audit --fix
     openclaw security audit --deep --json
     openclaw status --all --deep
     ```
   - 稳定后让agent读Skill文件+cron配置+成功运行日志，让它理解系统"正常状态"

---

### 💡 具体案例/数据

**模型性能对比**（2026年2月中旬数据）：

| 模型 | Agent质量 | 工具调用 | OSWorld/SWE-Bench |
|------|----------|---------|------------------|
| Claude Sonnet 4.6 | 优秀 | 可靠 | OSWorld 72.5% |
| Claude Opus 4.6 | 优秀 | 可靠 | OSWorld 72.7%，100万token上下文 |
| GPT-5.3-Codex | 优秀 | 可靠 | SWE-Bench Pro最顶尖，比5.2快25% |
| Kimi K2.5 | 不错 | 可靠 | — |
| MiniMax M2.5 | 不错 | 可靠 | SWE-Bench 80.2%，开源MIT协议 |
| GLM-5 | 尚可 | 稳定 | 重推理任务稳定 |

**Workspace文件结构**：
```
~/.openclaw/workspace/
├── USER.md        # 你是谁，偏好，上下文
├── AGENTS.md      # Agent身份和路由
├── HEARTBEAT.md   # 每次心跳要检查什么
├── MEMORY.md      # 长期事实
├── Soul.md        # 决策循环和行为
├── Todo.md        # 当前任务
└── progress-log.md # 运行日志
```

**Soul.md核心内容模板**：
```markdown
## 操作系统

### 核心方法
- 把每个有意义的任务当作执行循环，而不是一次性尝试。
- 优先验证结果，而不是快速猜测。
- 保持决策透明，确保进度可审计。

### 规划纪律
- 任何非琐碎请求都从规划模式开始。
- 在实施前定义范围、约束条件和明确的"完成"标准。
- 如果事实改变或某一步失败，暂停执行并重新规划。

### 执行循环
- 重复：构建 → 测试 → 记录 → 决策。
- 构建最小的有意义的改动。
- 立即针对预期行为进行测试。
- 把变更、通过/失败情况、下一步该做什么记录在`progress-log.md`里。
- 根据证据决定迭代、升级或关闭。

### 任务管理
- 保持`todo.md`作为实时真相来源。
- 将工作分解为子任务，持续更新状态。
- 发现后续任务时立即添加，而不是留下隐性债务。

### 学习循环
- 每次纠正后，追加到`tasks/lessons.md`。
- 每条记录：失败情况、根本原因、预防规则。
- 每次会话开始前回顾教训。

### 质量关卡
- 没有证据绝不标记完成。
- 要求测试通过、日志干净且可理解、可观察的正确性。
- 最终检查："一个资深工程师会批准这个作为生产就绪代码吗？"

### 升级规则
- 缺少凭证、外部故障或需求模糊时立即升级。
- 同一问题上失败三次后，停止并重新规划再继续。
```

**安全事故数据**：
- OpenClaw存在多个CVE，包括CVSS 8.8的远程代码执行漏洞
- Bitsight和Censys扫描发现超过3万个暴露实例
- ClawHavoc活动在ClawHub种植了1,184+个恶意Skill，占整个注册表约12%
- 恶意Skill类型：加密货币窃取器、反向shell、伪装成交易机器人和生产力工具的凭证外泄
- CrowdStrike、Cisco、Kaspersky均已发布警告

---

### 📝 避坑指南

- ⚠️ 心跳/状态ping/定时检查绝对不要跑在Opus上，这是14亿token的主要烧法
- ⚠️ 不写Skill文件就上线agent，等于让一个能力强但没有操作手册的员工自由发挥——它会在同一个失败方法上循环六次
- ⚠️ 会话关闭后agent完全失忆，长任务不配cron job就是在赌运气
- ⚠️ 长会话上下文会被压缩，agent会悄悄丢失之前的决策，第二次推导可能得出不同结论——所有重要状态必须写文件
- ⚠️ 不要一次性配多个集成，每个集成是独立故障点，出问题时无法定位根因
- ⚠️ ClawHub上的Skill不可盲目信任，安装前必须跑`openclaw security audit`，供应链投毒是真实威胁
- ⚠️ agent有shell访问权限、浏览器控制权，能以你的名义发消息，不需要问你就执行——透明度和可审计性是硬需求，不是可选项

---

### 🏷️ 行业标签
#OpenClaw #AI-Agent #VibeCoding #模型路由 #Agent运维 #Token优化 #自动化工作流 #安全审计

---

---
