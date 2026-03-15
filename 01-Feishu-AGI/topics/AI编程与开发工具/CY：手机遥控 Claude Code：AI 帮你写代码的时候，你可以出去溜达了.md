# AI编程与开发工具

## 39. [2026-02-26]

## 📚 文章 8


> 文档 ID: `KH86wNDwkiJdiXkRfrEcNTWVnod`

**来源**: CY：手机遥控 Claude Code：AI 帮你写代码的时候，你可以出去溜达了 | **时间**: 2026-02-26 | **原文链接**: `https://mp.weixin.qq.com/s/XZZMFl38...`

---

### 📋 核心分析

**战略价值**: Claude Code Remote Control 让你用手机遥控电脑上正在运行的 Claude Code 会话，实现"AI 干活、人类自由"——布置任务后出门，手机审批、查进度、发指令，彻底解除对电脑的物理依赖。

**核心逻辑**:

- **功能本质**：Remote Control 不迁移代码或环境，电脑端项目文件原封不动，手机只是一个遥控器，通过二维码或链接与电脑会话实时同步。
- **审批机制**：Claude 执行到需要许可的操作（修改文件、执行命令）时会主动暂停，将审批请求推送到手机，用户点"批准"继续、点"拒绝"换方案，无需守在电脑前。
- **多设备同步**：对话状态在电脑、手机、平板间实时同步，可从任意设备输入新指令，类似微信多设备登录逻辑。
- **语音输入支持**：手机端可按住麦克风说话代替打字，适合"跑一下测试"、"批准这个修改"等简单指令；复杂技术命令仍建议打字。
- **版本与权限门槛**：需要 Claude Code v2.1.52+，且必须是 Max 计划订阅用户（Pro 正在逐步开放），并已通过 `/login` 完成过一次网页登录。
- **全局自动开启**：通过 `/config → Enable Remote Control for all sessions → true` 可免去每次手动输入，但该选项正在逐步开放，部分用户菜单中暂时不可见。
- **tmux 防断连**：长任务必须配合 tmux 使用，防止终端窗口关闭或 SSH 断连导致任务中断；`Ctrl+B D` 断开，`tmux attach -t claude` 重连。
- **防休眠双保险**：Claude 工作时会自动阻止电脑休眠，但建议额外配置系统级防休眠（Mac：系统设置→电池→选项→开启"当显示器关闭时防止自动休眠"）或命令行 `caffeinate -i -s &`。
- **ntfy 主动推送**：通过在 `.claude/settings.json` 配置 hooks + curl 命令，结合手机 ntfy App，实现 Claude 有事时主动推送通知，无需轮询查看。
- **Git 分支隔离**：布置任务时要求 Claude 先建新分支（如 `feat/new-feature`），完成后用 `git diff main...feat/new-feature` 审查，满意合并，不满意删分支，主代码零风险。
- **现实稳定性**：功能标注为 "Research Preview"，已知问题包括认证 bug、API 500 错误、会话莫名终止、停止按钮失灵、手机 App 看不到会话等；知名开发者 Simon Willison 评价"现在还有点粗糙"，Hacker News 有用户称其为"最多 bug 的产品之一"。

---

### 🛠️ 操作流程

**第一步：确认版本和订阅**

```bash
claude --version   # 确认版本 ≥ v2.1.52
claude update      # 版本不够则升级
```

需满足：
- Claude Code v2.1.52 或更新版本
- Max 计划订阅（Pro 逐步开放中）
- 已通过 `/login` 完成过一次网页登录

**第二步：启动远程连接**

在 Claude Code 会话中输入：

```
/remote-control
```

或简写 `/rc`（可在 Claude 正在执行任务时输入，会排队执行，不打断当前任务）。

**第三步：扫码连接（三种方式）**

| 方式 | 操作 | 适用场景 |
|------|------|---------|
| 扫二维码 | 按空格键显示二维码，手机摄像头扫描 | 最快，推荐首选 |
| 复制链接 | 复制终端 URL，浏览器打开 | 平板或其他电脑 |
| App 列表 | 打开 Claude 手机 App 或 claude.ai/code，找带绿色圆点的会话 | 已安装 App 的用户 |

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 全局自动开启 | `/config → Enable Remote Control for all sessions → true` | 所有会话自动开启远程控制 | 该选项正在逐步开放，部分用户暂时看不到 |
| tmux 防断连 | `brew install tmux` → `tmux new-session -s claude` → `claude remote-control` | 终端关闭或 SSH 断连后任务继续运行 | 断开用 `Ctrl+B D`，重连用 `tmux attach -t claude` |
| Mac 防休眠 | 系统设置→电池→选项→开启"当显示器关闭时防止自动休眠" | 防止电脑休眠中断任务 | Claude 工作时已自动阻止休眠，此为双重保险 |
| 命令行防休眠 | `caffeinate -i -s &` | 阻止系统休眠 | 后台运行，任务结束后手动 kill |
| ntfy 推送通知 | 见下方配置代码块 | Claude 有事时手机秒弹推送 | 需在手机安装 ntfy App 并订阅对应频道 |
| Git 分支隔离 | 任务中加一句："请先创建分支 feat/xxx，然后再开始实现" | 主代码零风险，不满意直接删分支 | 完成后用 `git diff main...feat/xxx` 审查 |

**ntfy 配置代码块**（路径：项目 `.claude/settings.json`）：

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "curl -s -d 'Claude 需要你' ntfy.sh/你的频道名"
      }]
    }]
  }
}
```

---

### 💡 具体案例/数据

- 科技媒体 MacStories 测评：多设备无缝切换是"真正的生活质量提升，不是花哨的噱头"。
- 有用户反馈使用两周后，坐在电脑前的时间减少了 30%，产出质量未下降。
- Hacker News 用户："用语音控制出奇地自然，'看一下测试输出'这种简单指令，说出来比打字快多了。"
- 知名开发者 Simon Willison：遭遇认证 bug、API 500 错误、莫名其妙的会话终止，评价"现在还有点粗糙"。
- Hacker News 吐槽："这是我用过最多 bug、最不精致的产品之一"，状态页"几乎每天都有严重事故"。

---

### 📝 避坑指南

- ⚠️ **提示"账号未开通 Remote Control"**：先 `/logout` 再 `/login` 重新登录一次。
- ⚠️ **API 500 错误**：访问 `status.anthropic.com` 确认服务器状态，等几分钟再试。
- ⚠️ **手机 App 里看不到会话**：已知 bug，直接复制终端链接在浏览器打开。
- ⚠️ **`/rc` 命令不识别**：运行 `claude update` 升级到最新版。
- ⚠️ **二维码显示不出来**：按空格键，或把终端窗口拉宽。
- ⚠️ **断连后恢复不了**：短时间断连会自动恢复；超过 10 分钟需重新运行 `/remote-control`。
- ⚠️ **长任务必须用 tmux**：不用 tmux 直接跑，关掉终端窗口任务就死了。
- ⚠️ **功能仍是 Research Preview**：不要在生产关键任务上依赖它的稳定性。

---

### 🏷️ 行业标签

#ClaudeCode #RemoteControl #AI编程 #开发者工具 #Anthropic #移动端控制 #异步开发

---

---
