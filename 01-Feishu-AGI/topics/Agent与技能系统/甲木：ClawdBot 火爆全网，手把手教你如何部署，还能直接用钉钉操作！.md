# Agent与技能系统

## 35. [2026-01-28]

## 📙 文章 4


> 文档 ID: `HCAPwVnVciK1UgkHBnKc3hcWnLd`

**来源**: 甲木：ClawdBot 火爆全网，手把手教你如何部署，还能直接用钉钉操作！ | **时间**: 2026-01-28 | **原文链接**: `https://mp.weixin.qq.com/s/Xr6bbxaA...`

---

### 📋 核心分析

**战略价值**: Moltbot（原 ClawdBot）是一个开源可自托管的本地 Agent，通过阿里云 + 百炼 + 钉钉生态实现国内可用的「私人 Jarvis」闭环，无需翻墙拼积木。

**核心逻辑**:

- **为什么火**：把 AI 交互入口搬进"消息"（像发微信一样下指令），且具备长期在线执行能力，而非一次性对话。
- **执行型闭环**：能连接 GitHub、网盘、邮箱、日历等生产力工具，形成「指令 → 执行 → 结果」完整链路，而非只输出文字。
- **记忆 + 主动 + 持续**：三个关键能力叠加，让它区别于普通 chatbot，更接近"数字员工"。
- **GitHub Star 暴涨至 64k**，增长仅用数天，验证了市场对"私人 AI 助理"的强烈需求。
- **命名变更**：已从 ClawdBot 改名 Moltbot，GitHub 地址：`https://github.com/clawdbot/clawdbot`
- **安全隔离是前提**：Moltbot 拥有极高的本地权限（文件系统、工具链调用），必须部署在隔离设备或云服务器，严禁装在主力机上，否则存在误删文件、误触发费用风险。
- **国内适配核心问题**：原生支持的都是海外软件（Telegram、iMessage 等），国内用户需要通过阿里云 AppFlow + 钉钉机器人完成通道替换。
- **阿里云方案解决三个痛点**：① 服务器长期在线隔离；② 预装 Moltbot 镜像，免手动配置依赖；③ 内置百炼平台，直接选模型调用，无需科学上网。
- **钉钉打通的意义**：将「模型 + 部署 + 消息通道 + 协同入口」全部收进同一生态，实现手机遥控 AI 干活的完整闭环。
- **AppFlow 是关键中间层**：它作为 Moltbot API 与钉钉机器人之间的桥接，目前仅支持 HTTP 模式（Stream 模式无法返回消息）。

---

### 🛠️ 操作流程

#### 第一步：购买 Moltbot 云服务器

1. 登录阿里云：`https://account.aliyun.com/`
2. 直接访问 Moltbot 专属购买链接：
   `https://swasnext.console.aliyun.com/buy?spm=a2c4g.11186623.0.0.44b74febS5Oq2Y&regionId=us-east-1&planId=swas.s.c2m2s40b1.linux&imageId=bd45493af84846deb5dcd3fca6c1a1d9&amount=1&duration=12&autoRenew=false#/`
3. 确认以下配置（默认已预设）：

| 配置项 | 值 |
|--------|-----|
| 实例规格族 | 通用型 |
| vCPU | 2vCPU |
| 内存 | 2GiB |
| 镜像 | 应用镜像 - Moltbot |
| 地域 | 美国（弗吉尼亚） |
| 数量 | 1 |

4. 选择时长（1个月或1年），按需开启自动续费，点击「立即购买」完成支付。
5. 支付成功后点击「管理控制台」，记录服务器页面备用。

---

#### 第二步：配置 Moltbot（绑定百炼 API Key + 生成 Token）

**2.1 获取百炼 API Key**

1. 打开百炼大模型平台：
   `https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.44b74febS5Oq2Y&tab=model#/model-market`
2. 点击「密钥管理」：
   `https://bailian.console.aliyun.com/?tab=model#/api-key`
3. 点击「创建 API-Key」，复制生成的 Key 保存备用。
4. ⚠️ API Key 泄露会导致第三方冒用身份，产生超出预期的 Token 费用。

**2.2 在服务器控制台配置**

1. 访问服务器列表：`https://swasnext.console.aliyun.com/servers`
2. 点击实例 ID → 进入「服务器概览」→ 点击「应用详情」页签。
3. **端口放通**：点击「一键放通」，开放对应防火墙端口。
4. **配置百炼 API Key**：点击「一键配置」→ 输入百炼 API Key → 点击「执行命令」写入。
5. **生成 Moltbot Token**：点击「执行命令」，生成访问 Token，**立即保存该 Token**（后续 AppFlow 配置必用）。
6. 点击「打开网站页面」，进入 Moltbot 对话页面，可先测试对话。

**2.3 开启 ResponseAPI（为后续 AppFlow 调用预留接口）**

路径：Moltbot 页面左侧导航栏 → `Setting > Config` → 左侧点击 `Gateway` → 切换至 `Http` 页签 → 在 `Responses` 区域将 `Enabled` 切换为开启 → 点击 `Save`。

---

#### 第三步：集成钉钉

**3.1 创建钉钉应用**

1. 确保钉钉账号有开发者权限，获取方式：`https://open.dingtalk.com/document/orgapp/obtain-developer-permissions`
2. 访问钉钉开放平台：`https://open-dev.dingtalk.com/`
3. 左侧导航栏 → 「钉钉应用」→ 右上角「创建应用」。
4. 填写应用名称、描述，上传图标，点击「保存」。
5. 左侧菜单 → 「凭证与基础信息」，复制 **Client ID** 和 **Client Secret** 备用。

**3.2 创建消息卡片模板**

1. 访问卡片平台：`https://open-dev.dingtalk.com/fe/card`
2. 点击「新建模板」，填写：

| 字段 | 值 |
|------|-----|
| 卡片类型 | 消息卡片 |
| 卡片模板场景 | AI 卡片 |
| 关联应用 | Clawdbot（刚创建的应用） |

3. 进入模拟编辑页面后，**不要使用预设模板**，不做任何操作，直接「保存」→「发布」→「返回」模板列表。
4. 复制**模板 ID** 备用。

**3.3 授予应用卡片消息权限**

1. 访问应用列表：`https://open-dev.dingtalk.com/fe/app`，进入刚创建的应用。
2. 左侧菜单 → 「开发配置 > 权限管理」。
3. 搜索框输入 `Card.Streaming.Write`，点击「申请权限」。
4. 再次搜索 `Card.Instance.Write`，点击「申请权限」。
5. ⚠️ 两个权限必须**分别单独申请**，批量选择有 bug。

**3.4 创建 AppFlow 连接流**

1. 使用模板直接创建：
   `https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/tl-81856c0550684f50929b`
2. 点击「立即使用」，进入配置向导：

| 步骤 | 操作 |
|------|------|
| Moltbot 账户授权 | 点击「添加新凭证」，输入第二步生成的 **Moltbot Token** |
| 钉钉账户授权 | 点击「添加新凭证」，填入 **Client ID**、**Client Secret**，设置凭证名称 |
| 执行动作配置 | 填写**模型名称**、**公网地址**（服务器 IP）、**模板 ID** |
| 基本信息 | 填写连接流名称和描述（建议保持默认） |

3. 配置完成后，复制生成的 **WebhookUrl**，点击「发布」。
4. ⚠️ WebhookUrl 必须立即复制保存，后续配置机器人必用。

**3.5 配置钉钉机器人**

1. 访问应用列表：`https://open-dev.dingtalk.com/fe/app`，进入目标应用。
2. 「添加应用能力」→ 找到「机器人」卡片 → 点击「添加」。
3. 打开「机器人配置」开关，填写机器人简介和描述（内容随意）。
4. **消息接收模式**：选择 **HTTP 模式**（⚠️ 不能选 Stream 模式，否则无法返回消息）。
5. **消息接收地址**：填入上一步的 **WebhookUrl**。
6. 点击「发布」。

**3.6 发布应用版本**

1. 左侧导航栏 → 「版本管理与发布」→「创建新版本」。
2. 填写版本号、版本描述，选择**应用可见范围**，点击「保存」→ 弹窗中点击「直接发布」。

**3.7 在钉钉群中添加并测试机器人**

1. 进入钉钉群 → 「群设置」→「机器人」→「添加机器人」。
2. 搜索刚创建的机器人名称，选中后点击「添加」→「完成添加」。
3. 在群中 @ 机器人发送消息，验证是否正常返回 AI 卡片响应。

---

### 📦 配置/工具详表

| 模块 | 关键设置 | 预期效果 | 注意事项/坑 |
|------|---------|---------|-----------|
| 阿里云轻量服务器 | 2vCPU/2GiB，Moltbot 镜像，美国弗吉尼亚 | 长期在线隔离运行 Moltbot | 不要装在主力机，高权限有误操作风险 |
| 百炼 API Key | 密钥管理页面创建，写入服务器 | 驱动 Moltbot 调用大模型 | Key 泄露会产生超预期 Token 费用 |
| Moltbot Token | 服务器应用详情页「执行命令」生成 | AppFlow 鉴权凭据 | 含 Token 的完整 URL 泄露 = 管理员权限泄露 |
| ResponseAPI | Setting > Config > Gateway > Http > Responses > Enabled | 开放 API 接口供 AppFlow 调用 | 不开启则 AppFlow 无法访问 Moltbot |
| 钉钉卡片模板 | 类型：消息卡片，场景：AI 卡片，不用预设模板 | 支持流式返回结果展示 | 进编辑页后直接保存发布，不要改模板内容 |
| 钉钉权限 | Card.Streaming.Write + Card.Instance.Write | 允许应用发送卡片消息 | 必须分别单独申请，批量有 bug |
| AppFlow 连接流 | 填入 Token、Client ID/Secret、模型名、公网地址、模板 ID | 桥接 Moltbot 与钉钉机器人 | 发布前必须复制 WebhookUrl |
| 钉钉机器人消息模式 | HTTP 模式 | 正常接收并返回消息 | Stream 模式会导致无法返回消息 |

---

### 📝 避坑指南

- ⚠️ **不要把 Moltbot 装在主力机**：它拥有文件系统和工具链的高权限执行能力，误操作风险真实存在，务必用隔离设备或云服务器。
- ⚠️ **百炼 API Key 妥善保管**：泄露后第三方可冒用身份调用模型，产生超预期费用。
- ⚠️ **含 Token 的完整 URL 不能泄露**：任何持有该链接的人可直接绕过登录，获得 Moltbot 管理员权限。
- ⚠️ **钉钉两个权限必须分别申请**：`Card.Streaming.Write` 和 `Card.Instance.Write` 批量选择有 bug，需单独逐个申请。
- ⚠️ **机器人消息接收模式必须选 HTTP**：AppFlow 目前仅支持 HTTP 模式，选 Stream 模式会导致消息无法返回。
- ⚠️ **卡片模板编辑页不要动预设模板**：进入编辑页后直接保存发布即可，修改模板内容可能导致异常。
- ⚠️ **WebhookUrl 在 AppFlow 发布前必须复制**：这是配置钉钉机器人消息接收地址的唯一凭据。
- ⚠️ **百炼 Token 费用独立计费**：购买服务器的费用不包含模型调用费用，Token 消耗单独计算。

---

### 🏷️ 行业标签
#Moltbot #ClawdBot #AI助理 #自托管Agent #阿里云 #百炼 #钉钉集成 #AppFlow #开源AI #国内部署

---

---
