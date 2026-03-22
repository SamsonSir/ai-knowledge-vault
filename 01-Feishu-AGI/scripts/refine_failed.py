#!/usr/bin/env python3
"""
提纯补全脚本：扫描 daily/*.md 中因 API 失败而跳过提纯的文章，重新提纯替换。
用法: python3 refine_failed.py [--dry-run]
"""
import json, re, sys, os, time
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DAILY_DIR = BASE_DIR / 'daily'
DATA_DIR = BASE_DIR / 'data'

# 复用 generate_daily_report 的提纯函数
sys.path.insert(0, str(Path(__file__).parent))
from generate_daily_report import refine_content_with_kimi, export_doc_to_markdown, get_tenant_access_token

PATTERN = r'⚠️ \*\*(?:API 多次重试失败|文章内容过长).*?\*\*'
PATTERN_LINK = r'文档 ID: `([^`]+)`'


def main():
    dry_run = '--dry-run' in sys.argv
    
    access_token = get_tenant_access_token()
    fixed = 0
    still_failed = 0
    
    for md_file in sorted(DAILY_DIR.glob('*.md')):
        content = md_file.read_text(encoding='utf-8')
        
        # 找出所有需要重新提纯的文章段
        # 按文章分割（---分隔）
        articles = re.split(r'\n---\n', content)
        updated_articles = []
        changed = False
        
        for article in articles:
            if 'API 多次重试失败' not in article:
                updated_articles.append(article)
                continue
            
            # 提取 doc_token
            m = re.search(PATTERN_LINK, article)
            if not m:
                updated_articles.append(article)
                continue
            token = m.group(1)
            
            print(f'[INFO] 发现未提纯文章: {token} (in {md_file.name})')
            
            if dry_run:
                updated_articles.append(article)
                continue
            
            # 重新提纯
            try:
                raw = export_doc_to_markdown(token, access_token)
                if raw:
                    refined = refine_content_with_kimi(raw, token)
                    if 'API 多次重试失败' not in refined:
                        updated_articles.append(refined)
                        fixed += 1
                        changed = True
                        print(f'[SUCCESS] 提纯成功: {token}')
                        time.sleep(1)  # 避免API限流
                    else:
                        updated_articles.append(article)
                        still_failed += 1
                        print(f'[WARN] 再次失败: {token}')
                else:
                    updated_articles.append(article)
                    print(f'[WARN] 文档不可访问: {token}')
            except Exception as e:
                updated_articles.append(article)
                print(f'[ERROR] {token}: {e}')
        
        if changed:
            md_file.write_text('\n---\n'.join(updated_articles), encoding='utf-8')
            print(f'[INFO] 更新: {md_file.name}')
    
    print(f'\n{"="*40}')
    if dry_run:
        print('[DRY RUN] 仅扫描，未做修改')
    print(f'提纯成功: {fixed}')
    print(f'仍然失败: {still_failed}')


if __name__ == '__main__':
    main()
