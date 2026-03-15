# Skill: feishu-knowledge-extractor

## 适用场景
从飞书知识库（Wiki）批量提取文章内容，经 Claude 提纯后生成结构化 Markdown 日报。

---

## 核心架构

```
飞书索引页 (Wiki)
    ↓ list_blocks (分页，每页500)
index_map.json (日期 → [doc_token, ...])
    ↓ batch_process.py (每次处理1天)
generate_daily_report.py (逐篇读取 + Claude 提纯)
    ↓
daily/YYYY-MM-DD.md
```

---

## 关键文件

| 文件 | 作用 |
|------|------|
| `data/index_map.json` | 日期到文章 token 的映射，离线构建 |
| `data/extract-state.json` | 断点状态，记录已完成日期 |
| `scripts/batch_process.py` | 全量/增量处理入口，每次处理1天 |
| `scripts/generate_daily_report.py` | 读取单篇文章 + Claude 提纯 |
| `scripts/incremental_update.py` | 每天重新拉索引页 diff 新增 token |

---

## 正确的数据提取方式

### ❌ 错误：用 `feishu_doc(read)` 读索引页
返回纯文本，超链接全部丢失，拿不到文章 token。

### ✅ 正确：用 `feishu_doc(list_blocks)` 分页拉取
```python
# 分页拉取所有 blocks
params = {'page_size': 500}
if page_token:
    params['page_token'] = page_token
r = requests.get(
    f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks',
    headers={'Authorization': f'Bearer {access_token}'},
    params=params
)
# 从 block 的 mention_doc.obj_token 拿到文章 token
```

---

## 增量更新逻辑

每天凌晨 2 点（Asia/Shanghai）触发：
1. 重新拉索引页全量 blocks，解析出最新 index_map
2. diff 出今天新增的 token
3. 更新 `index_map.json`
4. 调 `batch_process.py` 处理今天

Cron 配置：`0 2 * * *` (Asia/Shanghai)，OpenClaw 原生 cron 工具配置，**不用 bash crontab**。

---

## 断点机制

`extract-state.json` 格式：
```json
{
  "last_processed": "YYYY-MM-DD",
  "completed": ["2026-01-03", "2026-01-04", ...],
  "failed": [],
  "last_run": "ISO8601时间戳"
}
```

`batch_process.py` 的截止判断（防止空跑）：
```python
today = datetime.now().strftime('%Y-%m-%d')
if date > today:
    return None  # 不处理未来日期
```

---

## 踩坑记录（血泪教训）

1. **索引页 read 拿不到 token** → 必须用 list_blocks
2. **index_map 全年占位** → 脚本必须加 `date > today` 截止判断
3. **断点文件中途换格式** → 定好格式不要换，换之前清理旧文件
4. **cron 无退出机制** → 必须在 `get_next_date` 返回 None 时自然退出
5. **在 session 里连续跑大量内容** → context 会爆，必须用 cron 每次处理1天

---

## 启动新任务前必过检查

参考 `AUTOMATION_CHECKLIST.md`，重点确认：
- [ ] 已用 list_blocks 验证能拿到真实文章 token
- [ ] 已端到端跑通一篇文章的完整提取链路
- [ ] index_map 已构建，内容日期范围已确认
