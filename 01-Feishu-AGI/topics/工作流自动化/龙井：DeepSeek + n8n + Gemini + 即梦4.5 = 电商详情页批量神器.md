# 工作流自动化

## 5. [2026-01-16]

## 📒 文章 7


> 文档 ID: `I6jhwDnxvixaJQk7C9qcday5npS`

**来源**: 龙井：DeepSeek + n8n + Gemini + 即梦4.5 = 电商详情页批量神器 | **时间**: 2026-03-13 | **原文链接**: 无

---

### 📋 核心分析

**战略价值**: 用 n8n 工作流 + 即梦4.5 API 实现「输入产品参数/亮点/图片 → 自动批量输出10张电商详情页」的全自动流水线，前端用纯 HTML 单文件承接，零代码部署可用。

**核心逻辑**:
- 整体架构分两层：n8n 后端工作流（负责 AI 调用、数据处理、图片生成）+ 纯 HTML 前端（负责用户输入、结果展示、下载）
- 触发方式分两阶段迭代：开发调试阶段用「表单节点」，前后端联调阶段换成「Webhook 节点」，两者字段名一致，切换时只需修改数据引用路径
- 产品图片必须先经过「视觉理解模型」转成文字描述（英文），再传入后续生图流程，目的是提升10张图之间产品外观的一致性
- 文案策划节点要求模型输出严格的 JSON 结构（含 `slides` key），禁止输出 Markdown 代码块，避免后续 `JSON.parse` 失败
- 文案数据用 Code 节点拆分成10个独立 item，再进入 Loop 循环节点（batch size=1）逐张生图，保证每张图独立处理
- 每张图的生图提示词由 Agent 节点动态拼接（产品视觉描述 + 场景描述 + 主副标题），并明确约束：禁止画面出现额外文字、禁止出现"9:16"字样
- 即梦4.5 通过 HTTP 节点调用，参数来自火山引擎 API Explorer 调试台导出的 curl，导入 n8n 后删除 `watermark` 参数（该参数即梦4.5不支持）
- 10张图生成完毕后，用 Code 节点聚合成一个 `{ images: [...], total: 10 }` 对象，再由 `Respond to Webhook` 节点一次性返回前端
- 前端 HTML 用 `FormData` 发送数据（字段名固定：`产品的参数`、`产品的亮点`、`data`），接收到图片 URL 数组后渲染展示，下载采用双重保障（fetch→Blob 优先，CORS 失败则降级 `window.open`），循环间隔 500ms 防浏览器拦截
- 模型选型：视觉理解用豆包1.6视觉模型，文案策划和提示词生成用 DeepSeek-V3-2，生图用即梦4.5，均通过火山引擎 API 统一接入

---

### 🎯 关键洞察

**为什么要先用表单节点再换 Webhook？**
表单节点可以在 n8n 内部直接提交测试数据，不依赖外部前端，适合单独调试每个节点。等工作流稳定后再换 Webhook，前端才能真正打通。切换后必须同步修改工作流中所有引用 `$('On form submission')` 的地方，改成 Webhook 节点对应的引用路径。

**为什么要做「产品原型描述」这一步？**
直接把图片传给生图模型，10张图里产品外观会漂移（颜色、材质、形状不一致）。先用视觉模型把产品外观转成固定的英文文字描述，再把这段描述注入每张图的提示词，相当于给10张图锁定了同一个产品"锚点"。

**即梦4.5 接入的核心坑**：
- 必须先在 API Explorer 调试成功，再复制 curl 导入 n8n，不能直接手写参数
- `watermark` 参数必须删除，否则报错
- 新用户有200张免费额度，可以放心调试

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| n8n 版本 | 2.2.4，Docker 本地部署 | 稳定运行 | 参考：`https://mp.weixin.qq.com/s/fhtcPEPBWxjo6xZLEKCRzw` |
| 触发节点（调试期） | On Form Submission，字段：产品的参数、产品的亮点、产品图片 | 本地表单上传测试数据 | 联调前端后需替换为 Webhook 节点 |
| 触发节点（生产期） | Webhook 节点，HTTP Method: POST | 接收前端 FormData | Test URL 用于测试，生产环境换 Production URL |
| 产品原型描述 | OpenAI Chat Model 节点，接豆包1.6视觉模型；开启图片传递 | 输出产品英文外观描述 | 必须选有视觉理解能力的模型；base url: `https://ark.cn-beijing.volces.com/api/v3` |
| 电商文案策划 | Basic LLM Chain，模型 DeepSeek-V3-2 | 输出含 `slides` key 的 JSON 数组（10个对象） | 系统提示词必须强调禁止输出 Markdown 代码块 |
| 数据拆分 | Code 节点，`JSON.parse` + `.map` | 1个 item → 10个独立 item | 见下方代码块 |
| 循环生图 | Loop Over Items，batch size=1 | 逐张处理10个 item | batch size 必须为1 |
| 提示词生成 | Agent 节点，模型 DeepSeek-V3-2 | 输出单张图的完整绘图提示词 | 用户提示词动态引用 `$('产品原型描述').item.json.output` 和 `$json.scene_desc` 等 |
| 即梦4.5 生图 | HTTP 节点，从 API Explorer curl 导入 | 返回图片 URL | 删除 `watermark` 参数；先调试成功再导入 |
| 图片聚合 | Code 节点，提取所有 item 的 URL 合并为数组 | 输出 `{ images: [...], total: 10 }` | 见下方代码块 |
| 返回前端 | Respond to Webhook，Body: `{{ $json }}` | 一次性返回所有图片 URL | 必须放在工作流最末尾 |
| 前端 HTML | 单文件，FormData POST，双重下载保障 | 输入→生成→展示→下载 | WEBHOOK_URL 变量在代码顶部修改 |

---

### 🛠️ 操作流程

**阶段一：搭建 n8n 后端工作流**

1. **触发节点（表单）**
   - 添加 `On Form Submission` 节点
   - 创建三个字段：`产品的参数`（文本）、`产品的亮点`（文本）、产品图片（文件上传）

2. **产品原型描述节点**
   - 添加 Basic LLM Chain 节点
   - 开启图片传递选项
   - 添加 OpenAI Chat Model 子节点，连接火山引擎豆包1.6视觉模型
   - 鉴权配置：API Key 填火山引擎 Key，base url 填 `https://ark.cn-beijing.volces.com/api/v3`
   - 用户提示词：
     ```
     请仔细看这张图。请用一段英文详细描述这个产品的视觉外观。
     重点描述：颜色、材质（如磨砂/光面）、形状结构、以及产品上的关键细节。
     注意：只描述产品本身，不要描述背景。这段文字将用于生成后续的绘图提示词。
     ```

3. **电商文案策划节点**
   - 添加 Basic LLM Chain 节点，模型选 DeepSeek-V3-2
   - 用户提示词：
     ```
     这是产品的参数：
     {{ $('On form submission').item.json['产品的参数'] }}

     这是产品的亮点：
     {{ $('On form submission').item.json['产品的亮点'] }}
     ```
   - 系统提示词：
     ```
     你是资深的电商详情页策划专家。
     任务：根据用户提供的产品参数和亮点，策划一套 10 屏的手机端详情页方案。

     请严格按照以下 JSON 结构输出一个包含 10 个对象的数组，包含 key: "slides"。
     不要输出 Markdown 代码块 (```)，不要输出任何解释性文字。

     【输出示例格式】：
     {
       "slides": [
         {
           "id": 1,
           "title": "静享自由",
           "copy": "48dB深度降噪，喧嚣止步",
           "scene_desc": "Cinematic shot, soft volumetric lighting, minimalist concrete background, floating feather indicating lightness"
         },
         {
           "id": 2,
           "title": "蓝牙5.3",
           "copy": "0.038s无感延迟，音画同步",
           "scene_desc": "Cyberpunk neon lighting, blurred motion background, high tech data stream visualization"
         }
       ]
     }
     ```

4. **数据拆分 Code 节点**
   ```javascript
   // 只取第一个 item
   const item = $input.first();

   // 把 output 里的字符串解析成对象
   const parsed = JSON.parse(item.json.output);

   // 返回 slides 数组作为新的 items
   return parsed.slides.map(slide => ({
     json: slide,
   }));
   ```

5. **循环节点**
   - 添加 Loop Over Items 节点
   - batch size 设置为 **1**

6. **Agent 节点（生成绘图提示词）**
   - 模型选 DeepSeek-V3-2
   - 用户提示词：
     ```
     产品视觉呈现：
     {{ $('产品原型描述').item.json.output }}

     产品描述：
     {{$json.scene_desc}}

     需渲染文字（必须完全精准呈现）：
     主标题："{{$json.title}}"
     副标题："{{$json.copy}}"

     设计要求：
     制作一张竖版电商海报（画面比例 9:16）。
     产品必须作为视觉核心，与上述场景自然融合。
     文字排版：将主标题与副标题美观地置于画面留白区域（顶部或底部）。文字需清晰易读、风格精致，与背景形成高对比度。
     整体风格：高端商业广告质感，C4D 渲染效果，版式简洁大气，达到获奖级海报设计水准。
     重点注意：必须严格按照原文，将 "{{ $json.title }}" 和 "{{ $json.copy }}" 精准呈现在图像上，不得出现任何拼写错误，仅生成指定的主副标题，画面其他区域（尤其是四角）禁止出现任何额外文字 / 伪文字
     ```
   - 系统提示词：
     ```
     ## 角色
     你是一名精通即梦4.0 模型的 AI 绘图提示词工程师。
     你的任务是将**产品视觉呈现**与**产品描述**整合为一段逻辑连贯、高质量的绘图提示词。

     ## 格式
     输出格式要求：仅提交提示词文本，无需附加任何解释说明。

     ## 严格限制：
     仅生成指定的主副标题，画面所有区域（包括但不限于四角、边缘、背景）严禁出现任何数字、符号类文字，尤其是 "9:16" 相关字样，确保画面纯净无额外文字干扰。
     ```

7. **即梦4.5 HTTP 节点**
   - 进入火山引擎 API Explorer：`https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey`
   - 在 API Explorer 中将模型切换为即梦4.5，其他参数保持默认，先调试成功
   - 调试成功后复制 curl
   - 在 n8n 中添加 HTTP Request 节点 → 导入 curl
   - 将 prompt 参数替换为 Agent 节点输出的提示词
   - **删除 `watermark` 参数**（即梦4.5不支持）

8. **图片聚合 Code 节点**（放在 Loop 节点之后）
   ```javascript
   // 获取流入当前节点的所有 10 个数据包
   const items = $input.all();

   // 遍历所有数据包，提取 URL
   const images = items.map(item => {
     const d = item.json;
     
     // 1. 优先匹配即梦 API 格式
     if (d.data && Array.isArray(d.data) && d.data[0] && d.data[0].url) {
         return d.data[0].url;
     }
     
     // 2. 兼容其他可能的格式
     if (d.data && d.data.url) return d.data.url;
     if (d.output) return d.output;
     if (d.url) return d.url;
     
     return null;
   }).filter(url => url); // 去除空值

   // 只返回 1 个对象，包含所有图片数组
   return {
     json: {
       images: images,
       total: images.length,
       debug_input_size: items.length
     }
   };
   ```

9. **Respond to Webhook 节点**
   - 放在工作流最末尾
   - Response Body 填：`{{ $json }}`

---

**阶段二：搭建前端 HTML**

1. **用 Gemini 生成前端**，使用以下完整 Prompt：

```
# Role
你是一名精通 n8n 工作流对接的高级前端开发工程师。你的任务是编写一个单文件 HTML（包含 CSS 和 JS），作为 n8n AI 生图工作流的本地前端控制台。

# Goal
生成一个极具科技感（赛博朋克/暗黑风格）的 Web 界面，左侧为输入区，右侧为结果展示区。用户填写信息并上传图片后，通过 Webhook 发送给 n8n，并展示返回的生成图片，支持批量下载。

# Visual Style Requirements
1. **布局**：左右分栏布局。左侧 30% 为控制面板（固定），右侧 70% 为结果展示区（可滚动）。
2. **风格**：Dark Mode（深色模式），使用霓虹色（如青色 #00f3ff）作为强调色。
3. **交互**：按钮要有 Hover 效果，生图过程中要有明显的 Loading 动画（遮罩层）。
4. **响应式**：上传图片区域支持点击上传和文件拖拽预览。

---

---
