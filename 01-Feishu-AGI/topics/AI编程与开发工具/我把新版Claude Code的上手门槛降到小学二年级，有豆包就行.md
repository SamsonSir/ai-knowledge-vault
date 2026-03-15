# AI编程与开发工具

## 5. [2026-01-14]

## 📙 文章 4


> 文档 ID: `SGMSwGtoHin7D2kWETOcb4MKn4e`

**来源**: 我把新版Claude Code的上手门槛降到小学二年级，有豆包就行 | **时间**: 2026-01-14 | **原文链接**: `https://mp.weixin.qq.com/s/kKU8otnN...`

---

### 📋 核心分析

**战略价值**: 用豆包AI替代手动查教程，配合OpenRouter（支付宝付款）+ cc-switch + Skills + OpenCode，搭建一套无需国外银行卡、可切换六家模型、稳定用一年的本地AI编程全家桶。

**核心逻辑**:

- OpenRouter是模型API聚合市场，不加价，透明定价，平台只收充值手续费（信用卡5.5%），支持支付宝付款，无需国外银行卡
- OpenRouter可以把已有的OpenAI、Anthropic等API Key存入统一管理，一次配置长期复用
- OpenRouter内有大量免费模型：小米、DeepSeek、GLM、Qwen等，每周更新模型使用排行榜
- 安装Claude Code和cc-switch不需要查教程，直接把需求口述给豆包，说明电脑系统，让豆包给出完整安装命令，包括终端怎么打开都可以问
- cc-switch是统一管理面板，可视化界面，同时支持Claude Code、CodeX、Gemini CLI的API管理，启动前选好供应商，模型自动切换
- Skills是给Claude Code用的知识库文件夹（不是普通Prompt），可放规范、脚本、模板、参考资料，Agent按需自动调取；支持热加载，生成后无需重启即可使用
- skill-creator是官方技能，用于帮你设计新技能，安装后直接用自然语言描述需求即可生成定制Skills
- OpenCode安装命令（Mac最稳定版）：`curl -fsSL https://opencode.ai/install | bash`，首次运行输入 `/model` 选免费模型
- oh-my-opencode是OpenCode的核心插件，缺少它OpenCode不完整，安装方式：在OpenCode界面运行 `按照这里的说明进行安装和配置 https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/README.md`
- 反代方式（opencode-antigravity-auth薅Gemini Pro额度）封号率高，明确不推荐；稳定方案是通过OpenRouter使用Gemini

---

### 🎯 关键洞察

**为什么用OpenRouter而不是中转API**：
- 中转API本质是灰色通道（绕路/拼车/代刷），价格波动大，多平台充值导致利用率低（作者实测年底利用率仅30%）
- OpenRouter是官方聚合入口，定价透明，底层供应商定多少就是多少，且支持把已有Key存入，不会浪费已有资源

**为什么用豆包替代教程**：
- 现有教程数量虽多但质量参差，且不同系统命令不同，遇到报错还要再搜
- 把官方安装指南打包给豆包，拍照提问，豆包直接给出适配当前系统的完整命令，连"怎么打开终端"都能问

**终极形态分工逻辑**：
- Claude Code → 整个项目代码
- Cursor → 单个文件调整、开发进度记录
- OpenCode → 项目模块处理、修Bug
- 三个入口同时挂掉的概率极低，形成冗余保障

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| OpenRouter注册充值 | 支付界面选支付宝 | 无需国外银行卡 | 信用卡收5.5%手续费，支付宝更划算 |
| OpenRouter API Key | 新建Key后复制备用 | 统一管理所有模型入口 | 可将已有OpenAI/Anthropic Key存入 |
| Claude Code + cc-switch安装 | 口述给豆包：「我的电脑是苹果，要安装Claude Code和CC switch，还要把openrouter api key配置到cc switch，然后用上gpt gemini claude glm kimi minimax 六家模型！」 | 豆包输出完整安装命令 | 说明电脑系统（Mac/Win/Linux） |
| cc-switch模型切换 | 启动Claude Code前在cc-switch选API供应商 | 自动切换模型，无需手动改配置 | 同时支持Claude Code、CodeX、Gemini CLI |
| Skills社区查找 | 在Claude Code中运行：`读取下面网页里面所有的 Skills，当我给你提出我的需求之后，匹配最合适的，并且返回它的链接。https://github.com/anthropics/skills https://github.com/ComposioHQ/awesome-claude-skills` | 自动匹配社区现成Skills | 也可去 `https://skillsmp.com/` 手动浏览（共4911页） |
| skill-creator安装 | 在Claude Code运行：`安装这个skill，skill项目地址为: https://github.com/anthropics/skills/tree/main/skills/skill-creator` | 获得设计新技能的能力 | 中间弹出选择默认选yes |
| 自定义Skills生成 | 运行skill-creator后用自然语言描述需求，如：`使用skill-creator帮我设计一个Skill。这个Skill在我创建前端页面的时候，能够保留复杂度和美学，设计出一个非常有创造力、以文字表达和渐变色为主体的网页。我还需要加上一些纯CSS和HTML实现的动画，增加一些点缀色，使用更加出人意料的字体，并且实现一些简单的鼠标悬停交互效果。` | 生成定制Skills，热加载无需重启 | 纯自然语言输入即可 |
| OpenCode安装（Mac） | `curl -fsSL https://opencode.ai/install | bash` | 安装开源版Claude Code | Mac有三种安装命令，此命令最稳定 |
| OpenCode选免费模型 | 首次运行输入 `/model` | 选择免费模型 | 用免费模型安装oh-my-opencode |
| oh-my-opencode安装 | 在OpenCode界面运行：`按照这里的说明进行安装和配置 https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/README.md` | OpenCode获得完整功能 | 安装时间较长，可同时玩Claude Code等待 |
| oh-my-opencode配置问答 | 三个问题：有无Claude Pro/Max？有无GPT订阅？会用Gemini吗？按实际回答 | 自动配置对应模型权限 | 作者答案：No, Yes, Yes |
| OpenCode登录GPT | 新开命令行窗口运行：`opencode auth login` | 登录GPT账号 | 不能在OpenCode界面内运行，需新开窗口；无自动弹出浏览器则手动点链接 |
| Cursor安装 | 支付界面选美元 → 出现支付宝选项 | 支付宝订阅，免税，比银行卡便宜 | 补充Claude Code单文件调整能力 |

---

### 🛠️ 操作流程

1. **准备阶段 - 搞定API**
   - 注册OpenRouter账号：`https://openrouter.ai`
   - 充值选支付宝（选美元计价）
   - 新建API Key，复制保存
   - 可选：将已有OpenAI/Anthropic Key存入OpenRouter统一管理

2. **核心执行 - 安装主工具链**
   - 打开豆包助手（`https://doubao.com/bot/stIy6xcY`）
   - 输入：「我的电脑是[你的系统]，要安装Claude Code和CC switch，还要把openrouter api key配置到cc switch，然后用上gpt gemini claude glm kimi minimax 六家模型！」
   - 按豆包给出的命令逐步执行（不懂怎么开终端也可以问豆包）
   - 安装完成后打开cc-switch可视化界面，验证六家模型均可切换

3. **Skills配置**
   - 在Claude Code中运行社区Skills查找Prompt（见配置表）
   - 安装skill-creator：`安装这个skill，skill项目地址为: https://github.com/anthropics/skills/tree/main/skills/skill-creator`
   - 用自然语言让skill-creator生成定制Skills，中间弹窗默认选yes

4. **安装OpenCode（可选但推荐）**
   - 运行：`curl -fsSL https://opencode.ai/install | bash`
   - 首次运行输入 `/model` 选免费模型
   - 在OpenCode界面安装oh-my-opencode（见配置表）
   - 回答三个配置问题
   - 新开命令行窗口运行 `opencode auth login` 登录GPT

5. **安装Cursor（补充IDE）**
   - 官网下载Cursor，支付时选美元+支付宝

6. **验证与优化**
   - 确认三套工具均可正常启动
   - 分工：Claude Code处理整体项目，Cursor处理单文件，OpenCode处理模块和Bug
   - 开发前先把idea口述给豆包CC版，生成类似Claude Code Plan模式的提示语，节省API用量

---

### 💡 具体案例/数据

- 作者用中转API年底统计利用率仅30%，多平台充值导致资源浪费
- skillsmp.com上共有4911页Skills可浏览
- 全程豆包辅助安装，整套工具链约花半小时
- 社区热度第一的前端设计Skills可用以下Prompt复刻：「使用skill-creator帮我设计一个Skill。这个Skill在我创建前端页面的时候，能够保留复杂度和美学，设计出一个非常有创造力、以文字表达和渐变色为主体的网页。我还需要加上一些纯CSS和HTML实现的动画，增加一些点缀色，使用更加出人意料的字体，并且实现一些简单的鼠标悬停交互效果。」

---

### 📝 避坑指南

- ⚠️ opencode-antigravity-auth（反代薅Gemini Pro额度）近期封号率极高，明确不推荐，稳定方案用OpenRouter接Gemini
- ⚠️ `opencode auth login` 必须在新开的命令行窗口运行，不能在OpenCode界面内执行
- ⚠️ 如果auth login没有自动弹出浏览器，手动点击终端中显示的链接同样有效
- ⚠️ oh-my-opencode安装时间较长，不要以为卡住了，可以同时去玩Claude Code等待
- ⚠️ Mac安装OpenCode有三种命令，只用 `curl -fsSL https://opencode.ai/install | bash` 这一条，其余两种稳定性较差
- ⚠️ 中转API（1:10、1:20比例）价格波动大、利用率低，不建议作为主力方案

---

### 🏷️ 行业标签

#ClaudeCode #OpenCode #OpenRouter #cc-switch #Skills #豆包 #AI编程工具链 #本地部署 #支付宝付款 #无需国外银行卡

---

---
