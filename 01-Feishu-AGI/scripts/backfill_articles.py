#!/usr/bin/env python3
"""
历史文章回填脚本：按日期重跑 daily 提纯（含图片）并重建 topics。
默认只执行你传入的日期范围；不带参数不执行，避免误跑全量。
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
INDEX_MAP = DATA_DIR / 'index_map.json'


def usage():
    print(
        '用法:\n'
        '  python3 backfill_articles.py <start_date> <end_date> [limit]\n\n'
        '示例:\n'
        '  python3 backfill_articles.py 2026-01-01 2026-01-07\n'
        '  python3 backfill_articles.py 2026-01-01 2026-01-31 5\n',
        file=sys.stderr,
    )


def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) >= 4 else None

    all_dates = sorted(json.load(open(INDEX_MAP, 'r', encoding='utf-8')).keys())
    target_dates = [d for d in all_dates if start_date <= d <= end_date]
    if limit is not None:
        target_dates = target_dates[:limit]

    if not target_dates:
        print('[INFO] 没有匹配到待回填日期')
        return

    print(f'[INFO] 准备回填 {len(target_dates)} 个日期: {target_dates[0]} ~ {target_dates[-1]}')

    gen_script = Path(__file__).parent / 'generate_daily_report.py'
    cls_script = Path(__file__).parent / 'classify_topics.py'
    sync_script = BASE_DIR.parent / 'git-sync.sh'

    for idx, date in enumerate(target_dates, 1):
        print(f'\n[INFO] ({idx}/{len(target_dates)}) 回填 {date}')
        ret1 = os.system(f'python3 {gen_script} {date}')
        if ret1 != 0:
            print(f'[ERROR] {date} 提纯失败')
            sys.exit(1)

        ret2 = os.system(f'python3 {cls_script} {date}')
        if ret2 != 0:
            print(f'[ERROR] {date} 主题分类失败')
            sys.exit(1)

        if sync_script.exists():
            os.system(f'bash {sync_script}')

    print('\n[SUCCESS] 历史回填完成')


if __name__ == '__main__':
    main()
