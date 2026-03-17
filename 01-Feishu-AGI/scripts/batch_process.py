#!/usr/bin/env python3
"""
批量处理脚本：每次处理一个日期，支持断点续跑
由 cron 定时调用
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DAILY_DIR = BASE_DIR / 'daily'
INDEX_MAP = BASE_DIR / 'data' / 'index_map.json'
STATE_FILE = BASE_DIR / 'data' / 'extract-state.json'

def load_state():
    if STATE_FILE.exists():
        return json.load(open(STATE_FILE))
    return {'last_processed': None, 'completed': [], 'failed': []}

def save_state(state):
    json.dump(state, open(STATE_FILE, 'w'), indent=2, ensure_ascii=False)

def get_next_date(state):
    """获取下一个待处理的日期（只处理 <= 今天的日期）"""
    data = json.load(open(INDEX_MAP))
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 过滤：只保留 <= 今天的日期
    all_dates = sorted([d for d in data.keys() if d <= today])
    completed = set(state.get('completed', []))
    
    for date in all_dates:
        # 跳过已完成的
        if date in completed:
            continue
        # 跳过已有文件的
        if (DAILY_DIR / f'{date}.md').exists():
            completed.add(date)
            continue
        return date
    
    return None  # 全部处理完毕

def notify(msg):
    """通过 openclaw 发飞书消息给老大"""
    import subprocess
    result = subprocess.run([
        'openclaw', 'message', 'send',
        '--channel', 'feishu',
        '-t', 'user:ou_68f0a760761d15f8e1352eb8a7e0bd0d',
        '-m', msg
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f'[WARN] 通知发送失败: {result.stderr}', file=sys.stderr)

def main():
    state = load_state()
    
    next_date = get_next_date(state)
    
    if next_date is None:
        print('[INFO] 所有日期已处理完毕！')
        # 汇报：没有新数据
        notify('📊 AGI知识库增量采集\n状态：今日无新文章\n时间：' + datetime.now().strftime('%Y-%m-%d %H:%M'))
        return
    
    print(f'[INFO] 正在处理日期: {next_date}')
    
    # 调用 generate_daily_report.py
    script = Path(__file__).parent / 'generate_daily_report.py'
    ret = os.system(f'python3 {script} {next_date}')
    
    if ret == 0 and (DAILY_DIR / f'{next_date}.md').exists():
        # 先做主题分类，再标记完成
        classify_script = Path(__file__).parent / 'classify_topics.py'
        cls_ret = os.system(f'python3 {classify_script} {next_date}')
        if cls_ret != 0:
            state.setdefault('failed', []).append(next_date)
            save_state(state)
            print(f'[ERROR] {next_date} 主题分类失败')
            sys.exit(1)

        state.setdefault('completed', []).append(next_date)
        state['last_processed'] = next_date
        state['last_run'] = datetime.now().isoformat()
        save_state(state)
        print(f'[SUCCESS] {next_date} 处理完成')
        # 汇报：处理成功
        notify(f'✅ AGI知识库增量采集\\n日期：{next_date}\\n状态：处理完成\\n文章数：{len(json.load(open(INDEX_MAP)).get(next_date, []))}篇')
        # 自动推送到 GitHub
        sync_script = BASE_DIR.parent / 'git-sync.sh'
        if sync_script.exists():
            os.system(f'bash {sync_script}')
    else:
        state.setdefault('failed', []).append(next_date)
        save_state(state)
        print(f'[ERROR] {next_date} 处理失败')
        # 汇报：处理失败
        notify(f'❌ AGI知识库增量采集\\n日期：{next_date}\\n状态：处理失败\\n请检查日志')
        sys.exit(1)

if __name__ == '__main__':
    main()
