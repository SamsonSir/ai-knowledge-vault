#!/usr/bin/env python3
"""
按日期将 daily/<date>.md 中的文章分类写入 topics/<主题>/<标题>.md
支持重复执行：会先清理该日期已有的 topic 文件，再重新写入。
"""
import json
import os
import re
import sys
from pathlib import Path
import requests

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
DAILY_DIR = BASE_DIR / 'daily'
TOPICS_DIR = BASE_DIR / 'topics'
CLS_FILE = DATA_DIR / 'classification.json'

CLAUDE_API_KEY = os.getenv('ANTHROPIC_API_KEY', 'sk-Gr8tCh3atKEdlGJpUGpcPFSCnovO2rgMcWeF4p50zfOoZSIL')
CLAUDE_BASE_URL = os.getenv('ANTHROPIC_BASE_URL', 'https://www.packyapi.com')


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\n\r\t]', '_', name).strip().strip('.')
    return name[:100] if name else '未命名'


def extract_first_json_object(text: str) -> dict:
    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch != '{':
            continue
        try:
            obj, _ = decoder.raw_decode(text[i:])
            if isinstance(obj, dict):
                return obj
        except Exception:
            continue
    return {}


def load_classification_meta():
    if not CLS_FILE.exists():
        raise FileNotFoundError(f'classification.json 不存在: {CLS_FILE}')
    with open(CLS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_articles_from_daily(date: str):
    daily_file = DAILY_DIR / f'{date}.md'
    if not daily_file.exists():
        raise FileNotFoundError(f'daily 文件不存在: {daily_file}')

    content = daily_file.read_text(encoding='utf-8')
    sections = re.split(r'\n(?=## [^\n]+ 文章 \d+)', content)

    articles = []
    for idx, section in enumerate(sections, 1):
        if '文章' not in section[:30]:
            continue
        title = ''
        strategic = ''
        for line in section.split('\n'):
            if '**来源**' in line and not title:
                title = re.sub(r'\*\*来源\*\*:?[ \t]*', '', line).split('|')[0].strip()
            if '战略价值' in line and not strategic:
                strategic = re.sub(r'\*\*战略价值\*\*[:：]\s*', '', line).strip()
        if title:
            articles.append({
                'index': len(articles) + 1,
                'title': title,
                'strategic': strategic[:100],
                'content': section.strip(),
            })
    return articles


def classify_articles(articles, topics):
    if not articles:
        return {}
    topics_str = '\n'.join([f'- {t}' for t in topics])
    article_list = '\n'.join([
        f'{a["index"]}. {a["title"]} | {a["strategic"][:60]}'
        for a in articles
    ])
    prompt = (
        '将以下文章归类到指定主题，每篇只选一个最匹配的主题。\n\n'
        f'主题列表：\n{topics_str}\n\n'
        '严格输出 JSON 对象，key 为编号字符串（"1","2"...），value 为主题名。不要输出解释，不要输出多段 JSON。\n\n'
        f'文章：\n{article_list}'
    )
    api_url = f'{CLAUDE_BASE_URL}/v1/messages'
    headers = {
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    }
    r = requests.post(api_url, headers=headers, json={
        'model': 'claude-sonnet-4-6',
        'max_tokens': 1000,
        'messages': [{'role': 'user', 'content': prompt}]
    }, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f'主题分类 API 失败: {r.status_code} {r.text[:200]}')
    resp = r.json()
    text = '\n'.join(block.get('text', '') for block in resp.get('content', []) if block.get('type') == 'text')
    return extract_first_json_object(text)


def remove_existing_topic_files_for_date(date: str):
    removed = 0
    if not TOPICS_DIR.exists():
        return removed
    marker = f'**时间**: {date}'
    for path in TOPICS_DIR.rglob('*.md'):
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            continue
        if marker in text:
            path.unlink()
            removed += 1
    return removed


def write_topics(date: str, articles, assignments, meta):
    topics = set(meta.get('topics', []))
    classification = meta.get('classification', {})

    removed = remove_existing_topic_files_for_date(date)
    if removed:
        print(f'[INFO] 已清理 {date} 旧 topic 文件 {removed} 个')

    for article in articles:
        topic = assignments.get(str(article['index']))
        if not topic or topic not in topics:
            print(f'[WARN] 文章 {article["index"]} 未匹配到有效主题，跳过')
            continue

        topic_dir = TOPICS_DIR / topic
        topic_dir.mkdir(parents=True, exist_ok=True)

        filename = sanitize_filename(article['title']) + '.md'
        file_path = topic_dir / filename
        if file_path.exists():
            filename = sanitize_filename(article['title']) + f'_{date}.md'
            file_path = topic_dir / filename

        # 从 topics/<主题>/xxx.md 回到 vault 根目录，需要 ../../_images/
        topic_content = article['content'].replace('../_images/', '../../_images/')
        file_path.write_text(f'# {topic}\n\n{topic_content}\n', encoding='utf-8')

        classification[f'{date}_{article["index"]}'] = topic
        print(f'[INFO] {article["title"][:40]} → {topic}/{filename}')

    meta['classification'] = classification
    with open(CLS_FILE, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 2:
        print('用法: python3 classify_topics.py <YYYY-MM-DD>', file=sys.stderr)
        sys.exit(1)

    date = sys.argv[1]
    meta = load_classification_meta()
    articles = parse_articles_from_daily(date)
    if not articles:
        print(f'[INFO] {date} 未提取到文章，跳过分类')
        return
    assignments = classify_articles(articles, meta.get('topics', []))
    write_topics(date, articles, assignments, meta)
    print(f'[SUCCESS] {date} 主题分类完成，文章 {len(articles)} 篇')


if __name__ == '__main__':
    main()
