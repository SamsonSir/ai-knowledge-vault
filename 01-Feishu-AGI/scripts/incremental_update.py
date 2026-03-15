#!/usr/bin/env python3
"""
增量更新脚本：每天拉取飞书索引页最新 blocks，diff 出新增文章，处理当天数据
由 cron 每天定时调用
"""
import json
import os
import re
import sys
import requests
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
INDEX_MAP = DATA_DIR / 'index_map.json'
STATE_FILE = DATA_DIR / 'extract-state.json'
DAILY_DIR = BASE_DIR / 'daily'

# 飞书索引文档 token（WaytoAGI 每日知识库索引页）
INDEX_DOC_TOKEN = 'XjxvwwCZ7ijJMxkJ3SucrVEUn4p'

FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', 'cli_a90749c404a1dbd6')
FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', 'n9vXbGD1jYmy3U3jQb82afNIUKjJxYdf')


def get_token():
    r = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={'app_id': FEISHU_APP_ID, 'app_secret': FEISHU_APP_SECRET}
    )
    data = r.json()
    if data.get('code') != 0:
        print(f'[ERROR] 获取 token 失败: {data}', file=sys.stderr)
        sys.exit(1)
    return data['tenant_access_token']


def fetch_all_blocks(doc_token, access_token):
    """分页拉取文档所有 blocks"""
    blocks = []
    page_token = None
    while True:
        params = {'page_size': 500}
        if page_token:
            params['page_token'] = page_token
        r = requests.get(
            f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks',
            headers={'Authorization': f'Bearer {access_token}'},
            params=params
        )
        data = r.json()
        if data.get('code') != 0:
            print(f'[ERROR] 拉取 blocks 失败: {data}', file=sys.stderr)
            sys.exit(1)
        items = data.get('data', {}).get('items', [])
        blocks.extend(items)
        if not data.get('data', {}).get('has_more'):
            break
        page_token = data['data'].get('page_token')
    return blocks


def get_block_text(block):
    """从 block 中提取文本内容，支持 text 和 heading 类型"""
    block_type = block.get('block_type')
    if block_type == 2:
        elements = block.get('text', {}).get('elements', [])
        return ''.join(e.get('text_run', {}).get('content', '') for e in elements)
    elif block_type == 3:
        elements = block.get('heading1', {}).get('elements', [])
        return ''.join(e.get('text_run', {}).get('content', '') for e in elements)
    elif block_type == 4:
        elements = block.get('heading2', {}).get('elements', [])
        return ''.join(e.get('text_run', {}).get('content', '') for e in elements)
    elif block_type == 5:
        elements = block.get('heading3', {}).get('elements', [])
        return ''.join(e.get('text_run', {}).get('content', '') for e in elements)
    return ''


def get_block_elements(block):
    """获取 block 中的所有 elements，用于提取 mention_doc"""
    block_type = block.get('block_type')
    if block_type == 2:
        return block.get('text', {}).get('elements', [])
    elif block_type == 3:
        return block.get('heading1', {}).get('elements', [])
    elif block_type == 4:
        return block.get('heading2', {}).get('elements', [])
    elif block_type == 5:
        return block.get('heading3', {}).get('elements', [])
    return []


def parse_index_map(blocks):
    """从 blocks 解析日期->token 映射
    
    结构说明：
    - heading1 (type=3): 日期标题，如 "3月14日收录"
    - text (type=2): 文章标题行，如 "📕 文章名称"（可能包含日期，但不是新日期）
    - text (type=2): 空字符串，但包含 mention_doc 链接
    """
    date_map = {}
    current_date = None
    
    for i, block in enumerate(blocks):
        block_type = block.get('block_type')
        text = get_block_text(block)
        
        # 检测日期标题：**只有 heading1-3 才算日期标题**
        # 普通 text 里的日期（如文章标题"4月8日东京见"）不算新日期
        if block_type in [3, 4, 5] and text:  # heading1, heading2, heading3
            match = re.search(r'(\d+)月(\d+)日', text)
            if match:
                month = match.group(1).zfill(2)
                day = match.group(2).zfill(2)
                current_date = f'2026-{month}-{day}'
                date_map.setdefault(current_date, [])
        
        # 提取文档链接：当前 block 或下一个 block 可能有 mention_doc
        if current_date:
            # 检查当前 block
            elements = get_block_elements(block)
            for elem in elements:
                token = elem.get('mention_doc', {}).get('token')  # 字段名是 token，不是 obj_token
                if token and token not in date_map[current_date]:
                    date_map[current_date].append(token)
            
            # 检查下一个 block（如果是空 text block，可能包含链接）
            if i + 1 < len(blocks):
                next_block = blocks[i + 1]
                next_type = next_block.get('block_type')
                next_text = get_block_text(next_block)
                # 下一个 block 是空的，或者是下一个文章的标题（但不是日期标题）
                if not next_text or (next_type == 2 and not next_text.endswith('收录')):
                    next_elements = get_block_elements(next_block)
                    for elem in next_elements:
                        token = elem.get('mention_doc', {}).get('token')  # 字段名是 token，不是 obj_token
                        if token and token not in date_map[current_date]:
                            date_map[current_date].append(token)
    
    return date_map


def main():
    today = datetime.now().strftime('%Y-%m-%d')
    print(f'[INFO] 增量更新，今天: {today}')

    # 1. 拉取最新索引
    print('[INFO] 拉取飞书索引页...')
    access_token = get_token()
    blocks = fetch_all_blocks(INDEX_DOC_TOKEN, access_token)
    new_map = parse_index_map(blocks)
    print(f'[INFO] 索引页共 {len(new_map)} 个日期')

    # 2. 加载旧 index_map，diff 出新增
    old_map = json.load(open(INDEX_MAP)) if INDEX_MAP.exists() else {}
    old_tokens_today = set(old_map.get(today, []))
    new_tokens_today = set(new_map.get(today, []))
    added = new_tokens_today - old_tokens_today

    if not new_tokens_today:
        print(f'[INFO] 今天 {today} 暂无新文章，退出')
        return

    print(f'[INFO] 今天共 {len(new_tokens_today)} 篇，新增 {len(added)} 篇')

    # 3. 更新 index_map.json（合并新数据）
    old_map[today] = list(new_tokens_today)
    with open(INDEX_MAP, 'w', encoding='utf-8') as f:
        json.dump(old_map, f, ensure_ascii=False, indent=2)
    print('[INFO] index_map.json 已更新')

    # 4. 如果今天已有 daily 文件且有新增，删掉重新生成；否则直接生成
    daily_file = DAILY_DIR / f'{today}.md'
    if daily_file.exists() and added:
        print(f'[INFO] 今天已有文件但有新增，重新生成')
        daily_file.unlink()
        # 从 state completed 里移除今天，让 batch_process 重跑
        state = json.load(open(STATE_FILE)) if STATE_FILE.exists() else {}
        completed = state.get('completed', [])
        if today in completed:
            completed.remove(today)
            state['completed'] = completed
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

    # 5. 调用 batch_process 处理今天
    script = Path(__file__).parent / 'batch_process.py'
    ret = os.system(f'python3 {script}')
    if ret == 0:
        print(f'[SUCCESS] {today} 增量处理完成')
    else:
        print(f'[ERROR] {today} 处理失败', file=sys.stderr)
        sys.exit(1)

    # 6. 主题分类已由 batch_process.py 内部完成，这里不再重复执行
    return


def sanitize_filename(name):
    """清理文件名非法字符，限制长度"""
    name = re.sub(r'[<>:"/\\|?*\n\r\t]', '_', name).strip().strip('.')
    return name[:100] if name else '未命名'


def classify_new_articles(date):
    """对指定日期的新文章做主题分类，每篇写入 topics/<主题>/<标题>.md"""
    daily_file = DAILY_DIR / f'{date}.md'
    if not daily_file.exists():
        return

    # 加载现有分类数据
    cls_file = DATA_DIR / 'classification.json'
    if cls_file.exists():
        cls_data = json.load(open(cls_file, encoding='utf-8'))
    else:
        print('[WARN] classification.json 不存在，跳过主题分类')
        return

    topics = cls_data.get('topics', [])
    classification = cls_data.get('classification', {})
    topics_dir = BASE_DIR / 'topics'
    topics_dir.mkdir(exist_ok=True)

    # 从 daily 文件中按文章分割
    content = daily_file.read_text(encoding='utf-8')
    # 按 "## 🔖 文章 N" 行分割（各种 emoji 变体）
    sections = re.split(r'\n(?=## [^\n]+ 文章 \d+)', content)

    new_articles = []
    for section in sections:
        if '文章' not in section[:30]:
            continue
        title = ''
        strategic = ''
        for line in section.split('\n'):
            if '**来源**' in line and not title:
                title = re.sub(r'\*\*来源\*\*:?\s*', '', line).split('|')[0].strip()
            if '战略价值' in line and not strategic:
                strategic = re.sub(r'\*\*战略价值\*\*[:：]\s*', '', line).strip()
        if title:
            new_articles.append({
                'title': title,
                'strategic': strategic[:100],
                'content': section.strip()
            })

    if not new_articles:
        print(f'[INFO] {date} 未提取到文章，跳过分类')
        return

    # 调用 Claude 做主题分类
    CLAUDE_API_KEY = os.getenv('ANTHROPIC_API_KEY', 'sk-Gr8tCh3atKEdlGJpUGpcPFSCnovO2rgMcWeF4p50zfOoZSIL')
    CLAUDE_BASE_URL = os.getenv('ANTHROPIC_BASE_URL', 'https://www.packyapi.com')

    topics_str = '\n'.join([f'- {t}' for t in topics])
    article_list = '\n'.join([
        f'{j+1}. {a["title"]} | {a["strategic"][:60]}'
        for j, a in enumerate(new_articles)
    ])
    prompt = (
        '将以下文章归类到指定主题，每篇只选一个最匹配的主题。\n\n'
        f'主题列表：\n{topics_str}\n\n'
        '严格输出JSON对象，key为编号字符串（"1","2"...），value为主题名，不要输出其他内容：\n\n'
        f'文章：\n{article_list}'
    )

    api_url = f'{CLAUDE_BASE_URL}/v1/messages'
    headers = {
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    }
    try:
        r = requests.post(api_url, headers=headers, json={
            'model': 'claude-sonnet-4-6',
            'max_tokens': 1000,
            'messages': [{'role': 'user', 'content': prompt}]
        }, timeout=60)
    except Exception as e:
        print(f'[WARN] 主题分类请求异常: {e}')
        return

    if r.status_code != 200:
        print(f'[WARN] 主题分类 API 失败: {r.status_code}')
        return

    new_cls = {}
    for block in r.json().get('content', []):
        if block.get('type') == 'text':
            m = re.search(r'\{[\s\S]+\}', block['text'])
            if m:
                try:
                    new_cls = json.loads(m.group())
                except Exception:
                    pass
                break

    # 每篇文章写入独立文件：topics/<主题>/<标题>.md
    for j, article in enumerate(new_articles):
        topic = new_cls.get(str(j + 1))
        if not topic or topic not in topics:
            print(f'[WARN] 文章 {j+1} 未匹配到有效主题，跳过')
            continue

        topic_dir = topics_dir / topic
        topic_dir.mkdir(exist_ok=True)

        filename = sanitize_filename(article['title']) + '.md'
        file_path = topic_dir / filename

        # 同名文件加日期后缀避免覆盖
        if file_path.exists():
            filename = sanitize_filename(article['title']) + f'_{date}.md'
            file_path = topic_dir / filename

        file_content = f'# {topic}\n\n{article["content"]}\n'
        file_path.write_text(file_content, encoding='utf-8')

        # 更新分类记录
        art_id = f'{date}_{j+1}'
        classification[art_id] = topic
        print(f'[INFO] {article["title"][:40]} → {topic}/{filename}')

    cls_data['classification'] = classification
    with open(cls_file, 'w', encoding='utf-8') as f:
        json.dump(cls_data, f, ensure_ascii=False, indent=2)
    print(f'[SUCCESS] {date} 主题分类完成，{len(new_cls)} 篇')


if __name__ == '__main__':
    main()
