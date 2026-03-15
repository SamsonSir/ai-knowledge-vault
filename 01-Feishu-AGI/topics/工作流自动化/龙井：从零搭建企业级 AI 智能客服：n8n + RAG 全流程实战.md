# 工作流自动化

## 14. [2026-02-04]

## 📘 文章 3


> 文档 ID: `Uq1qwtJNAikrHFkeyHfcQyvbnNg`

**来源**: 龙井：从零搭建企业级 AI 智能客服：n8n + RAG 全流程实战 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 用 n8n 从零搭建一套「知识库 + 多渠道 + 公网部署」的企业级智能客服，覆盖 RAG 全链路实战，7×24 小时无人值守。

**核心逻辑**:

- **Agent 四要素缺一不可**：LLM（大脑）+ Planning（决策，内置于 Agent 节点）+ Memory（短期记忆，上下文窗口）+ Tools（执行手，如搜索/知识库），缺任何一个都是残缺体。
- **系统提示词决定 Agent 人设**：DeepSeek 知道自己是 DeepSeek，是因为深度求索在系统提示词里写了约束。同理，你写什么角色，Agent 就是什么角色。
- **工具调用失败首选换模型，而非调高迭代次数**：Max Iterations 默认 10，调高不稳定；根本原因是模型兼容性，换 Gemini 或火山引擎模型可直接解决。
- **短期记忆有硬上限**：Context Window Length 默认 5（5 组问答），超出后最早的对话被挤出；重启对话后全部清空，无法持久化。
- **RAG 三步缺一不可**：向量化（Embedding 模型把文字转数字坐标）→ 相似度检索（余弦相似度，Pinecone 返回最近 N 个片段）→ 上下文注入（资料 + 问题打包发给 LLM）。
- **Embedding 模型必须前后一致**：存入时用 `gemini-embedding-001`，检索时必须也用 `gemini-embedding-001`，否则向量对不上，检索结果为空或乱。
- **Dimension 维度值不用查文档，跑错误反推**：先填默认值跑一遍，报错信息会直接告诉你正确的维度（如 768 → 报错 → 改 3072）。
- **两条工作流必须拆分**：「管理员存数据」（一次性/有新资料时运行）和「客服取数据」（24 小时实时运行）放在同一画布只适合演示，生产环境必须拆开。
- **内网穿透是本地部署公网化的关键**：Ngrok 是主流方案，ngrok 命令行窗口必须保持运行，域名可能变化需重新配置，可申请静态域名规避。
- **Gmail OAuth 登录必须通过 Ngrok 域名访问 n8n 后台**：用 `localhost:5678` 登录会报错，必须用 `recreantly-catechistic-makeda.ngrok-free.dev` 这类 Ngrok 域名访问后台再做授权。
- **n8n 适合邮件场景，国内 IM 平台（飞书/微信/企业微信）推荐用 Coze**：n8n 接国内平台配置繁琐，Coze 对这些平台开箱即用。

---

### 🎯 关键洞察

**RAG 执行链路完整拆解**（以「有什么分类体系」为例）：

1. Chat Trigger 接收用户输入，打包发给 Agent
2. Agent 读取 System Message，判断问题类型 → 属于电商内部知识 → 决策调用向量库工具
3. Gemini Embedding 把问题转为数字向量（如 `[0.12, -0.98, 0.55...]`）
4. Pinecone 用余弦相似度检索，返回 Limit=4 个最相关片段
5. 工具侧的 DeepSeek 把 4 段零散文字整理成干净文本，返回给 Agent
6. Agent（主 DeepSeek）结合电商客服人设，组织语言输出最终回复

**工具选择策略**（系统提示词中明确分工）：
- 内部问题（退换货/运费/产品参数/售后）→ 优先查向量库
- 外部问题（市场价格对比/竞品/行业新闻/实时汇率）→ 才用 SerpAPI
- 两者都查不到 → 告知用户并建议转人工

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Agent 节点 | 默认创建即可，挂载 LLM + Memory + Tools | 智能调度核心 | Max Iterations 默认 10，工具调用失败先换模型 |
| LLM 参数 | Temperature（创意度）、Max Tokens（长度限制）、Top P、Frequency Penalty、Presence Penalty | 控制回答风格和长度 | 无特殊需求保持默认 |
| Short-term Memory | Context Window Length = 5 | 记住最近 5 组问答 | 重启对话后清空，无法持久化 |
| Pinecone 向量库 | 创建 Index，选向量模型，填 Dimension | 存储文档向量 | Dimension 填错会报错，从报错信息反推正确值 |
| Embedding 模型 | gemini-embedding-001（需 Google API，90天免费） | 文字 → 数字向量 | 存入和检索必须用同一个模型 |
| 文件上传表单 | Accepted File Types: `.pdf, .doc, .docx, .xls, .xlsx, .csv`（英文逗号） | 支持多格式上传 | 逗号必须英文，否则格式识别失败 |
| Pinecone 检索 | Limit = 4 | 返回最相关 4 个片段 | 值太小可能漏掉关键信息，太大增加 token 消耗 |
| Ngrok 内网穿透 | `.\ngrok.exe config add-authtoken <令牌>`（只需一次）<br>`.\ngrok.exe http 5678` | 本地 n8n 公网可访问 | 命令行窗口不能关；域名可能变化；可申请静态域名 |
| docker-compose 公网配置 | 见下方代码块 | n8n 通过 Ngrok 域名对外提供服务 | 域名变化后需重新修改并 `docker-compose up -d` |
| Gmail 触发 | 每隔 1 分钟轮询收件箱 | 自动读取新邮件 | OAuth 授权必须通过 Ngrok 域名访问 n8n 后台 |
| 邮件回复节点 | 通过 Message ID 回复 | 精准回复对应邮件线程 | 确保 Gmail API 已启用，OAuth 权限全选（14个） |

---

### 🛠️ 操作流程

#### 第一部分：基础 Agent 搭建

1. **新建 Agent 节点** → 系统自动生成默认配置
2. **挂载 LLM**：添加大模型节点 → 配置 API 凭证 → 选择模型型号（如 DeepSeek）
3. **写系统提示词**（示例）：
   ```
   你是一个专业的科技行业分析师，你的风格简洁、犀利，擅长从冗长的新闻中提炼核心价值。
   请始终使用中文回答。
   ```
4. **添加工具**（以 Google Search 为例）：添加 SerpAPI 节点 → 配置 API 凭证 → 挂载到 Agent
5. **添加短期记忆**：添加 Memory 节点 → 设置 Context Window Length（默认 5）

#### 第二部分：RAG 知识库搭建

1. **准备阶段**：
   - 申请 Pinecone 账号，创建项目，获取 API Key
   - 申请 Google Gemini API（90天免费）
   - 在 Pinecone 创建 Index，选择 `gemini-embedding-001` 向量模型
   - Dimension 先填默认值，跑一遍报错后从错误信息获取正确值（如 3072）

2. **存数据工作流**：
   - 新建表单节点，设置 Accepted File Types: `.pdf, .doc, .docx, .xls, .xlsx, .csv`
   - 添加 Pinecone Vector Store 节点（上传模式）
   - 挂载 `gemini-embedding-001` Embedding 模型
   - 配置 Default Data Loader（文件加载器）
   - 运行测试，确认文件被分片上传（如「上传了15份」）

3. **问答工作流**：
   - 新建 Agent 节点，挂载 DeepSeek 作为主 LLM
   - 添加 Vector Store Tool，选择 Pinecone，挂载**同一个** `gemini-embedding-001`
   - 设置 Limit = 4（检索返回片段数）
   - 写系统提示词（见下方完整提示词）
   - 添加 Simple Memory 节点

4. **系统提示词（完整版）**：
   ```
   你是一个专业的电商智能客服助手。你的目标是利用手头的工具，准确、礼貌地回答客户的问题。

   请遵循以下【工具使用策略】：

   1. **优先查询内部知识库 (Answer questions with a vector store)**：
      - 当用户询问关于"退换货政策"、"运费"、"店铺具体产品参数"、"售后规则"或"常见问题"时，**必须**首先使用此工具查询。
      - 依据知识库返回的内容回答，不要编造内部政策。

   2. **补充使用联网搜索 (SerpAPI)**：
      - 只有当知识库中没有相关信息，或者用户询问的是"当前市场价格对比"、"竞争对手产品"、"最新的行业新闻"或"实时汇率"等外部信息时，才使用 SerpAPI。

   3. **回答规范**：
      - 始终使用中文回答。
      - 语气亲切、专业。
      - 如果两个工具都找不到答案，请诚实地告诉用户你暂时无法获取该信息，并建议转接人工。

   请根据用户的提问，智能选择最合适的工具。
   ```

#### 第三部分：公网部署（Ngrok 内网穿透）

1. **下载 Ngrok**：`https://ngrok.com/download/windows`，解压到本地目录
2. **获取 Authtoken**：登录 Ngrok 官网 → 复制 Authtoken
3. **注册令牌**（只需一次）：
   ```cmd
   .\ngrok.exe config add-authtoken <你的令牌>
   ```
4. **启动穿透**（保持窗口运行）：
   ```cmd
   .\ngrok.exe http 5678
   ```
5. **修改 docker-compose.yml**，在 `environment:` 下添加：
   ```yaml
   - N8N_EDITOR_BASE_URL=https://recreantly-catechistic-makeda.ngrok-free.dev/
   - WEBHOOK_URL=https://recreantly-catechistic-makeda.ngrok-free.dev/
   ```
6. **完整 docker-compose.yml**：
   ```yaml
   services:
     n8n:
       image: docker.n8n.io/n8nio/n8n:latest
       container_name: n8n
       restart: unless-stopped
       ports:
         - "5678:5678"
       environment:
         - TZ=Asia/Shanghai
         - GENERIC_TIMEZONE=Asia/Shanghai
         - N8N_LOG_LEVEL=info
         - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false
         - N8N_EDITOR_BASE_URL=https://recreantly-catechistic-makeda.ngrok-free.dev/
         - WEBHOOK_URL=https://recreantly-catechistic-makeda.ngrok-free.dev/
       volumes:
         - ./n8n_data:/home/node/.n8n
         - ./n8n_files:/home/node/files
   ```
7. **重启 n8n**：
   ```bash
   docker-compose up -d
   ```
8. **docker run 方式**（停旧容器 → 删旧容器 → 重新启动）：
   ```bash
   docker stop <容器ID或名称>
   docker rm <容器ID或名称>
   docker run -d \
     --name n8n \
     -p 5678:5678 \
     -e N8N_EDITOR_BASE_URL=https://recreantly-catechistic-makeda.ngrok-free.dev/ \
     -e WEBHOOK_URL=https://recreantly-catechistic-makeda.ngrok-free.dev/ \
     -v ~/.n8n:/home/node/.n8n \
     docker.n8n.io/n8nio/n8n
   ```

#### 第四部分：接入 Gmail 自动回复

1. **新建邮件工作流**，复制电商客服 Agent 节点过去，删除 Chat Trigger
2. **添加 Gmail Trigger**（收到邮件后触发），轮询间隔设为 1 分钟
3. **配置 Gmail OAuth**：
   - 进入谷歌云平台：`https://console.cloud.google.com/`
   - 创建新项目 → 搜索并启用 Gmail API
   - 配置 OAuth 同意屏幕（填写智能客服接入的邮箱，保持一致）
   - 创建 OAuth 客户端，重定向 URI 填写 Ngrok 域名（从 n8n 凭证配置页复制）
   - 设置数据访问范围：搜索 Gmail API，全选 14 个权限 → 更新 → 保存
   - 回到 n8n，填入客户端 ID 和客户端密钥 → 保存 → 点击登录授权
   - ⚠️ 授权时必须通过 Ngrok 域名访问 n8n 后台，不能用 localhost:5678
4. **配置 Agent 节点**：将邮件内容（发件人、主题、正文）注入到 User Message 和 Session ID
5. **添加 Gmail Reply 节点**：通过 Message ID 回复对应邮件线程
6. **保存 → 发布（Activate）**

---

### 💡 具体案例/数据

- 文件上传后被分成 **15 个片段**存入 Pinecone（实测数据）
- Pinecone 检索 Limit 设置为 **4**，返回 4 个最相关片段
- Context Window Length 默认 **5**（5 组问答）
- Max Iterations 默认 **10**，调高到 20/30 不稳定
- Gemini Embedding 维度：填 768 报错，正确值为 **3072**（从报错信息反推）
- Gmail API 权限范围：共 **14 个**，需全选
- n8n 版本要求：**高于 1.19** 才支持 n8n Chat 发布功能

---

### 📝 避坑指南

- ⚠️ **工具调用失败不要调高 Max Iterations**，优先换模型（Gemini 或火山引擎），根本原因是模型兼容性
- ⚠️ **Embedding 模型必须前后一致**：存入用什么模型，检索就用什么模型，否则向量对不上
- ⚠️ **Dimension 维度值不用查文档**：先填默认值跑一遍，从报错信息直接获取正确值
- ⚠️ **Gmail OAuth 授权必须通过 Ngrok 域名访问 n8n 后台**，用 localhost:5678 会报错
- ⚠️ **Ngrok 命令行窗口不能关闭**，关闭后公网访问立即失效
- ⚠️ **Ngrok 免费域名可能变化**，变化后需重新修改 docker-compose.yml 并重启 n8n；可申请静态域名规避
- ⚠️ **表单 Accepted File Types 必须用英文逗号**：`.pdf, .doc, .docx, .xls, .xlsx, .csv`
- ⚠️ **生产环境必须拆分两条工作流**：存数据和问答放同一画布只适合演示
- ⚠️ **n8n Chat 发布功能要求版本 > 1.19**，低版本需升级
- ⚠️ **国内 IM 平台（飞书/微信/企业微信）不推荐用 n8n**，改用 Coze，开箱即用

---

### 🏷️ 行业标签
#n8n #RAG #智能客服 #Agent #向量数据库 #Pinecone #Embedding #内网穿透 #Ngrok #Gmail自动化 #LLM #工作流自动化

---

---
