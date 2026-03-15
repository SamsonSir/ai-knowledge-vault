# Agent与技能系统

## 93. [2026-03-03]

## 📓 文章 6


> 文档 ID: `Yph1wLHJSi9ofLkUWPvcf1KunWf`

**来源**: 给OpenClaw开天眼！解决了10个跨境电商网站爬虫难题 | **时间**: 2026-03-03 | **原文链接**: `https://mp.weixin.qq.com/s/ng_0-mad...`

---

### 📋 核心分析

**战略价值**: 用 OpenClaw + 现成 Skill 打通 Reddit/Amazon/YouTube/TikTok/Twitter/GitHub 等10个跨境高频场景的数据采集链路，从安装到 Prompt 模板全程可复刻。

**核心逻辑**:

- **Reddit 免费路线**：`reddit-readonly` Skill 直打 `old.reddit.com` 的公开 `.json` 接口，无需 API Key，支持读热帖、搜帖子、读评论串。安装地址：`https://lobehub.com/skills/openclaw-skills-reddit-scraper`，ClawHub 镜像：`https://clawhub.ai/buksan1950/reddit-readonly`
- **Reddit 结构化路线**：Decodo OpenClaw Skill 提供 `reddit_post` + `reddit_subreddit` 两个工具，返回干净 JSON，后端自带 IP 轮换，稳定性高于免费路线。地址：`https://github.com/Decodo/decodo-openclaw-skill`
- **Amazon 反爬绕过**：同用 Decodo Skill，内置 `amazon`（单品页解析）和 `amazon_search`（关键词批量搜索），自动维护 CSS Selector，返回字段：价格、评分、评论数、ASIN、Best Seller 标志、卖家信息。
- **YouTube 字幕提取**：Decodo Skill 内置 `youtube_subtitles`，输入视频 ID 直接返回完整字幕文本，无需 YouTube API。工作流：`google_search` 找视频 ID → `youtube_subtitles` 拿字幕 → AI 提炼卖点和痛点。
- **TikTok / B站 视频**：用 Agent-Reach 项目内置的 `yt-dlp`（148K Stars），YouTube 和 B站通吃。一句话安装全套工具（含小红书、Reddit）：`帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md`，AI 自动读文档配置。项目地址：`https://github.com/Panniantong/agent-reach`
- **Twitter/X 免费读取**：用浏览器扩展（Cookie-Editor 或 Get cookies.txt LOCALLY）导出 Twitter Cookie，配置到 Agent-Reach 内置的 xreach：`agent-reach configure twitter-cookies "此处粘贴你复制的Cookie内容"`。⚠️ Cookie 有效期 7-30 天，需定期重新导出。
- **GitHub 竞品情报**：Agent-Reach 内置 `gh CLI`，先 `brew install gh` 安装，再 `gh auth login` 授权，让 OpenClaw 直接搜仓库、读 Issue、分析 Star 增长趋势，Issue 区 = 免费竞品缺陷报告。
- **动态 SPA 网站**：两个工具按场景选择——`playwright-npx`（AI 写脚本 + CSS 选择器，跑通后适合持续执行）；`browser-use`（视觉模式，AI 像人一样点选，Token 消耗大，适合未知结构网站）。遇 Cloudflare 换 `stealth-browser` Skill（底层 playwright-extra，模拟 User-Agent、WebGL 指纹、Timezone）。不想本地装 Chromium 用 Firecrawl Skill（远程沙盒，返回干净 Markdown，免费额度 500 次，加 `cache: 2d` 避免重复消耗）。安装 playwright-npx：`https://playbooks.com/skills/openclaw/skills/playwright-npx`
- **搜索工具三选**：Tavily（国内直连，无需海外信用卡，免费额度够个人用）；Brave Search（数据质量更高，需海外信用卡）；Exa（意图型研究查询，如"找真实买家写的独立评测"）。安装 Brave Search：`访问 https://clawhub.ai/steipete/brave-search 把这个skill安装到你文件夹下，然后配置api key是BSAl2YP5xxxxx`
- **Apify 工业级爬虫**：20年网页抓取积累，海量现成 Actor 覆盖 Google Maps、YouTube、Instagram、TikTok、Amazon。新建 API Key：`https://console.apify.com/account/integrations`，安装：`访问 https://github.com/apify/agent-skills，安装apify skills用于数据抓取api key是apify_api_5kIYzpxxxx`

---

### 🎯 关键洞察

**搜索策略**：多条窄查询远比一条宽查询有效。与其搜一次"蓝牙耳机市场分析"，不如分三次：
1. `bluetooth earbuds under 30 site:reddit.com complaints 2025`
2. `bluetooth earbuds amazon best seller negative reviews`
3. `bluetooth earbuds temu competitor comparison`

三次结果合并，质量差距极大。

**工具选型逻辑**：Playwright 专攻复杂交互与动态反爬；Apify 负责亚马逊、TikTok 等平台大规模结构化抓取。两者组合可打穿 99% 的情报场景。

**升级玩法**：Reddit 差评 + Amazon 数据交叉验证——先从 `r/AmazonSeller` 抓竞品差评 → 再用 `amazon_search` 验证这些问题产品的真实评分数据 → 交叉分析找选品机会。

---

### 📦 配置/工具详表

| 场景 | 工具/Skill | 安装/配置方式 | 返回数据 | 注意事项 |
|------|-----------|-------------|---------|---------|
| Reddit 免费读取 | reddit-readonly | `https://lobehub.com/skills/openclaw-skills-reddit-scraper` | 热帖、评论串 | 无需 API Key，打 old.reddit.com JSON 接口 |
| Reddit 结构化 | Decodo Skill | `https://github.com/Decodo/decodo-openclaw-skill` | 干净 JSON | 后端 IP 轮换，稳定性更高 |
| Amazon 商品 | Decodo Skill（同上） | 同上安装后直接调用 | 价格、评分、ASIN、BSR | 自动维护解析规则，无需手写 Selector |
| YouTube 字幕 | Decodo `youtube_subtitles` | 同上 | 完整字幕文本 | 输入视频 ID，无需 YouTube API |
| TikTok / B站 | Agent-Reach `yt-dlp` | `https://github.com/Panniantong/agent-reach` | 视频内容 | 148K Stars，两平台通吃 |
| Twitter/X | Agent-Reach `xreach` | Cookie 导出后 `agent-reach configure twitter-cookies "..."` | 推文、时间线 | Cookie 7-30 天过期，需定期重导 |
| GitHub 情报 | `gh CLI` | `brew install gh` + `gh auth login` | 仓库、Issue、Star 趋势 | 官方工具，比爬网页稳定 |
| 动态 SPA | playwright-npx | `https://playbooks.com/skills/openclaw/skills/playwright-npx` | 页面完整数据 | 跑通后适合持续执行 |
| 反爬网站 | stealth-browser | ClawHub 搜索安装 | 页面数据 | 模拟 User-Agent、WebGL 指纹、Timezone |
| 远程沙盒爬取 | Firecrawl | ClawHub 安装，加 `cache: 2d` | 干净 Markdown | 免费 500 次，本机零压力 |
| 搜索（国内） | Tavily | ClawHub 安装 + API Key | 实时搜索结果 | 无需海外信用卡，国内直连 |
| 搜索（高质量） | Brave Search | `https://clawhub.ai/steipete/brave-search` | 高质量搜索结果 | 需海外信用卡注册 |
| 意图型研究 | Exa | ClawHub 安装 | 精准研究结果 | 适合"找真实买家评测"类查询 |
| 工业级批量抓 | Apify | `https://github.com/apify/agent-skills` + API Key | 结构化 CSV/JSON | 覆盖 Google Maps、Amazon、TikTok 等主流平台 |

---

### 🛠️ 操作流程

#### 场景一：Amazon 选品报告（一句话触发）

1. **准备**：安装 Decodo OpenClaw Skill（`https://github.com/Decodo/decodo-openclaw-skill`）
2. **执行**：对 OpenClaw 说：
   ```
   用 amazon_search 搜 "portable blender"，抓前 30 个结果，
   提取价格区间、评分分布、有无 Best Seller 标志，生成选品报告
   ```
3. **升级**：追加 Reddit 交叉验证：
   ```
   再从 r/AmazonSeller 抓 "portable blender" 相关差评，
   与 amazon_search 数据交叉分析，找出差异化机会点
   ```

#### 场景二：YouTube 竞品分析

1. **准备**：安装 Decodo Skill 或 Agent-Reach
2. **执行**：
   ```
   找3个 YouTube 上关于 "camping folding table review" 的视频，
   抓取字幕，提炼用户最常提到的产品问题
   ```
3. **验证**：字幕文本返回后，让 AI 归类高频词并输出 Top5 痛点

#### 场景三：Twitter 热点监控

1. **准备**：用 Cookie-Editor 浏览器扩展导出 Twitter Cookie（JSON 格式）
2. **配置**：
   ```bash
   agent-reach configure twitter-cookies "此处粘贴你复制的Cookie内容"
   ```
3. **执行**：
   ```
   到推特，搜索过去48小时内提到 "Amazon FBA policy change" 的推文，
   整理出主要讨论点
   ```
4. **维护**：每 7-30 天重新导出 Cookie 更新配置

#### 场景四：GitHub 竞品 Issue 挖掘

```bash
# 安装
brew install gh
# 授权
gh auth login
# 在浏览器弹窗中完成授权
```
然后对 OpenClaw 说：
```
搜索 GitHub 上 star 数最高的跨境电商选品工具，
读取它的 issue 列表，看看用户反映最多的 bug 是什么
```

#### 场景五：SPA 动态网站（多 Tab 议程页）

```
帮我爬这个网站的完整议程，页面有5个Tab，
点击每个Tab后等JS加载，把所有展商数据按Tab分文件存成 Markdown
```

---

### 💡 具体案例/数据

**价格监控 Prompt 模板**（配合 cron 每天 03:00 执行）：

```
# 任务：建立电商竞品价格自动监控哨兵
# 触发机制：配置 cron 任务，每天凌晨 03:00 自动执行本提示词。

执行工作流：
1. 抓取最新数据：使用 playwright-npx 或 web_fetch 访问以下竞品链接列表：
   [填入竞品链接1, 链接2...]，提取当前售价和库存状态。
2. 快照比对：读取本地 price_memory.txt 文件中保存的昨日数据快照，
   将新数据与旧数据进行逐一比对。
3. 条件触发：
   - 若价格和状态无变化，静默终止任务。
   - 若发现价格变动（降价、大促标记、断货），立刻生成警报信息
     （包含：商品名、原价、现价、变动幅度、链接）。
4. 消息推送：将警报信息通过 Webhook 发送到我的 [飞书/Telegram] 接收群。
5. 记忆更新：将今日最新价格快照覆盖写入 price_memory.txt，供明日比对使用。
```

**多源选品情报聚合 Prompt 模板**（可加 cron 变成每周自动刷新的选品雷达）：

```
# 任务：执行多源交叉验证的选品调研
# 目标品类：[填入你的目标品类，如：露营折叠桌]

执行工作流（并行或依次调用以下技能）：
1. 亚马逊大盘：调用 amazon_search 抓取该词排名前 50 的商品，
   输出主流价格带、平均评分及 Top3 卖家的份额占比。
2. 社群痛点：调用 reddit_subreddit 搜索相关版块（如 r/Camping），
   提取真实买家近半年的高频吐槽和差评痛点。
3. 评测分析：使用 youtube_subtitles 抓取该品类播放量前 3 的评测视频字幕，
   总结 KOL 强调的核心卖点。
4. 线下竞争：调用 Apify 技能抓取 Google Maps 上相关批发商的数量，
   评估线下竞争热度。
5. 交叉验证与输出：对上述 4 路数据进行交叉比对。
   只有当至少 3 个数据源指向积极信号时，才输出"推荐进入"的结论。
   最终生成一份结构化报告，包含：入场建议、核心痛点总结、差异化产品设计方向。
```

**Apify 实战案例**（Google Maps + 邮箱提取）：
```
搜索美国德州所有做 'electronics wholesale' 的商家 Google Maps 数据，
然后从这些商家网站里提取邮箱
```
执行链路：自动调用 Google Places Actor → 输出结构化 CSV → 再调用 Contact Info Scraper 追加邮箱列。

---

### 📝 避坑指南

- ⚠️ **Reddit API 已于2025年10月关闭开发者接口**，服务器 IP 容易 403，必须走 old.reddit.com JSON 接口或 Decodo IP 轮换方案，不要自己写爬虫。
- ⚠️ **Twitter Cookie 有效期 7-30 天**，过期后 xreach 会静默失败，需定期重新用 Cookie-Editor 导出并重新配置。
- ⚠️ **web_fetch 拿到空 HTML**：速卖通、独立站产品列表等 JS 异步加载页面，必须换 playwright-npx 或 browser-use，不能用 web_fetch。
- ⚠️ **playwright-npx vs browser-use 选型**：已知页面结构 → playwright-npx（跑通后稳定持续执行）；未知结构 → browser-use（视觉模式，但 Token 消耗极大，不适合批量）。
- ⚠️ **Cloudflare 拦截**：playwright-npx 遇到 Cloudflare 必须换 stealth-browser，否则必被拦截。
- ⚠️ **Firecrawl 免费额度只有 500 次**：加 `cache: 2d` 配置避免对同一页面重复消耗额度。
- ⚠️ **Brave Search 需要海外信用卡**：国内用户无法直接注册，优先用 Tavily 作为替代。
- ⚠️ **Playwright 大规模抓取不稳定**：一次抓 500 家竞品时，Playwright 实时生成脚本容易翻车，换 Apify 现成 Actor 更可靠。
- ⚠️ **Skill Router 进阶方向**：可在 `https://github.com/VoltAgent/awesome-openclaw-skills` 搜索 `router` 相关 Skill，让 AI 自动判断该用哪层工具，无需每次手动指定。

---

### 🛠️ 组合技速查表

| 目标场景 | 推荐工具 |
|---------|---------|
| 目标网站有公开 JSON | `web_fetch` / Decodo Skill |
| 有 JS 渲染 | `playwright-npx` |
| 有 Cloudflare | `stealth-browser` |
| VPS 跑 / 内存有限 | Firecrawl（远程沙盒） |
| 主流平台批量抓 | Apify（现成 Actor） |
| 搜索 + 抓内容一步到位 | `firecrawl search --scrape` |
| 国内联网搜索 | Tavily |
| 要求数据零幻觉 | Apify / Firecrawl（确定性工具） |

---

### 🏷️ 行业标签

#OpenClaw #跨境电商 #爬虫 #数据采集 #选品情报 #Reddit #Amazon #Apify #Playwright #AGI工具链

---

---
