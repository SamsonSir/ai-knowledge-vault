# 工作流自动化

## 9. [2026-01-22]

## 📒 文章 7


> 文档 ID: `RpcgwvZqTiEjGZkyjmhcXN83nKf`

**来源**: 进阶教程：给AI装上"逻辑大脑"，打造金融级稳定的多轮对话Agent（Dify实战） | **时间**: 2026-01-21 | **原文链接**: `https://mp.weixin.qq.com/s/XqkFrh4N...`

---

### 📋 核心分析

**战略价值**: 用「状态机 + 多专职LLM节点」替代单一大模型记忆，在Dify工作流中实现金融级可控的多轮对话Agent，解决槽位丢失、意图污染、任务中断等生产级痛点。

**核心逻辑**:

- **痛点根源**：纯LLM记忆依赖概率，上下文超长后任务状态极易丢失；私有化开源模型能力更弱，金融合规场景不可接受随机输出。
- **状态机本质**：一个显式维护的「笔记本」，记录当前任务ID、任务栈、槽位值、任务阶段，在提示词中直接注入最新状态，比依赖LLM隐式记忆任务完成率高出一个量级。
- **对话历史收集方案**：在每个直接回复节点后挂代码节点，将`user`+`assistant`格式化后写入会话变量`history`（str类型，覆盖模式），最多保留10轮，超出则丢弃最早轮次（生产建议改为压缩策略）。
- **query改写节点升级**：将完整`history`字符串注入改写节点的user prompt，温度调低，加额外规则约束，解决代词指代不清、改写错误问题。
- **问题分类路由**：用户输入经改写后，先走分类节点，分为 FAQ / 单轮任务 / 多轮任务 / 转人工 / 闲聊 五类，再分发给对应处理分支，防止意图污染。
- **多轮任务槽位追问**：信息提取节点检查`task_slots`中value为`null`/`None`/空字符串的字段，追问节点每次只问一个缺失槽位，口语化表达，直到槽位全满才进入执行阶段。
- **状态机强制拦截**：即便LLM判断「可以执行」，状态机仍会检查`current_task_slots`，若有`null`槽位则强制将`stage`保持在`COLLECTING`，拒绝进入`EXECUTING`，防止LLM跳步。
- **任务栈级联更新**：用户全局意图变更时（如「不去拉萨了改去三亚」），触发`__updated_variables`，状态机清空栈内关联子任务，重新定位主任务并更新槽位值。
- **多专职LLM节点**：query改写、意图分类、信息提取、槽位追问、FAQ检索、单轮任务执行各用独立LLM节点，每个节点只做一件事，提升单节点成功率。
- **会话变量全部用str类型**：Dify中JSON属性不支持嵌套，且JSON不支持直接在LLM提示词中引用，因此所有状态数据序列化为字符串存储。

---

### 🎯 关键洞察

**为什么状态机比纯LLM记忆更可靠**：

- LLM是概率模型，上下文窗口越长、任务越复杂，「遗忘」概率越高。即便是Gemini这类顶级模型也会出现任务状态丢失。
- 状态机将任务状态「外化」为结构化字符串，每轮对话都把最新状态注入提示词（如`#当前状态是查询天气信息收集中`），LLM每次都能看到完整的当前快照，不依赖隐式记忆。
- 金融场景的核心诉求是「可靠可控」，状态机提供了确定性的流程控制，LLM只负责语义理解和自然语言生成，两者职责分离。

**任务栈（task_stack）的「后进先出」逻辑**：

用户在处理「查天气」过程中插入「查路线」，系统将「查路线」压入栈顶，优先处理；「查路线」完成后弹出，自动恢复「查天气」任务，不丢失原始槽位。这是解决「多轮任务中途插话」问题的核心机制。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 会话变量 `history` | 类型：str；赋值模式：覆盖 | 存储最近10轮对话，格式为`user: xxx\n\nassistant: xxx` | 必须是str类型，不能用JSON |
| 会话变量 `current_task_slots` | 类型：str | 存储当前任务的槽位键值对 | 序列化为字符串，LLM提示词可直接引用 |
| 会话变量 `current_task` | 类型：str | 存储当前任务名称 | 同上 |
| 会话变量 `sys_context_str` | 类型：str | 存储全量状态机信息（含锁、栈、阶段） | 同上 |
| 代码节点（历史收集） | 见下方代码块 | 格式化并截断对话历史 | 超10轮直接丢弃，生产建议改压缩分支 |
| 代码节点（状态机维护） | 代码较长，作者提供DSL，评论区索取 | 维护task_stack、slots、stage、global_intent_lock | 每次路由后必须先更新状态机再执行任务 |
| 变量赋值节点 | 选择「覆盖」模式 | 将代码节点输出写回会话变量 | 必须在代码节点之后立即接变量赋值节点 |
| 追问节点（LLM） | 见下方Prompt模板 | 每次只追问一个缺失槽位，口语化 | 不要一次问多个槽位 |
| Agent节点 | 简单提示词 + 工具调用 | 执行单轮任务（如查天气API） | 模拟场景可简化，生产需完善提示词 |

---

### 🛠️ 操作流程

**1. 准备阶段：创建会话变量**

在Dify Chatflow中创建以下会话变量（全部选str类型）：

| 变量名 | 类型 | 赋值模式 |
|---|---|---|
| `history` | str | 覆盖 |
| `current_task` | str | 覆盖 |
| `current_task_slots` | str | 覆盖 |
| `sys_context_str` | str | 覆盖 |

**2. 核心执行：搭建工作流节点链**

```
用户输入
  → [代码节点] 历史收集（更新history）
  → [变量赋值节点] 写入history会话变量
  → [LLM节点] query改写（注入history）
  → [LLM节点] 意图分类（FAQ / 单轮 / 多轮 / 转人工 / 闲聊）
  → [代码节点] 状态机更新（更新sys_context_str / current_task / slots）
  → [变量赋值节点] 写入状态机会话变量
  → [条件判断] 是否多轮任务？
      ├─ 是 → [LLM节点] 信息提取 → [条件判断] 槽位是否全满？
      │           ├─ 否 → [LLM节点] 追问节点 → 输出追问话术
      │           └─ 是 → [Agent节点] 执行任务 → 输出结果
      ├─ FAQ → [知识库检索] → 输出答案
      ├─ 单轮任务 → [API调用] → 输出结果
      └─ 转人工 → 转人工流程
```

**3. 历史收集代码节点（完整代码）**

```python
def main(old_history: str, user_query: str, **kwargs) -> dict:
    current_answer = ""
    # 从上游所有分支中找到非空回答
    for key, value in kwargs.items():
        if value and str(value).strip() and str(value).lower() != "none":
            current_answer = str(value).strip()
            break
    # 空值保护
    if not current_answer or not user_query:
        return {"result": old_history or ""}
    # 格式化当前轮次
    new_turn = f"user: {user_query.strip()}\n\nassistant: {current_answer.strip()}"
    separator = "\n\n---\n\n"
    # 拼接历史
    if not old_history or not str(old_history).strip():
        full_history = new_turn
    else:
        full_history = f"{old_history.strip()}{separator}{new_turn}"
    # 截断：只保留最近10轮
    history_list = full_history.split(separator)
    if len(history_list) > 10:
        history_list = history_list[-10:]
    final_output = separator.join(history_list)
    return {"result": final_output}
```

**4. 追问节点Prompt模板（完整）**

```
# Role
你是一个专业的对话意图澄清助手。你的工作是根据当前的任务状态和已收集的信息，判断还缺少哪些关键信息，并向用户发起追问。

# Context
用户正在进行一项多轮对话任务，系统维护了一个"状态机"来记录任务进度。

# Goal
请检查 `task_slots` 中 value 为 `null` 或 `None` 或 空字符串 的字段。
生成一句简短、自然、礼貌的追问，引导用户补充这些缺失的信息。

# Constraints
1. 只追问缺失项：不要提及已经填好的项，除非为了确认上下文。
2. 一次问一个：如果缺多个槽位，优先追问逻辑上最靠前或最重要的一个。
3. 口语化：不要使用"请输入参数 city"，要说"请问您想查询哪个城市？"。
4. 输出格式：直接输出追问话术，不要包含任何 JSON、Markdown 标记或额外解释。

# Examples
## Example 1
Input: Task: 查询天气 | Slots: {"city": "上海", "date": null}
Output: 没问题，请问您想查询上海哪一天的天气呢？

## Example 2
Input: Task: 查询路线 | Slots: {"origin": null, "destination": "北京西站"}
Output: 收到，那您的出发地是哪里？

## Example 3
Input: Task: 预订会议室 | Slots: {"time": null, "people": null}
Output: 好的，请问您计划在这个会议室开会的时间大概是几点？
```

**5. 验证与优化**

- 用「查天气→插问保险→确认投保→改目的地」这条链路做端到端测试，验证任务栈压栈/弹栈是否正确。
- 检查每轮输出的`sys_context_str`，确认`stage`、`slots`、`global_intent_lock`值符合预期。
- 观察`history`变量是否在第11轮正确丢弃第1轮。

---

### 💡 具体案例/数据

**5轮多意图对话的状态机完整流转**：

| 轮次 | 用户输入 | LLM提取 | 状态机动作 |
|---|---|---|---|
| 01 | "下周三我想从成都开车去拉萨。" | 任务:路径规划；from:成都, to:拉萨, date:2026-01-28 | 创建task_id:451425c2，压入task_stack；global_intent_lock=LOCKED |
| 02 | "那边现在冷吗？推荐个保险吧。" | 任务:投保咨询；type:旅游险；识别高原背景 | task_stack顶部新增投保任务；current_task切换为保险；stage=COLLECTING；high_risk_confirm=null |
| 03 | "会有高原反应吗？保险管这个吗？" | 意图:FAQ；无新槽位 | 挂起投保任务；允许LLM回答FAQ；不改变current_task的任务ID |
| 04 | "行，那买一份吧。" | 意图:确认投保（LLM可能直接跳支付） | 状态机检查slots发现high_risk_confirm=null；强制stage保持COLLECTING；回复"请确认是否包含攀登等高风险运动" |
| 05 | "不去了，改去三亚，那边暖和。" | 意图:全局变更；to:三亚 | 触发__updated_variables；清空高原相关保险子任务；恢复路径规划主任务；to从拉萨改为三亚 |

**查天气三轮对话效果验证**：
```
user: 天气咋样啊
assistant: 请问您想查询哪个城市的天气呢？
---
user: 北京
assistant: 没问题，请问您想查询北京哪一天的天气呢？
---
user: 今天的
assistant: 北京 · 2026-01-21 | 晴 | -5℃ ~ 4℃ | 西北风3级 | 湿度42% | 早晚温差大，外

---

---
