# 内容创作与自媒体

## 15. [2026-05-05]

## 📔 文章 5


> 文档 ID: `K2WuwFILkiVpwhk46oAcW2twnid`

**来源**: Coze智能体轻松复刻10w+爆款诗集视频，智能体搭建全流程拆解！ | **时间**: 2025-05-05 | **原文链接**: `https://mp.weixin.qq.com/s/oOGhj85p...`

---

### 📋 核心分析

**战略价值**: 用 Coze 工作流 + 剪映小助手插件，输入一个主题词即可全自动生成「背景+字幕+配音+BGM」的诗集短视频，复刻小红书 6w+ 粉丝账号的爆款内容模式。

**核心逻辑**:

- **账号验证**：目标参考账号专做现代诗集类视频，2025年2月起号，约3个月涨至6w+粉丝，多条视频点赞超1w+，评论爆表，证明该品类在小红书/抖音有稳定流量。
- **触发机制**：音乐+文字组合在0.3秒内刺入听众潜意识，引发情感共鸣，是该类视频高完播率的核心原因。
- **输入设计**：工作流有3个输入字段——`theme`（开头背景两字，如"暗恋"）、`title`（开头标题）、`content`（主体诗句内容）；`content`和`title`为非必填，不填则走模型自动创作，填了则走仿写/二创/续写/直接输出。
- **开头视频**：背景是1920×1080纯黑画板，持续时间固定0~3秒（3,000,000微秒），theme文字转数组后通过时间线插件叠加字幕。
- **内容字幕**：诗句按标点/换行切割成单句列表，再按索引分为3组（textlist1/2/3），目的是在视频中保持字幕整体定位统一，每3句为一个展示单元。
- **时间轴核心**：内容部分从3.1秒（3,100,000μs）开始累积，每句配音时长（秒→微秒）连续叠加，生成每句的start/end；标题时间段每3句合并一段；英文标题在每组第2句起点+180,000μs出现。
- **配音方案**：循环节点遍历字幕列表，每句调用火山引擎官方配音插件生成音频，再用音频时长插件获取每句时长，供时间轴计算使用。
- **全局数据**：BGM和空白视频有默认URL，可覆盖；总时长 = 开头3秒 + 所有配音时长之和，从0开始计算`alltime`。
- **最终合成**：所有时间线数据通过「剪映小助手数据生成器」插件构建，再用「视频合成-剪映小助手」插件按剪辑排列顺序堆砌草稿，一键输出剪映工程文件。
- **代码零门槛**：全程无需手写代码，所有Python节点代码直接复制使用，遇到问题用DeepSeek处理即可。

---

### 🎯 关键洞察

**时间轴是整个工作流最复杂的部分**，逻辑链如下：

> 配音时长（秒）→ 转微秒 → 从3,100,000μs起累积 → 生成每句timeslist → 每3句合并为content_times/title_times → 英文标题偏移180,000μs → 全局alltime = 3,100,000 + 所有配音总时长

关键偏移量汇总：
- 开头结束：3,000,000μs（3秒）
- 内容起点：3,100,000μs（3.1秒，留100ms过渡）
- etime起点：3,100,000 + 600,000 = 3,700,000μs
- dtime范围：3,100,000 ~ 3,700,000μs
- 英文标题偏移：每组第2句start + 180,000μs

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 输入字段 | theme(必填) / title(非必填) / content(非必填) | 非必填为空时走模型创作 | 变量聚合节点必须承接前面输出 |
| 开头背景 | 1920×1080纯黑画板，转base64字符串 | 黑底白字开头 | 图片必须转为可用字符串格式 |
| 开头时间线 | start:0, end:3,000,000（微秒） | 固定3秒开头 | 输出必须为对象数组格式 |
| 诗句切割 | 正则：`[\\ / ,，.。！：；!：;？_—— \n n]\s*` | 切成单句list | 移除空字符串元素 |
| 配音 | 火山引擎官方配音插件（循环节点） | 每句独立音频 | 需配合音频时长插件获取时长 |
| 内容分组 | idx%3 分为textlist1/2/3 | 字幕位置统一 | 每3句一个展示单元 |
| 时间轴计算 | base_time=3,100,000μs，连续累积 | 精准字幕同步 | 秒→微秒用`int(float(t)*1_000_000)` |
| 标题时间段 | 每3段合并，start=第0段start+1，end=第2段end | 标题覆盖3句全程 | 不足3段的组丢弃 |
| 英文标题 | 每组第1段（索引1）start+180,000μs | 英文标题延迟出现 | 偏移量固定180,000μs |
| BGM默认值 | `https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oIEbFeIYChGZrnc3YyUAV6UyfxDt6kICggBoQg` | 有输入则覆盖默认 | 格式必须为数组 |
| 空白视频默认值 | `https://ousir-1308765611.cos.ap-guangzhou.myqcloud.com/%E7%89%B9%E6%95%88/blankvideo.mp4` | 有输入则覆盖默认 | 格式必须为数组 |
| 时间线生成插件 | 剪映小助手数据生成器 | 生成剪映时间线JSON | 按插件描述配置各字段 |
| 视频合成插件 | 视频合成-剪映小助手 | 输出剪映草稿工程 | 按剪辑排列顺序堆砌 |

---

### 🛠️ 操作流程

**第一步：用户输入信息处理**

1. 创建3个输入字段：`theme`（必填）、`title`（非必填）、`content`（非必填）
2. 加入变量聚合节点，承接前面输出结果
3. 可选：加入背景音乐创作节点（不加则后续设为默认BGM）
4. 判断逻辑：content/title为空 → 走创作模型按theme生成诗句；不为空 → 按要求仿写/二创/续写/直接输出

**第二步：开头元素及时间线制作**

1. 代码节点：将theme转为数组 `[theme_str]`
2. 代码节点：生成1920×1080纯黑画板图片，转为base64字符串
3. 代码节点：提取关键词（用于字幕自动配色）
4. 代码节点：构建开头输出变量（sbg/sword/time），time固定为 `[{"start":0,"end":3000000}]`
5. 调用时间线数据生成插件，分别处理：开头背景、开头标题、开头主题

```python
async def main(args: Args) -> Output:
    params = args.params
    sbg = [params['bg']] if 'bg' in params else []
    sword = [params['word']] if 'word' in params else []
    time_common = [{"start": 0, "end": 3000000}]
    ret: Output = {"sbg": sbg, "sword": sword, "time": time_common}
    return ret
```

**第三步：内容元素及时间线制作**

1. 代码节点：用正则切割诗句为单句list

```python
import re
async def main(args: Args) -> Output:
    params = args.params
    content = params['content']
    pattern = r'[\\ / ,，.。！：；!：;？_—— \n n]\s*'
    texts = re.split(pattern, content)
    texts = [t for t in texts if t]
    ret: Output = {"textList": texts}
    return ret
```

2. 代码节点：提取内容关键词（字幕自动上色用）
3. 循环节点（遍历textList）：
   - 火山引擎配音插件 → 生成每句音频
   - 音频时长插件 → 获取每句时长（秒）
4. 代码节点：对字幕加格式数据
5. 代码节点：将title/english_title按诗句组数复制为等长数组（每3句一组）

```python
async def main(args: Args) -> Output:
    params = args.params
    title = params['title']
    english_title = params['english_title']
    textlist = params['textlist']
    group_count = len(textlist) // 3
    titleList = [title for _ in range(group_count)]
    english_titleList = [english_title for _ in range(group_count)]
    ret: Output = {"titleList": titleList, "english_titleList": english_titleList}
    return ret
```

6. 代码节点：将textlist按idx%3分为textlist1/2/3

```python
async def main(args: Args) -> Output:
    textlist = args.params['textlist']
    textlist1, textlist2, textlist3 = [], [], []
    for idx, text in enumerate(textlist):
        match idx % 3:
            case 0: textlist1.append(text)
            case 1: textlist2.append(text)
            case 2: textlist3.append(text)
    return {"textlist1": textlist1, "textlist2": textlist2, "textlist3": textlist3}
```

7. 核心时间轴计算代码节点（完整代码见下方）
8. 调用剪映小助手数据生成器插件，按顺序构建所有内容时间线

**第四步：定义全局数据**

1. 代码节点：聚合bgm/blank_video/alltime，计算总时长

```python
async def main(args: Args) -> Output:
    params = args.params
    DEFAULT_BGM = ["https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oIEbFeIYChGZrnc3YyUAV6UyfxDt6kICggBoQg"]
    DEFAULT_blank_video = ["https://ousir-1308765611.cos.ap-guangzhou.myqcloud.com/%E7%89%B9%E6%95%88/blankvideo.mp4"]
    ret: Output = {"alltime": [], "bgm": DEFAULT_BGM, "blank_video": DEFAULT_blank_video}
    if 'bgm' in params and isinstance(params['bgm'], list):
        ret["bgm"] = params['bgm']
    if 'blank_video' in params and isinstance(params['blank_video'], list):
        ret["blank_video"] = params['blank_video']
    if 'stime' in params and isinstance(params['stime'], list) and len(params['stime']) > 0:
        stime = params['stime'][0]
        audio_total = 0
        if 'audiotime_list' in params and isinstance(params['audiotime_list'], list):
            try:
                audio_total = sum(float(t) * 1_000_000 for t in params['audiotime_list'])
            except:
                audio_total = 0
        stime_duration = stime["end"] - stime["start"]
        total_duration = stime_duration + audio_total
        ret["alltime"] = [{"start": 0, "end": total_duration}]
    return ret
```

2. 调用剪映小助手数据生成器，定义全局时间线元素

**第五步：构建剪映草稿**

1. 调用「视频合成-剪映小助手」插件
2. 按剪辑排列顺序（开头→内容→全局）逐步堆砌草稿元素
3. 参考插件官方操作手册配置各字段

---

### 💡 核心时间轴计算完整代码

```python
async def main(args: Args) -> Output:
    params = args.params
    ret: Output = {
        "audio": [], "times": [], "timeslist": [], "bg_effect": [], "bg_img": [],
        "content_times1": [], "content_times2": [], "content_times3": [],
        "title_times": [], "Etitle_times": [], "bg_img2": [], "etime": [], "dtime": []
    }

    if 'audio' in params and params['audio']:
        ret["audio"] = [str(params['audio'])]

    if 'audiotime_list' in params and isinstance(params['audiotime_list'], list):
        try:
            time_us_list = [int(float(t) * 1_000_000) for t in params['audiotime_list']]
        except:
            time_us_list = []

        base_time = 3_100_000
        current = base_time

        for duration in time_us_list:
            ret["timeslist"].append({"start": current, "end": current + duration})
            current += duration

        if ret["timeslist"]:
            ret["times"] = [{"start": ret["timeslist"][0]["start"] + 1, "end": ret["timeslist"][-1]["end"]}]
            ret["etime"] = [{"start": base_time + 600_000, "end": ret["timeslist"][-1]["end"]}]
            ret["dtime"] = [{"start": base_time, "end": base_time + 600_000}]

        cumulative_times = [base_time]
        for duration in time_us_list:
            cumulative_times.append(cumulative_times[-1] + duration)

        content_times1_ends = []
        for i in range(0, len(ret["timeslist"]), 3):
            if i + 3 <= len(time_us_list):
                end_time = cumulative_times[i+3]
                ret["content_times1"].append({"start": ret["timeslist"][i]["start"] + 1, "end": end_time})
                content_times1_ends.append(end_time)

        for i in range(1, len(ret["timeslist"]), 3):
            if i//3 < len(content_times1_ends):
                ret["content_times2"].append({"start": ret["timeslist"][i]["start"] + 1, "end": content_times1_ends[i//3]})

        for i in range(2, len(ret["timeslist"]), 3):
            if i//3 < len(content_times1_ends):
                ret["content_times3"].append({"start": ret["timeslist"][i]["start"] + 1, "end": content_times1_ends[i//3]})

        for i in range(0, len(ret["timeslist"]), 3):
            group = ret["timeslist"][i:i+3]
            if len(group) == 3:
                ret["title_times"].append({"start": group[0]["start"] + 1, "end": group[2]["end"]})

        for i in range(0, len(ret["timeslist"]), 3):
            group = ret["timeslist"][i:i+3]
            if len(group) == 3:
                ret["Etitle_times"].append({"start": group[1]["start"] + 180_000, "end": group[2]["end"]})

    for field in ['textList', 'bg_effect', 'bg_img', 'bg_img2']:
        if field in params:
            val = params[field]
            ret[field] = val if isinstance(val, list) else [str(val)]

    return ret
```

---

### 📝 避坑指南

- ⚠️ 开头背景图片生成后必须转为字符串格式，否则后续插件无法读取
- ⚠️ sbg/sword/time/bgm/blank_video 等所有输出必须是数组格式，不能是单值
- ⚠️ 时间单位全程使用微秒（μs），配音插件返回的是秒，必须 `×1,000,000` 转换
- ⚠️ 诗句总数必须是3的倍数才能保证content_times/title_times完整，不足3句的末尾组会被丢弃
- ⚠️ 变量聚合节点不能漏，否则前面节点的输出无法传递到后续节点
- ⚠️ 剪映草稿堆砌顺序必须与实际剪辑排列顺序一致，顺序错误会导致时间线错位
- ⚠️ BGM和空白视频有硬编码默认URL，如需替换直接修改DEFAULT_BGM和DEFAULT_blank_video的值

---

### 🏷️ 行业标签

#Coze工作流 #剪映自动化 #诗集短视频 #AI内容创作 #小红书涨粉 #视频时间轴 #火山引擎TTS #自动剪辑

---

---
