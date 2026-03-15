#!/usr/bin/env python3
"""
生成单个日期的合并日报 Markdown
将该日期的所有日报合并到一个文件中
使用 Claude Sonnet 提纯内容（纯文本，无图片）
"""
import json
import sys
import os
import re
import time
import signal
import requests
from pathlib import Path


def timeout_handler(signum, frame):
    print('[ERROR] 请求超时，强制退出', file=sys.stderr)
    sys.exit(1)


# 设置全局超时 300 秒
signal.signal(signal.SIGALRM, timeout_handler)

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'

# 飞书 API 凭证
FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', 'cli_a90749c404a1dbd6')
FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', 'n9vXbGD1jYmy3U3jQb82afNIUKjJxYdf')


def read_shell_export(name):
    """从 ~/.bashrc ~/.zshrc 读取 export 变量"""
    home = Path.home()
    for rc in [home / '.bashrc', home / '.zshrc']:
        if not rc.exists():
            continue
        try:
            text = rc.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        m = re.search(rf'export\s+{re.escape(name)}=(?:"([^"]*)"|\'([^\']*)\'|([^\n#]+))', text)
        if m:
            return (m.group(1) or m.group(2) or m.group(3) or '').strip()
    return ''


def get_runtime_var(name, default=''):
    return os.getenv(name) or read_shell_export(name) or default


# Claude API 配置
CLAUDE_API_KEY = get_runtime_var('ANTHROPIC_API_KEY', 'sk-Gr8tCh3atKEdlGJpUGpcPFSCnovO2rgMcWeF4p50zfOoZSIL')
CLAUDE_BASE_URL = get_runtime_var('ANTHROPIC_BASE_URL', 'https://www.packyapi.com')

# 超长文章阈值
MAX_CHARS = 25000


REFINE_PROMPT = '''你是一位资深 AI 知识架构师，任务是将飞书文档的 raw_content 提纯为可直接录入 Obsidian 知识库的高质量 Markdown。

## 提纯协议（必须严格遵守）

### 1. 元数据保留
- 必须保留文章原始来源、发布时间、原文链接
- 格式：在文章开头添加 > 引用块，包含来源信息

### 2. 内容结构（层级化输出）
必须按以下结构组织：

```markdown
### 📋 核心分析

**战略价值**: 一句话概括文章的战略意义

**核心逻辑**:
- 要点 1
- 要点 2
...

### 🎯 关键洞察
3-5 条深度洞察，每条独立成段，用加粗小标题引导

### 📦 可执行模块（如适用）
| 模块 | 内容描述 | 适用场景 |
|------|---------|---------|
| XXX | XXX | XXX |

### 🔗 相关资源
- 原文链接：XXX
- 相关工具：XXX
```

### 3. 提纯原则
- **删减**: 删除寒暄、过渡性废话、表情符号堆砌、广告引流
- **保留**: 核心方法论、操作步骤、技术细节、数据支撑、作者洞见
- **改写**: 口语化表达 → 结构化表达，但保持原意
- **加强**: 将隐含逻辑显性化，补充技术背景上下文

### 4. 输出要求
- 只输出提纯后的 Markdown 内容
- 禁止输出任何解释性文字、JSON 标记、代码块包裹
- 禁止使用 "以下是提纯后的内容" 等引导语

---

原始内容如下，请开始提纯：

{content}
'''


def get_tenant_access_token():
    r = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={'app_id': FEISHU_APP_ID, 'app_secret': FEISHU_APP_SECRET}
    )
    data = r.json()
    if data.get('code') != 0:
        print(f'[ERROR] 获取 token 失败: {data}', file=sys.stderr)
        sys.exit(1)
    return data['tenant_access_token']


def export_doc_to_markdown(doc_token, access_token):
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/raw_content'
    r = requests.get(url, headers={'Authorization': f'Bearer {access_token}'}, params={'lang': 0}, timeout=60)
    data = r.json()
    if data.get('code') != 0:
        print(f'[WARN] 文档不可访问 ({doc_token}): code={data.get("code")} {data.get("msg")}', file=sys.stderr)
        return None
    return data['data']['content']


def sanitize_urls(content):
    """把 https?:// 替换为占位符，防止 Claude 触发 WebFetch"""
    return re.sub(r'https?://', '__URL__', content)


def restore_urls(content):
    """把占位符还原为 https://"""
    return content.replace('__URL__', 'https://')


def refine_content_with_claude(content, doc_token):
    """使用 Claude Sonnet 按架构师级协议提纯内容"""

    # 超长文章直接跳过
    if len(content) > MAX_CHARS:
        print(f'[INFO] 文章过长（{len(content)} 字符），跳过提纯', file=sys.stderr)
        return f'> ⚠️ **文章内容过长（约 {len(content)} 字符），已跳过自动提纯。**\n> 🔗 原文链接：https://waytoagi.feishu.cn/wiki/{doc_token}\n'

    prompt = REFINE_PROMPT.format(content=sanitize_urls(content))
    headers = {'Authorization': f'Bearer {CLAUDE_API_KEY}', 'Content-Type': 'application/json'}
    payload = {
        'model': 'claude-sonnet-4-6',
        'max_tokens': 4096,
        'messages': [{'role': 'user', 'content': prompt}]
    }

    for attempt in range(3):
        try:
            r = requests.post(f'{CLAUDE_BASE_URL}/v1/messages', headers=headers, json=payload, timeout=120)
            if r.status_code == 200:
                result = r.json()
                refined = result.get('content', [{}])[0].get('text', '')
                return restore_urls(refined)
            else:
                print(f'[WARN] 第 {attempt+1} 次尝试失败（状态码 {r.status_code}），重试...', file=sys.stderr)
                time.sleep(2 ** attempt)
        except Exception as e:
            print(f'[WARN] 第 {attempt+1} 次尝试异常: {e}，重试...', file=sys.stderr)
            time.sleep(2 ** attempt)

    # 全部失败，返回原始内容+提示
    print(f'[ERROR] API 多次重试失败，返回原始内容', file=sys.stderr)
    return f'> ⚠️ **API 多次重试失败，已跳过自动提纯。**\n> 🔗 原文链接：https://waytoagi.feishu.cn/wiki/{doc_token}\n\n```\n{content[:2000]}\n```\n'


def load_index_map():
    index_file = DATA_DIR / 'index_map.json'
    if not index_file.exists():
        print(f'[ERROR] index_map.json 不存在', file=sys.stderr)
        sys.exit(1)
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_daily_report(date, access_token, output_dir):
    index_map = load_index_map()
    if date not in index_map:
        print(f'[ERROR] {date} 没有日报', file=sys.stderr)
        sys.exit(1)

    tokens = index_map[date]
    print(f'[INFO] {date} 共有 {len(tokens)} 篇日报', file=sys.stderr)

    output_dir.mkdir(parents=True, exist_ok=True)

    emojis = ['📕', '📗', '📘', '📙', '📔', '📓', '📒', '📚']
    merged = f'---\ndate: {date}\nsource: WaytoAGI每日知识库\nurl: https://waytoagi.feishu.cn/wiki/XjxvwwCZ7ijJMxkJ3SucrVEUn4p\n---\n\n'
    merged += f'# {date} WaytoAGI知识库更新\n\n> 共 {len(tokens)} 篇文章\n\n'

    for i, token in enumerate(tokens, 1):
        print(f'[INFO] 正在导出第 {i}/{len(tokens)} 篇...', file=sys.stderr)
        raw_content = export_doc_to_markdown(token, access_token)
        emoji = emojis[(i - 1) % len(emojis)]
        merged += f'## {emoji} 文章 {i}\n\n> 文档 ID: `{token}`\n\n'
        if raw_content:
            print(f'[INFO] 正在提纯第 {i} 篇...', file=sys.stderr)
            refined = refine_content_with_claude(raw_content, token)
            print(f'[SUCCESS] 第 {i} 篇导出并提纯成功', file=sys.stderr)
        else:
            refined = f'> ⚠️ **文档不可访问（已删除或无权限）**\n> 🔗 原文链接：https://waytoagi.feishu.cn/wiki/{token}\n'
            print(f'[WARN] 第 {i} 篇不可访问，已记录链接', file=sys.stderr)
        merged += refined
        merged += '\n\n---\n\n'

    output_file = output_dir / f'{date}.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged)

    print(f'[INFO] 合并完成！输出文件: {output_file}', file=sys.stderr)
    return output_file


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 generate_daily_report.py <date>', file=sys.stderr)
        sys.exit(1)

    date = sys.argv[1]
    output_dir = BASE_DIR / 'daily'

    print('[INFO] 正在获取 access_token...', file=sys.stderr)
    access_token = get_tenant_access_token()

    output_file = generate_daily_report(date, access_token, output_dir)
    print(f'[SUCCESS] {output_file}', file=sys.stderr)


if __name__ == '__main__':
    main()
