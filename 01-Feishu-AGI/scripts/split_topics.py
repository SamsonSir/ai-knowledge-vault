#!/usr/bin/env python3
"""
把 topics/ 下的大 md 文件拆分成 topics/<主题>/<文章>.md 的结构
"""

import os
import re
import shutil

TOPICS_DIR = "/home/admin/.openclaw/workspace/01-AI-Knowledge-Vault/01-Feishu-AGI/topics"

def sanitize_filename(name):
    """清理文件名中的非法字符"""
    # 替换 Windows/Linux 不允许的字符
    name = re.sub(r'[<>:"/\\|?*\n\r\t]', '_', name)
    name = name.strip().strip('.')
    # 限制长度
    if len(name) > 100:
        name = name[:100]
    return name or "未命名"

def extract_article_title(content):
    """从文章内容中提取标题（来源字段）"""
    # 匹配 **来源**: XXX | 的格式
    m = re.search(r'\*\*来源\*\*:\s*([^|]+?)(?:\s*\||\s*$)', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # 匹配战略价值作为备用
    m = re.search(r'\*\*战略价值\*\*[:：]\s*(.{10,60}?)(?:[。，\n]|$)', content)
    if m:
        return m.group(1).strip()[:60]
    return None

def split_topic_file(md_path):
    """拆分一个主题 md 文件"""
    topic_name = os.path.splitext(os.path.basename(md_path))[0]
    topic_dir = os.path.join(TOPICS_DIR, topic_name)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按 "## 数字. [日期]" 分割文章
    # 找到所有分割点
    pattern = r'^(## \d+\. \[[\d-]+\].*?)(?=^## \d+\. \[[\d-]+\]|\Z)'
    articles = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
    
    if not articles:
        print(f"  ⚠️  {topic_name}: 未找到文章分割点，跳过")
        return 0
    
    # 创建主题目录
    os.makedirs(topic_dir, exist_ok=True)
    
    count = 0
    used_names = {}
    
    for i, article_content in enumerate(articles):
        # 提取日期（用于备用文件名）
        date_m = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', article_content)
        date_str = date_m.group(1) if date_m else f"article-{i+1}"
        
        # 提取文章标题
        title = extract_article_title(article_content)
        
        if title:
            base_name = sanitize_filename(title)
        else:
            base_name = date_str
        
        # 处理同名文件（同日期多篇）
        if base_name in used_names:
            used_names[base_name] += 1
            file_name = f"{base_name}_{used_names[base_name]}.md"
        else:
            used_names[base_name] = 1
            file_name = f"{base_name}.md"
        
        file_path = os.path.join(topic_dir, file_name)
        
        # 给文章加主题标题头
        full_content = f"# {topic_name}\n\n{article_content.strip()}\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        count += 1
    
    print(f"  ✅ {topic_name}: {count} 篇文章 → {topic_dir}/")
    return count

def main():
    # 找到所有主题 md 文件（直接在 topics/ 下的，不是子目录里的）
    md_files = []
    for name in os.listdir(TOPICS_DIR):
        path = os.path.join(TOPICS_DIR, name)
        if os.path.isfile(path) and name.endswith('.md'):
            md_files.append(path)
    
    if not md_files:
        print("❌ 未找到任何主题 md 文件")
        return
    
    print(f"📂 找到 {len(md_files)} 个主题文件，开始拆分...\n")
    
    total = 0
    for md_path in sorted(md_files):
        total += split_topic_file(md_path)
    
    print(f"\n🎉 完成！共拆分 {total} 篇文章")
    print(f"📁 目录结构: {TOPICS_DIR}/<主题>/<日期_标题>.md")
    
    # 询问是否删除原始大文件（这里自动备份）
    backup_dir = os.path.join(os.path.dirname(TOPICS_DIR), "topics_backup")
    os.makedirs(backup_dir, exist_ok=True)
    for md_path in md_files:
        shutil.move(md_path, os.path.join(backup_dir, os.path.basename(md_path)))
    print(f"\n📦 原始大文件已移至备份目录: {backup_dir}/")

if __name__ == "__main__":
    main()
