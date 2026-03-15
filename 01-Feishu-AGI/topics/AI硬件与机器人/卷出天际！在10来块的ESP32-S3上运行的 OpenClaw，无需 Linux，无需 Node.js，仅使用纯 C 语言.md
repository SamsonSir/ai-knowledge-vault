# AI硬件与机器人

## 9. [2026-02-16]

## 📙 文章 4


> 文档 ID: `YIRLwxBGWiOXuKkSiAxcRvIynjc`

**来源**: 卷出天际！在10来块的ESP32-S3上运行的 OpenClaw，无需 Linux，无需 Node.js，仅使用纯 C 语言 | **时间**: 2026-02-10 | **原文链接**: `https://mp.weixin.qq.com/s?__biz=Mz...`

---

### 📋 核心分析

**战略价值**: 用 ESP32-S3（MCU 级硬件）+ 纯 C 固件实现具备持久记忆、工具调用、Telegram 远程控制的边缘 AI 代理，成本极低，无需 Linux/Node.js。

**核心逻辑**:

- **项目名称**: MimiClaw，基于 OpenClaw 理念，运行在 ESP32-S3 开发板上，固件语言为纯 C
- **硬件规格下限**: ESP32-S3 + 16MB Flash + 8MB PSRAM，功耗约 0.5W，USB 供电即可永动运行
- **记忆持久化机制**: 上下文不存 RAM，而是写入 Flash；对话历史用 `SOUL.md`、`USER.md`、`MEMORY.md` 三个 Markdown 文件存储，结构化数据用 JSONL 格式；重启后直接从 Flash 加载，实现跨电源周期记忆保留
- **交互入口**: 通过 Telegram Bot 收发消息，手机即可远程操控 AI 代理（需科学上网）
- **工具调用架构**: 内置工具系统，开发者可自定义 C 函数作为工具，例如 `read_temperature()`、`control_relay(on/off)`，直接调用 ESP32 的 GPIO、I2C、SPI 驱动，几行代码即可扩展
- **推理分工**: 传感器数据本地读取，Claude API 只负责高级推理，降低延迟，无需云端中转传感器原始数据
- **并发架构**: 双核 FreeRTOS 任务队列，一个核持续巡检传感器，另一个核处理 AI 推理与 Telegram 通信，互不阻塞
- **触发逻辑**: 传感器值超过阈值 → 触发工具调用 → Claude 推理 → 执行动作（如 `control_relay(ON)`）→ 发送 Telegram 通知，全链路自动化
- **Flash 磨损风险**: 频繁写操作会加速 Flash 磨损，适合低频交互场景，高频写入需评估寿命
- **扩展上限**: ESP32 的 8MB PSRAM / 16MB Flash 是天花板，复杂多模态推理、Modbus/OPC UA 工业协议、大容量日志、本地小模型等场景需升级至 Linux 工控板

---

### 🎯 关键洞察

**为什么 Flash 存 Markdown 而不是数据库？**
原因：ESP32 无法运行 SQLite 等数据库引擎，PSRAM 只有 8MB 不够缓存大量上下文。
动作：用 Markdown 纯文本文件分类存储（偏好/用户画像/事件日志），JSONL 存结构化记录。
结果：重启零成本恢复上下文，文件格式人类可读，调试方便，且 Claude 可直接理解 Markdown 内容作为 prompt 输入。

**为什么推理不在本地跑？**
原因：8MB PSRAM 根本无法加载任何可用的语言模型权重。
动作：本地只跑传感器采集 + 工具执行，推理请求发给 Claude API。
结果：边缘侧负责实时性（低延迟感知+执行），云侧负责智能性（语义理解+决策），职责分离，成本可控。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 记忆存储 | Flash 写入 `SOUL.md`、`USER.md`、`MEMORY.md`，结构化数据用 JSONL | 断电重启后上下文完整恢复 | 高频写入加速 Flash 磨损，低频场景才优雅 |
| 自定义工具 | C 函数 `read_temperature()`、`control_relay(on/off)`，调用 ESP32 GPIO/I2C/SPI 驱动 | AI 可直接调用硬件动作 | 工具函数需注册到 MimiClaw 工具系统，参考项目文档 |
| Telegram 接入 | 配置 Telegram Bot Token，项目文档有逐步指引 | 手机消息远程控制 AI 代理 | 需科学上网，国内直连不可用 |
| 并发任务 | FreeRTOS 双核任务队列，一核巡检传感器，一核处理推理/通信 | 传感器采集与 AI 响应互不阻塞 | 任务优先级需合理配置，避免看门狗超时 |
| 阈值触发 | 传感器值超阈值 → 调用 Claude 推理 → 执行工具 → 发 Telegram 通知 | 全自动闭环控制 | 阈值参数硬编码在 C 代码中，修改需重新编译烧录 |
| 硬件接线 | AHT30 接 I2C，继电器接 GPIO，用杜邦线连接 | 温湿度采集 + 继电器控制 | 确认 I2C 地址无冲突，GPIO 电平匹配继电器模块 |

---

### 🛠️ 操作流程

1. **准备阶段**:
   - 硬件：ESP32-S3 开发板（16MB Flash + 8MB PSRAM）+ AHT30 温湿度传感器 + 继电器模块 + 杜邦线
   - 软件环境：安装 ESP-IDF 工具链
   - 创建 Telegram Bot，获取 Bot Token

2. **核心执行**:
   - `git clone` MimiClaw 源码：`https://github.com/memovai/mimiclaw`
   - 在项目配置文件中填入 WiFi SSID/密码 和 Telegram Bot Token
   - 用 ESP-IDF 编译：`idf.py build`
   - 烧录固件：`idf.py flash`
   - 接线：AHT30 → I2C 引脚，继电器模块 → 指定 GPIO 引脚
   - 在 C 代码中添加自定义工具函数 `read_temperature()` 和 `control_relay(on/off)`，注册到工具系统，重新编译烧录

3. **验证与优化**:
   - 上电后通过 Telegram 发送测试消息，确认 AI 响应正常
   - 检查 Flash 中 `MEMORY.md` 是否正确写入交互记录
   - 断电重启后再次发消息，验证历史上下文是否从 Flash 正确加载
   - 根据实际场景调整传感器阈值参数，重新编译烧录
   - 参考 Quick Start 文档：`https://mimiclaw.io`

---

### 💡 具体案例/数据

**场景：室内温湿度自动控制**

- 早上发消息："今天天气热吗？帮我盯着室内温度。"
  → MimiClaw 调用 `read_temperature()` 读到 28°C，结合 `web_search` 查本地天气，回复："室内 28°C，外头预计 32°C，我每 5 分钟监控一次，超过 30°C 自动开风扇。"

- 后台自动触发：温度升到 31°C → 触发 Claude 推理 → 执行 `control_relay(ON)` 开风扇 → 发 Telegram："温度升到 31°C，已自动开启风扇，当前湿度 65%。"

- 下午远程查询："现在屋里情况怎么样？"
  → 从 Flash `MEMORY.md` 加载历史，回复："从上午 10 点开始，温度在 27-31°C 波动，已自动开关风扇 3 次。最新读数 29.5°C，风扇关闭中。"

- 晚上总结："今天帮我总结一下室内环境。"
  → 读取 `SOUL.md`（偏好：舒适温度 25-28°C）+ `USER.md`（个人习惯）+ `MEMORY.md`（日志），生成："今天平均温度 29.2°C，最高 31.1°C，共运行风扇 45 分钟。建议明天把阈值调到 29°C 更省电。"

---

### 📝 避坑指南

- ⚠️ **Flash 磨损**：`MEMORY.md` 等文件频繁写入会加速 Flash 寿命消耗，高频交互场景（每分钟多次写入）需评估 Flash 寿命或降低写入频率
- ⚠️ **Telegram 需科学上网**：国内网络环境无法直连 Telegram API，需在路由器或设备网络层配置代理
- ⚠️ **阈值修改需重新烧录**：当前阈值参数硬编码在 C 代码中，动态调整需通过 Telegram 指令写入配置文件并解析，需自行实现
- ⚠️ **8MB PSRAM 是硬上限**：不要尝试在本地跑任何语言模型推理，所有 LLM 调用必须走 Claude API
- ⚠️ **FreeRTOS 任务优先级**：双核任务若优先级配置不当，可能触发看门狗复位，调试时注意串口日志

---

### 🏷️ 行业标签

#ESP32-S3 #边缘AI #嵌入式C #MimiClaw #OpenClaw #FreeRTOS #Telegram机器人 #AIoT #持久记忆 #工具调用

---

---
