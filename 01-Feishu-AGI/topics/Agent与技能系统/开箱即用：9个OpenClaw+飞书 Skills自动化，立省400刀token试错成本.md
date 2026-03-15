# Agent与技能系统

## 54. [2026-02-10]

## 📒 文章 7


> 文档 ID: `Wo9BwSBJhinyAzkEOGhc4ez7nbb`

**来源**: 开箱即用：9个OpenClaw+飞书 Skills自动化，立省400刀token试错成本 | **时间**: 2026-03-13 | **原文链接**: 无直接链接

---

### 📋 核心分析

**战略价值**: 花 $400+ Token 实测飞书 200+ API 后，将所有踩坑经验封装成 9 个可直接加载的 AI Agent Skill（Markdown 文档），让后来者零试错成本复用。

**核心逻辑**:

- **Skill 的本质**：一份写给 AI 看的 Markdown「避坑手册」，AI 调用 API 前先读它，等同于老员工给新人写的操作规范，不是代码/SDK/插件
- **省钱逻辑量化**：无 Skill 时写日期字段需试 4 次、耗 $1.8 Token、15 分钟；有 Skill 后一次成功、3 秒完成——核心原因是 Skill 里明确写了「日期字段必须转换为 13 位毫秒级时间戳」
- **安装方式**：两种路径，方式1下载 Zip 解压复制；方式2 git clone 后 `cp -r` 到 `~/.openclaw/workspace/skills/`，最后统一执行 `openclaw gateway restart` 重载
- **9 个 Skill 覆盖范围**：云文档(doc-writer)、多维表格(bitable)、日历(calendar)、消息与群管理(im)、任务(task)、知识库(wiki)、文件管理(drive)、组织架构(contact)、审批(approval)
- **最高频踩坑类型**：时间戳精度混用（Calendar 用 10 位秒级字符串，Bitable/Task 用 13 位毫秒级字符串，两者不可互换）
- **权限黑盒是最大隐患**：机器人创建的文件/群/空间默认归属机器人，用户不可见——必须在每次创建后立即补调权限接口
- **并发写入是文档乱序根源**：飞书 Docx API 对并发极敏感，所有 Block 必须放在单一 `children` 数组一次性 POST，或严格串行等待
- **ID 类型错传是审批/消息失败主因**：OpenID/UserID/UnionID 三者不可混用，所有接口必须显式声明 `user_id_type`
- **开源地址**：`https://github.com/alextangson/feishu_skills`，Star 数量影响更新速度
- **200+ API 仍在持续测试**，9 个为第一批开源，后续陆续释出

---

### 🎯 关键洞察

**Skill 的知识传递范式转变**：传统靠文档传递知识、靠 SDK 传递功能；Skill 把「人的试错成本」直接封装给 AI 继承。一个人踩过的坑，通过 Skill 让所有接入的 Agent 永远不再踩。

**飞书 API 的系统性陷阱规律**：
1. 时间戳单位不统一（跨 Skill 开发必须查表）
2. 创建成功 ≠ 用户可见（群、文件、空间均需补授权）
3. 表单/卡片的 JSON 必须二次字符串化（直接传对象会被当纯文本处理）
4. 权限问题优先排查「机器人可见范围」设置，而非代码逻辑

---

### 📦 配置/工具详表

| Skill 模块 | 核心 API 能力 | 关键坑/注意事项 | 解决方案 |
|-----------|-------------|--------------|---------|
| feishu-doc-writer | Markdown→Docx Block、Heading/Bullet/Code/Callout、文字样式 | 并发写入导致顺序随机错乱；Markdown 表格支持不稳定 | 单一 Batch 请求或串行等待；表格转无序列表 |
| feishu-bitable | CRUD（500条/次）、Upsert、字段管理、看板/甘特图、权限管理 | 数字字段禁传字符串；日期必须 13 位毫秒时间戳；限频 5次/秒 | 写入前调 `GET /fields` 读表结构；高并发加延时排队 |
| feishu-calendar | 创建日程、邀约参会人、会议室查询、空闲忙查询、变更订阅 | 创建时传 `attendees` 字段会被静默忽略；时间戳是 10 位秒级字符串 | 先创建拿 `event_id`，再补调「添加参与人」API；显式带 `timezone: "Asia/Shanghai"` |
| feishu-im | 文本/卡片消息、置顶、加急(Buzz)、撤回、建群拉人、群公告/菜单/Tab/Widget | 创建群后手机不可见；卡片显示为代码字符串；`emoji_type` 必须大写 | 创建后立即调「拉人入群」；`content` 必须字符串化 JSON；批量发送≤200群 |
| feishu-task | 创建/完成任务、评论留痕、附件关联 | `due.timestamp` 必须 13 位毫秒字符串（传 10 位显示 1970 年）；不指派人任务无提醒 | `members` 字段必填并设 `role: "assignee"`；更新时显式声明 `update_fields` |
| feishu-wiki | 空间列表、多级目录树、外部文档挂载、节点迁移/重命名 | 机器人直接创建顶级空间报 403；`node_token` ≠ `obj_token` | 手动建群→Wiki 空间设置中将群组设为管理员；写内容前先 `get_node` 获取 `obj_token` |
| feishu-drive | 多级文件夹创建、文件上传/克隆、元数据查询、权限管理 | 机器人创建的文件用户不可见；根目录随意创建难管理 | 「写后必授」：上传后立即调 `permissions` 接口加 `full_access`；先手动建顶级锚点文件夹 |
| feishu-contact | OpenID 获取、ID 体系互转(OpenID/UserID/UnionID)、部门检索、成员创建 | 搜不到用户≠用户不存在（是机器人可见范围未包含该用户）；手机号格式敏感 | 后台将机器人「可见范围」设为全员；本地建 KV 缓存 Phone→OpenID 映射减少限频 |
| feishu-approval | 自动填单发起、AI 审计评论、卡片动态更新、审批状态监听 | 控件 ID（widget177...）随机生成不可硬编码；`form` 字段需二次 Stringify；不支持 API 创建审批流定义 | 先调 `get_approval_definition` 获取真实 Widget ID；所有审批接口显式指定 `user_id_type` |

---

### 🛠️ 操作流程

**方式1（快速）**

1. 准备阶段：访问 `https://github.com/alextangson/feishu_skills`，下载 Zip 并解压
2. 核心执行：将解压后的 skill 文件夹复制到 `.openclaw/workspace/skills/` 目录
3. 验证与优化：执行 `openclaw gateway restart`，重启后自动加载

**方式2（Git）**

1. 准备阶段：
```bash
git clone https://github.com/alextangson/feishu_skills.git
```
2. 核心执行：
```bash
cp -r feishu_skills/feishu-* ~/.openclaw/workspace/skills/
```
3. 验证与优化：
```bash
openclaw gateway restart
```

---

### 💡 具体案例/数据

| 场景 | 无 Skill | 有 Skill | 差异 |
|-----|---------|---------|-----|
| 写多维表格日期字段 | 试错 4 次，$1.8 Token，15 分钟 | 一次成功，~$0，3 秒 | 原因：Skill 明确标注「13 位毫秒时间戳」 |
| 总测试投入 | $400+ Token | — | 换回 9 个 Skill 的第一手实测经验 |
| 飞书 API 总量 | 200+ | 9 个已开源 | 剩余持续测试中 |
| Bitable 批量操作上限 | — | 500 条/次 | 超出需分批 |
| IM 批量发消息上限 | — | 200 个群/次 | 超出触发封禁 |
| Bitable API 限频 | — | 5 次/秒 | 高并发必须延时排队 |

**典型自动化链路示例（会议→任务→文档）**：
1. `feishu-im` 提取群聊结论
2. `feishu-task` 自动派发 TODO（`due.timestamp` 用 13 位毫秒，`members` 指定 `role: "assignee"`）
3. `feishu-doc-writer` 生成会议纪要云文档（所有 Block 单次 POST）
4. `feishu-wiki` 挂载至对应项目节点（先 `get_node` 拿 `obj_token`）

---

### 📝 避坑指南

- ⚠️ **时间戳单位混用**：Calendar = 10 位秒级字符串；Bitable/Task = 13 位毫秒级字符串。传错直接导致时间显示 1970 年或 400 报错
- ⚠️ **并发写文档**：飞书 Docx API 并发写入会导致 Block 顺序随机错乱，必须单一 Batch 或串行
- ⚠️ **群创建后不可见**：创建群成功后必须立即补调「拉人入群」API，否则群在手机端不显示
- ⚠️ **卡片 JSON 未字符串化**：`content` 直接传 JSON 对象会被飞书当纯文本输出为代码字符串，必须先 `JSON.stringify()`
- ⚠️ **审批控件 ID 硬编码**：`widget177...` 是随机生成的，不同审批流同名控件 ID 不同，必须先调 `get_approval_definition` 动态获取
- ⚠️ **Wiki 权限 403**：机器人无法直接创建顶级空间，需手动建群→在 Wiki 空间设置中将群组设为管理员
- ⚠️ **Drive 文件失踪**：机器人创建的文件默认归属机器人，用户不可见，必须「写后必授」调 `permissions` 接口
- ⚠️ **Contact 搜不到用户**：不是用户不存在，是机器人「可见范围」未包含该用户，去开发者后台改「可见范围」为全员
- ⚠️ **Calendar 邀约静默失败**：创建日程时 `attendees` 字段会被忽略，必须拿到 `event_id` 后补调「添加参与人」接口
- ⚠️ **node_token vs obj_token**：Wiki 的 `node_token` 是目录位置，`obj_token` 才是真实文档，写内容必须用 `obj_token`

---

### 🏷️ 行业标签

#OpenClaw #飞书自动化 #AIAgent #Skill #多维表格 #飞书API #工作流自动化 #开源工具 #AGI工程化 #企业协同

---

---
