# AI学习与效率工具

## 11. [2026-02-28]

## 📔 文章 5


> 文档 ID: `MA3XwzFCOipNLakwdI5cOqvtn1g`

**来源**: OpenClaw+Obsidian+CC｜AI时代知识管理神器（20分钟装好全套） | **时间**: 2026-02-27 | **原文链接**: `https://mp.weixin.qq.com/s/EMahAzgf...`

---

### 📋 核心分析

**战略价值**: 用 OpenClaw（AI Agent）+ Obsidian（知识库）+ Claude Code（AI编程助手）三件套，跑通「收集→整理→创作→分享」完整知识管理闭环，全程无需命令行，小白20分钟可装完。

**核心逻辑**:

- **三件套分工明确**：OpenClaw 负责信息收集与处理（飞书端），Obsidian 负责知识沉淀与调用，Claude Code（Claudian插件）负责深度创作与分析，三者缺一不可
- **Cherry Studio 是安装入口**：通过 Cherry Studio 一键安装 OpenClaw，无需碰终端，解决小白最大痛点——环境配置问题
- **AI模型是龙虾的燃料**：OpenClaw 本身不含模型，必须外接 API，推荐阿里云百炼 Coding Plan（Lite版），配置地址为 `https://coding.dashscope.aliyuncs.com/v1`
- **4个模型按场景选用**：kimi-k2.5（默认主力）、glm-5（稳定可靠）、MiniMax-M2.5（响应速度快）、qwen3.5-plus（百万上下文）
- **飞书是手机端入口**：OpenClaw 本地部署后只能在电脑 Dashboard 用，对接飞书后才能手机随时调用，实现「刷到即处理」
- **4个必备Skill是地基**：x-reader（解析公众号/小红书/B站链接）、Multi Search Engine（17个搜索引擎）、Obsidian Skill（存入知识库）、find-skills（发现新能力）——缺任何一个，闭环就断
- **软链接打通OB与龙虾**：建立软链接后，OB里出现「龙虾工作区」文件夹，在OB编辑 SOUL.md 立即影响龙虾行为，双向实时同步
- **workspace 4个核心文件决定龙虾质量**：USER.md（你的信息）、SOUL.md（龙虾性格）、IDENTITY.md（龙虾形象）、AGENTS.md（工作手册），默认模板只能通用回复，第一天必须填好 USER.md
- **龙虾会自己教你配置**：飞书对接、OB安装、Skill安装，全部可以直接把指令发给龙虾，让它一步步引导，遇到报错复制给它即可
- **开源Skill库可扩展能力**：`https://github.com/cafe3310/public-agent-skills` 覆盖创作、部署、项目管理、辅助工具四大场景，全部免费

---

### 🎯 关键洞察

**为什么这套组合有效**：

传统知识管理断在「收集」和「调用」两个环节——收集靠收藏夹（死库），调用靠记忆（不可靠）。这套三件套的逻辑是：

1. OpenClaw 住在飞书里，随手转发即处理，不打断心流
2. 处理结果自动存入 Obsidian，形成结构化知识库
3. Claude Code 在 OB 内直接调用知识库做深度创作

关键在于**软链接**这一步——它让龙虾的工作区和OB知识库物理打通，不是两个独立系统，而是同一份数据的两个视图。

**Skill 的本质**：提示词 + 代码的集合。安装前建议让龙虾帮你审核内容，避免执行不明代码。

---

### 📦 配置/工具详表

| 模块 | 关键设置/命令 | 预期效果 | 注意事项/坑 |
|------|------------|---------|-----------|
| Cherry Studio | 下载对应系统安装包，打开后找红色龙虾图标 | 一键安装OpenClaw，无需终端 | Mac/Win/Linux均有版本 |
| 阿里云百炼 API | 提供商类型选 OpenAI；API地址：`https://coding.dashscope.aliyuncs.com/v1` | 接入模型服务 | 购买后在控制台点「生成Key」获取 |
| 4个模型ID | `kimi-k2.5` / `glm-5` / `MiniMax-M2.5` / `qwen3.5-plus` | 覆盖不同使用场景 | 模型ID复制到框里，名称自动填充 |
| 飞书对接 | 发给龙虾："帮我配置飞书，让我能通过飞书手机端跟你对话。一步步引导我，每步做完等我确认再继续" | 手机端可用 | 报错直接复制给龙虾 |
| Claudian插件 | 下载 main.js、manifest.json、styles.css 放到 `.obsidian/plugins/claudian/` | OB内出现CC对话窗口 | 需关闭OB安全模式才能启用 |
| cc-switch | 设置里下滑开启「跳过Claude Code初次安装确认」 | 跳过繁琐初始化 | 配置同一个百炼API Key |
| 软链接 | 发给龙虾："帮我建一个软链接，把你的工作区链接到我的OB仓库里，建一个叫「龙虾工作区」的文件夹。你自己找到路径，直接帮我搞定" | OB与龙虾双向实时同步 | 龙虾自动定位路径，无需手动 |

---

### 🛠️ 操作流程

**Step 1 安装 Cherry Studio + OpenClaw**
- 下载 Cherry Studio（Mac/Win/Linux）并安装打开
- 首页找红色龙虾图标 → 点进去 → 点绿色「安装 OpenClaw」按钮
- 等进度条走完，无需碰终端

**Step 2 购买阿里云百炼并获取 API Key**
- 打开百炼 Coding Plan 页面，选 Lite 版购买
- 购买后在控制台点「生成 Key」，复制 API Key

**Step 3 在 Cherry Studio 配置模型**
- ⚙️设置 → 模型服务 → 拉到底点「+ 添加」
- 提供商名称：阿里（随意）；提供商类型：**OpenAI**
- API密钥：粘贴百炼Key；API地址：`https://coding.dashscope.aliyuncs.com/v1`
- 依次添加4个模型ID：`kimi-k2.5`、`glm-5`、`MiniMax-M2.5`、`qwen3.5-plus`

**Step 4 启动龙虾**
- 左侧点OpenClaw图标 → 模型下拉选 `kimi-k2.5 | 阿里云百炼` → 点绿色「▶ 启动」
- 发「你好」，收到回复 = 安装成功 ✅

**Step 5 对接飞书**

发给龙虾：
```
帮我配置飞书，让我能通过飞书手机端跟你对话。一步步引导我，每步做完等我确认再继续
```
飞书里搜到机器人、发消息收到回复 = 飞书对接完成 ✅

**Step 6 安装 Obsidian + Claude Code**

发给龙虾：
```
帮我安装 Obsidian 知识库和 Claude Code，请按以下步骤引导我：
第一步：安装 Obsidian
第二步：安装 Claudian 插件 （Claude Code 的 OB 可视化界面）
4. 帮我下载 Claudian 插件文件 
https://github.com/YishenTu/claudian （main.js、manifest.json、styles.css）
5. 放到我的 OB 仓库的 .obsidian/plugins/claudian/ 目录下
6. 引导我在 OB 设置里关闭安全模式、启用 Claudian
第三步：安装 cc-switch
7. 帮我从 cc-switch releases 下载对应系统的安装包
8. 引导我安装并配置阿里云百炼 API Key（用我之前买的那个百炼 Coding Plan 的 Key）
9. 记得先点开设置，下滑开启跳过 Claude Code 初次安装确认
第四步：验证
10. 引导我点 OB 左侧 claudian，发"你好"测试
11. 收到回复代表成功
12. 每一步做完等我确认再继续
```
OB侧边栏出现CC对话窗口、发「你好」收到回复 = OB + Claude Code 安装完成 ✅

**Step 7 安装4个必备 Skill**

发给龙虾：
```
帮我安装以下 4 个必备 Skill，按顺序来：
1. Multi Search Engine （免费搜索引擎，17 个搜索引擎覆盖国内外）
npx clawhub@latest install multi-search-engine
2. x-reader （国内链接解析：微信公众号、小红书、B 站、X 等）
pip install git+https://github.com/runesleo/x-reader.git
3. Obsidian （让你能直接往我的 OB 知识库里存东西）
npx clawhub@latest install obsidian
4. find-skills （搜索和发现更多 Skill）
npx clawhub@latest install find-skills
每装完一个，帮我验证是否安装成功，再装下一个。
```

**Step 8 建立软链接打通OB与龙虾**

发给龙虾：
```
帮我建一个软链接，把你的工作区链接到我的 OB 仓库里，建一个叫「龙虾工作区」的文件夹。你自己找到路径，直接帮我搞定
```
OB里出现「龙虾工作区」文件夹 = 打通完成 ✅

**Step 9 填写 USER.md（第一天必做）**
- 打开OB「龙虾工作区」→ 找到 USER.md
- 填入：名字、职业、工作时间、沟通偏好
- 其他文件（SOUL.md、IDENTITY.md、AGENTS.md）可以慢慢调

---

### 💡 具体案例/数据

**场景1 爆款笔记拆解**：刷小红书看到好帖子 → 飞书转发给OpenClaw → 龙虾拆解底层逻辑 → 顺着聊选题/原理 → 经验自动沉淀到OB → 下次AI直接调用

**场景2 创意前的功课**：去生鲜电商公司交流AI制作TVC → 等桌时用龙虾调研行业和品牌资料 → 沉淀到OB → 晚上回家速读 → 和Claudian深聊完善调研 → 跑出TVC创意方向

**进阶Skill库**：`https://github.com/cafe3310/public-agent-skills`
- 创作与知识管理：语音转写、研究报告、去AI味
- 在线平台：部署到ModelScope，一键发布到社区
- 项目管理：PMP迭代、TDD、轻量管理
- 辅助工具：媒体库整理、表情包制作

---

### 📝 避坑指南

- ⚠️ 提供商类型必须选 **OpenAI**，不要选其他，否则API无法调通
- ⚠️ 启动龙虾前必须先配好模型，否则龙虾无法回复
- ⚠️ 安装Claudian插件前必须在OB设置里**关闭安全模式**，否则插件无法启用
- ⚠️ cc-switch安装后记得进设置**开启「跳过Claude Code初次安装确认」**，否则每次启动都要手动确认
- ⚠️ USER.md 不填 = 龙虾只会通用回复，第一天就填好是最高ROI的操作
- ⚠️ 安装第三方Skill前，建议让龙虾先帮你审核内容，Skill本质是提示词+代码，来源不明的有风险
- ⚠️ 本文方案为**本地部署**，云端部署是另一套流程

---

### 🏷️ 行业标签

#知识管理 #OpenClaw #Obsidian #ClaudeCode #AI工作流 #个人知识库 #飞书机器人 #阿里云百炼 #Agent #本地部署

---

---
