# Agent与技能系统

## 110. [2026-03-08]

## 📘 文章 3


> 文档 ID: `LXkWw0cGQizxwbkGyhXcBN3Znee`

**来源**: 小白必看！彻底终结 OpenClaw 安装难的问题 🦞 | **时间**: 2026-03-08 | **原文链接**: https://mp.weixin.qq.com/s/1pl5HqLH...

---

### 📋 核心分析

**战略价值**: 通过「Cherry Studio 一键自动化安装」+「AI Agent 全自驱安装」双保险组合，将 OpenClaw 安装成功率提升至 99.99%，彻底消除 Windows/Mac 用户的命令行恐惧。

**核心逻辑**:

- **两套方案分层兜底**：方案一是 Cherry Studio 图形化一键安装（覆盖 80% 用户），方案二是 AI Agent 全自驱安装（覆盖剩余 20% 遇到异常的用户），两套组合拳串联使用。
- **Cherry Studio 是国产开源工具**，无隐私泄露风险，下载地址：https://www.cherry-ai.com/download，支持 Mac 和 Windows，安装后需在右上角设置中配置模型 API KEY。
- **Cherry Studio 内置 OpenClaw 安装引导**：配置好 API KEY 后，点击界面中的「+」号 → 选择 OpenClaw → 点击「安装 OpenClaw」→ 全程跟随图形引导点击执行，安装完成后下拉选择模型并点击「启动」即可。
- **AI Agent 方案的触发条件**：Cherry Studio 自动安装失败、本机有残留 OpenClaw 文件、或首次安装遇到系统差异报错时，切换至 AI Agent 方案。
- **AI Agent 配置关键点**：在 Cherry Studio 左上角「添加助手」→「添加 Agent」，选择已配置好的模型，并将权限模式设置为「全自动模式」，这是 AI 能自驱解决所有问题的前提。
- **系统提示词是 AI 自驱的核心**：将下方完整提示词粘贴给 Agent 后，AI 会自动询问模型选择 → 收集 API Key → 检查环境 → 安装 → 配置 → 验证，全流程无需人工干预。
- **卸载重装逻辑**：AI 检测到本机已有 OpenClaw（包括安装失败的残留文件）时，会主动询问是否卸载重装，选「是」即可清理重来。
- **阿里百炼需手动配置**：阿里百炼不走 `openclaw onboard` 向导，需手动写入 `~/.openclaw/openclaw.json`，配置模板见下方附录。
- **卸载前必须切换目录**：执行卸载命令前必须先 `cd ~`，否则因当前目录被删除会报 `ENOENT: uv_cwd` 错误。
- **安装完成后的验证路径**：运行 `openclaw auth token` 获取 token，完整访问地址为 `https://localhost:18789/chat?token=xxx`，也可通过 `openclaw dashboard` 直接打开浏览器面板。

---

### 🛠️ 操作流程

**方案一：Cherry Studio 一键安装（推荐先试）**

1. 下载安装 Cherry Studio：https://www.cherry-ai.com/download，选择对应系统版本
2. 打开 Cherry Studio → 右上角「设置」→ 配置模型 API KEY
3. 点击界面「+」号 → 选择 OpenClaw
4. 点击「安装 OpenClaw」→ 全程跟随图形引导执行
5. 安装完成后下拉选择模型 → 点击「启动」→ 看到控制台页面即成功

**方案二：AI Agent 全自驱安装（方案一失败时使用）**

1. Cherry Studio 左上角「添加助手」→「添加 Agent」
2. 选择已配置好的模型，权限模式设为「全自动模式」
3. 将下方完整系统提示词粘贴给 Agent
4. AI 自动引导：选择模型提供商（A/B/C）→ 提供 API Key → AI 全自动完成安装配置
5. 安装完成后浏览器访问 `https://localhost:18789/chat?token=xxx`

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| macOS/Linux 安装命令 | `curl -fsSL https://openclaw.ai/install.sh \| bash` | 自动安装 OpenClaw | 需 Node.js ≥ 22 |
| Windows 安装命令 | `iwr -useb https://openclaw.ai/install.ps1 \| iex` | 自动安装 OpenClaw | 需 Node.js ≥ 22 |
| 备选安装（镜像源） | `npm install -g openclaw@latest --registry=https://registry.npmmirror.com` | 国内网络备用 | 网络异常时使用 |
| 智谱 GLM 配置 | `openclaw onboard --install-daemon` → 选 Z.AI → 粘贴 Key → 选 Coding-Plan-CN → 默认模型 `zai/glm-5` | 向导式配置 | 按顺序选择 |
| 字节火山引擎配置 | `openclaw onboard --install-daemon` → 选 Volcano Engine → 粘贴 Key → 选 `volcengine-plan/ark-code-latest` | 向导式配置 | 按顺序选择 |
| 阿里百炼配置 | 跳过向导，手动写 `~/.openclaw/openclaw.json`（见附录） | 手动配置 | 不支持向导，必须手动写文件 |
| 查看网关状态 | `openclaw status` | 确认服务运行 | — |
| 打开浏览器面板 | `openclaw dashboard` | 图形化界面 | — |
| 获取访问 token | `openclaw auth token` | 得到登录 token | 拼接到访问地址后 |

---

### 📝 AI Agent 系统提示词（完整版）

```
# 角色定义
你是 OpenClaw 安装助手，帮用户自动完成安装配置。用户是小白，只询问必要信息（模型选择、API Key），其余自动处理。

---

# 核心流程

## 1. 收集信息
询问用户选择模型提供商：A.智谱GLM / B.阿里百炼 / C.字节火山引擎
引导用户获取并提供 API Key

## 2. 环境检查
- 确保 Node.js ≥ 22，否则自动安装/升级
- 通过多种方式（npm、which）等检查本机是否已经有安装 OpenClaw，如已有 OpenClaw，询问用户是否卸载重装

## 3. 安装
- macOS/Linux: `curl -fsSL https://openclaw.ai/install.sh | bash`
- Windows: `iwr -useb https://openclaw.ai/install.ps1 | iex`
- 备选: `npm install -g openclaw@latest --registry=https://registry.npmmirror.com`

## 4. 配置
运行 `openclaw onboard --install-daemon`，根据用户选择的提供商配置：
- 智谱: 选 Z.AI → 粘贴 API Key → 选 Coding-Plan-CN → 默认模型 zai/glm-5
- 字节: 选 Volcano Engine → 粘贴 API Key → 选 volcengine-plan/ark-code-latest
- 阿里: 跳过向导，手动配置 ~/.openclaw/openclaw.json（见附录）

## 5. 验证
- 将 openclaw 命令设置为全局命令
- 查看网关状态：`openclaw status`
- 打开浏览器面板：`openclaw dashboard`
- 运行 `openclaw auth token` 获取 token
- 提供完整访问地址: https://localhost:18789/chat?token=xxx

---

# 关键注意事项

⚠️ 卸载前必须先切换目录
如果需要卸载旧版本，先执行 `cd ~`，再执行卸载命令。否则会因当前目录被删除而报错 `ENOENT: uv_cwd`。

⚠️ 阿里百炼配置
使用 OpenAI 兼容模式，Base URL: `https://coding.dashscope.aliyuncs.com/v1`，配置文件模板见附录。

---

# 附录

## 阿里百炼配置模板 (~/.openclaw/openclaw.json)
将 <API_KEY> 替换为用户的实际 Key：

{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "<API_KEY>",
        "api": "openai-completions",
        "models": [
          {"id": "qwen3.5-plus", "name": "qwen3.5-plus", "reasoning": false, "input": ["text", "image"], "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}, "contextWindow": 1000000, "maxTokens": 65536},
          {"id": "glm-5", "name": "glm-5", "reasoning": false, "input": ["text"], "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}, "contextWindow": 202752, "maxTokens": 16384}
        ]
      }
    }
  },
  "agents": {"defaults": {"model": {"primary": "bailian/qwen3.5-plus"}, "models": {"bailian/qwen3.5-plus": {}, "bailian/glm-5": {}}}},
  "gateway": {"mode": "local"}
}

## 参考文档链接
- OpenClaw 官方文档：https://docs.openclaw.ai/start/getting-started
- OpenClaw GitHub：https://github.com/openclaw/openclaw
- 智谱 GLM 对接文档：https://docs.bigmodel.cn/cn/coding-plan/tool/openclaw
- 字节火山引擎对接文档：https://www.volcengine.com/docs/82379/2183190
- 阿里百炼文档：https://bailian.console.aliyun.com/cn-beijing/?tab=doc#/doc/?type=model&url=3023085
```

---

### 📝 避坑指南

- ⚠️ **卸载必须先 `cd ~`**：卸载旧版前不切目录，会报 `ENOENT: uv_cwd`，因为当前目录被删除导致路径失效。
- ⚠️ **Node.js 版本必须 ≥ 22**：低版本会导致安装失败，AI Agent 会自动检测并升级，手动安装需自行确认版本。
- ⚠️ **阿里百炼不走向导**：不能用 `openclaw onboard` 配置阿里百炼，必须手动写 `~/.openclaw/openclaw.json`，Base URL 为 `https://coding.dashscope.aliyuncs.com/v1`。
- ⚠️ **AI Agent 必须开「全自动模式」**：不开全自动模式，AI 无法自主执行命令，只会给建议而不会实际操作。
- ⚠️ **安装失败有残留文件**：Cherry Studio 自动安装失败后本地可能有残留，切换 AI Agent 方案时直接选「卸载重装」清理干净再装。
- ⚠️ **AI 能力上限决定复杂问题的解决率**：极端复杂的系统问题需要配置能力更强的模型，并持续与 Agent 对话调试。

---

### 🏷️ 行业标签

#OpenClaw #AI编程助手 #自动化安装 #CherryStudio #AIAgent #小龙虾 #开发工具 #Windows安装 #Mac安装

---

---
