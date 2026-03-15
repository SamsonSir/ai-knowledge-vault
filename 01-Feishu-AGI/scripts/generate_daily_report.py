#!/usr/bin/env python3
"""
生成单个日期的合并日报 Markdown
将该日期的所有日报合并到一个文件中
使用 Claude Sonnet 提纯内容，并尽量保留正文图片（过滤广告/二维码类图片）
"""
import json
import sys
import os
import re
import time
import signal
import subprocess
import tempfile
import mimetypes
import requests
from pathlib import Path


def timeout_handler(signum, frame):
    print('[ERROR] 请求超时，强制退出', file=sys.stderr)
    sys.exit(1)


# 设置全局超时 300 秒
signal.signal(signal.SIGALRM, timeout_handler)

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
IMAGES_DIR = BASE_DIR / '_images'
HELPER_SCRIPT = BASE_DIR / 'scripts' / 'download_wiki_images.js'

# 飞书 API 凭证
FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', 'cli_a90749c404a1dbd6')
FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', 'n9vXbGD1jYmy3U3jQb82afNIUKjJxYdf')

# Claude API 配置
CLAUDE_API_KEY = os.getenv('ANTHROPIC_API_KEY', 'sk-Gr8tCh3atKEdlGJpUGpcPFSCnovO2rgMcWeF4p50zfOoZSIL')
CLAUDE_API_KEY_BACKUP = 'sk-OMY2hTJgwKGLkQQlKDbgnhZVhT7KYyC8B886pIoc2gR0Mcvj'
CLAUDE_BASE_URL = os.getenv('ANTHROPIC_BASE_URL', 'https://www.packyapi.com')

# 超长文章阈值
MAX_CHARS = 25000

# 广告/引流语义关键词（强信号才过滤，避免误杀正文图）
AD_CONTEXT_KEYWORDS = [
    '扫码', '二维码', '关注公众号', '公众号', '关注我们', '加群', '进群', '社群',
    '福利领取', '领取福利', '抽奖', '报名', '海报', '转发', '点赞', '私信', '商务合作',
    '推广', '赞助', '课程咨询', '下载app', '联系客服', '添加微信', 'vx', '微信咨询'
]

# 正文图片常见语义（命中时优先保留）
CONTENT_IMAGE_KEYWORDS = [
    '如下图', '见下图', '上图', '下图', '截图', '界面', '效果图', '示意图',
    '流程图', '架构图', '图表', '案例图', '演示图', '生成结果', '作品示例',
    '对比图', '产品图', '海报生成', '封面图', '配图'
]

REFINE_PROMPT = """你是 JokerSu 的首席 AGI 架构师。你的任务是将原文「脱水」并重构成一份「看后即能操作」的战术手册。

⚠️ 重要约束（必须严格遵守）：
1. 你只能输出文本，严禁调用任何工具（包括 WebFetch、搜索等）。
2. 文章中所有以 `__URL__` 开头的链接，必须原样保留 `__URL__` 前缀，不得删除或修改。例如：`__URL__mp.weixin.qq.com/s/xxx` 必须原样输出为 `__URL__mp.weixin.qq.com/s/xxx`。
3. 文章中所有 `[[IMAGE_n]]` 都是正文图片占位符：
   - 如果这张图是正文相关配图，就必须保留该占位符，且占位符文本必须原样输出，不能改写。
   - 如果这张图明显是广告图、二维码、推广图、公众号引流图，可以直接删除对应占位符。
   - 禁止把 `[[IMAGE_n]]` 改写成别的格式。

## 🚨 严禁触碰的红线
- 禁止概括：严禁出现"文章介绍了..."、"作者认为..."等废话。直接输出干货。
- 禁止丢失颗粒度：如果原文有 10 个步骤，你提纯后必须有 10 个步骤。丢失核心步骤视为失职。
- 禁止过度精简：提纯后的内容不得低于原文 60% 的字数，且必须包含所有具体的代码、参数、配置项、数据、案例。
- 核心分析和核心逻辑必须是"干货"不是"摘要"：
  * 核心逻辑至少 8-10 个要点，每个要点必须是可操作的具体细节
  * 严禁泛泛而谈，必须有具体的数字、时间、人名、产品名、操作步骤
- 过滤广告内容：去掉所有广告图片、推广链接、营销文案。
- 去掉具体价格：不需要保留具体的价格信息（如 $20/月、99元等）。

## 📐 萃取深度标准
1. 关键洞察：必须解释「为什么」。不仅要有结论，还要有逻辑支撑（原因 -> 动作 -> 结果）。
2. 工业级 SOP：必须达到「复刻级」精度。包含具体的命令、配置代码块、UI 路径、参数数值。
3. 表格化思维：只要有对比、列表、分类，必须使用 Markdown 表格。
4. 保留原文的所有关键细节：具体的数字、时间、人名、产品名、技术栈、配置参数、Prompt 模板、代码片段。
5. 过滤广告：去掉所有广告图片、推广链接、营销文案、二维码、公众号推广等内容。

## 📝 输出结构模板

**来源**: [文章标题] | **时间**: YYYY-MM-DD | **原文链接**: [URL]

### 📋 核心分析
**战略价值**: {一句话说清楚这篇文章的核心价值}

**核心逻辑**:（至少 8-10 个要点，每个要点必须包含具体的数据、案例、方法论）
- {要点1}
- {要点2}
- ...

### 🎯 关键洞察（如适用）
{深入分析，包含具体的案例、数据、逻辑推导过程}

### 📦 配置/工具详表 (如适用)
| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|

### 🛠️ 操作流程 (如适用)
1. **准备阶段**: {详细细节}
2. **核心执行**: {详细细节}
3. **验证与优化**: {详细细节}

### 💡 具体案例/数据（如适用）
{保留原文中的所有具体案例、数据、实验结果}

### 📝 避坑指南 (如适用)
- ⚠️ {坑点1}

### 🏷️ 行业标签
#标签1 #标签2 #标签3

---

现在请按照以上协议提纯以下文章：

"""


def get_tenant_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    r = requests.post(url, json={'app_id': FEISHU_APP_ID, 'app_secret': FEISHU_APP_SECRET}, timeout=30)
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


def fetch_all_blocks(doc_token, access_token):
    """分页拉取文档所有 blocks，用于提取图片 token"""
    blocks = []
    page_token = None
    while True:
        params = {'page_size': 500}
        if page_token:
            params['page_token'] = page_token
        r = requests.get(
            f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks',
            headers={'Authorization': f'Bearer {access_token}'},
            params=params,
            timeout=60,
        )
        data = r.json()
        if data.get('code') != 0:
            print(f'[WARN] 拉取 blocks 失败 ({doc_token}): {data}', file=sys.stderr)
            return []
        items = data.get('data', {}).get('items', [])
        blocks.extend(items)
        if not data.get('data', {}).get('has_more'):
            break
        page_token = data['data'].get('page_token')
    return blocks


def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*\n\r\t]', '_', name).strip().strip('.')
    return name[:120] if name else 'untitled'


def ext_from_image_info(image):
    name = image.get('name') or ''
    ext = Path(name).suffix.lower()
    if ext:
        return ext
    mime = (image.get('mimeType') or '').lower()
    if 'jpeg' in mime or 'jpg' in mime:
        return '.jpg'
    if 'webp' in mime:
        return '.webp'
    if 'gif' in mime:
        return '.gif'
    return '.png'


def extract_image_blocks(blocks):
    images = []
    for block in blocks:
        image = block.get('image') or {}
        token = image.get('token')
        if not token:
            continue
        images.append({
            'block_id': block.get('block_id'),
            'token': token,
            'width': int(image.get('width') or 0),
            'height': int(image.get('height') or 0),
            'name': image.get('name') or f'{token}.png',
            'mimeType': image.get('mimeType') or 'image/png',
        })
    return images


def should_keep_image(image, context_text=''):
    """过滤明显广告/二维码/小图标，默认尽量保留正文图"""
    name = (image.get('name') or '').lower()
    width = int(image.get('width') or 0)
    height = int(image.get('height') or 0)
    context = (context_text or '').lower()

    # 1) 文件名强信号：明确二维码/图标/logo 才过滤
    hard_bad_name_keywords = ['qrcode', 'qr_code', 'qr-', 'logo', 'avatar', 'icon']
    if any(k in name for k in hard_bad_name_keywords):
        return False

    # 2) 太小的一般不是正文图
    if width and height and width <= 180 and height <= 180:
        return False
    if width and height and max(width, height) < 220:
        return False

    # 3) 上下文出现明确正文配图语义，优先保留
    if any(k in context for k in CONTENT_IMAGE_KEYWORDS):
        return True

    # 4) 上下文出现强广告/引流语义，再结合尺寸过滤
    has_ad_context = any(k in context for k in AD_CONTEXT_KEYWORDS)
    square_like = width and height and abs(width - height) <= min(width, height) * 0.18
    very_tall = width and height and height / max(width, 1) >= 2.8
    if has_ad_context and (square_like or very_tall or max(width, height) <= 480):
        return False

    # 5) 默认保留，宁可多保留一张，也别误杀正文图
    return True


def inject_image_placeholders(raw_content, images):
    """把 raw_content 中的图片文件名替换成正文图片占位符"""
    if not raw_content:
        return raw_content, []

    filename_line = re.compile(r'^\s*[^/\\\n]+\.(png|jpg|jpeg|gif|webp)\s*$', re.I)
    lines = raw_content.splitlines()
    new_lines = []
    kept_images = []
    image_idx = 0

    for idx, line in enumerate(lines):
        if filename_line.match(line.strip()):
            if image_idx < len(images):
                img = images[image_idx]
                image_idx += 1
                context_window = '\n'.join(lines[max(0, idx - 5): min(len(lines), idx + 6)])
                if should_keep_image(img, context_window):
                    kept_images.append(img)
                    new_lines.append(f'[[IMAGE_{len(kept_images)}]]')
                # 广告/二维码图：直接跳过，不写入正文
            else:
                # 没匹配上块信息，保守起见丢弃这类孤立文件名行
                continue
        else:
            new_lines.append(line)

    return '\n'.join(new_lines), kept_images


def load_index_map():
    index_file = DATA_DIR / 'index_map.json'
    if not index_file.exists():
        print(f'[ERROR] index_map.json 不存在: {index_file}', file=sys.stderr)
        sys.exit(1)
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def sanitize_urls(content):
    """把 https?:// 替换为占位符，防止 Claude 触发 WebFetch"""
    return re.sub(r'https?://', '__URL__', content)


def restore_urls(content):
    """把占位符还原为 https://"""
    return content.replace('__URL__', 'https://')


def refine_content_with_claude(content, doc_token):
    """使用 Claude Sonnet 按架构师级协议提纯内容，最多重试 3 次"""

    # 超长文章直接跳过
    if len(content) > MAX_CHARS:
        print(f'[INFO] 文章过长（{len(content)} 字符），跳过提纯并记录链接', file=sys.stderr)
        return f'> ⚠️ **文章内容过长（约 {len(content)} 字符），已跳过自动提纯。**\n> 🔗 原文链接：https://waytoagi.feishu.cn/wiki/{doc_token}\n'

    sanitized = sanitize_urls(content)

    api_url = f'{CLAUDE_BASE_URL}/v1/messages'
    headers = {
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    }
    payload = {
        'model': 'claude-sonnet-4-6',
        'max_tokens': 16000,
        'messages': [{'role': 'user', 'content': REFINE_PROMPT + sanitized}]
    }

    for attempt in range(1, 4):
        current_key = CLAUDE_API_KEY if attempt < 3 else CLAUDE_API_KEY_BACKUP
        try:
            headers['x-api-key'] = current_key
            r = requests.post(api_url, headers=headers, json=payload, timeout=120)
            if r.status_code == 200 and r.text.strip():
                data = r.json()
                text_blocks = [b['text'] for b in data.get('content', []) if b.get('type') == 'text']
                if text_blocks:
                    return restore_urls('\n'.join(text_blocks))
                char_count = len(content)
                print(f'[WARN] Claude 触发工具调用（原文仅 {char_count} 字符），记录链接', file=sys.stderr)
                return f'> ⚠️ **原文内容过少（仅 {char_count} 字符），无有效内容可提纯。**\n> 🔗 原文链接：https://waytoagi.feishu.cn/wiki/{doc_token}\n'
            print(f'[WARN] 第 {attempt} 次尝试失败（状态码 {r.status_code}），重试...', file=sys.stderr)
        except Exception as e:
            print(f'[WARN] 第 {attempt} 次尝试异常: {e}，重试...', file=sys.stderr)
        time.sleep(2)

    return f'> ⚠️ **API 多次重试失败，已跳过自动提纯。**\n> 🔗 原文链接：https://waytoagi.feishu.cn/wiki/{doc_token}\n'


def download_wiki_images(doc_token, date, images):
    """通过浏览器上下文下载公开 wiki 页的正文图片"""
    if not images:
        return {}

    out_dir = IMAGES_DIR / date
    out_dir.mkdir(parents=True, exist_ok=True)

    jobs = {'out_dir': str(out_dir), 'images': []}
    for img in images:
        ext = ext_from_image_info(img)
        stem = sanitize_filename(Path(img.get('name') or img['token']).stem) or img['token']
        filename = f'{stem}_{img["token"][:8]}{ext}'
        jobs['images'].append({
            'token': img['token'],
            'name': img.get('name') or filename,
            'filename': filename,
        })

    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as tf:
        json.dump(jobs, tf, ensure_ascii=False)
        temp_json = tf.name

    try:
        proc = subprocess.run(
            ['node', str(HELPER_SCRIPT), doc_token, temp_json],
            capture_output=True,
            text=True,
            timeout=240,
        )
        if proc.returncode != 0:
            print(f'[WARN] 图片下载脚本失败: {proc.stderr[:800]}', file=sys.stderr)
            return {}
        data = json.loads(proc.stdout.strip())
        result_map = {}
        for item in data.get('results', []):
            if item.get('ok'):
                result_map[item['token']] = item['saved_path']
            else:
                print(f'[WARN] 图片下载失败 {item.get("token")}: {item.get("error")}', file=sys.stderr)
        return result_map
    except Exception as e:
        print(f'[WARN] 执行图片下载脚本异常: {e}', file=sys.stderr)
        return {}
    finally:
        try:
            os.unlink(temp_json)
        except OSError:
            pass


def materialize_images(markdown, doc_token, date, images):
    """把 [[IMAGE_n]] 占位符替换为本地 Markdown 图片链接"""
    if not images:
        return markdown

    placeholder_nums = sorted({int(x) for x in re.findall(r'\[\[IMAGE_(\d+)\]\]', markdown)})

    # 如果模型把所有图片都丢了，但文档里明明有正文图，则强行补到来源行后面
    if not placeholder_nums:
        placeholder_nums = list(range(1, len(images) + 1))
        image_block = '\n'.join(f'[[IMAGE_{n}]]' for n in placeholder_nums)
        source_line = re.search(r'^(\*\*来源\*\*.*)$', markdown, re.M)
        if source_line:
            insert_at = source_line.end()
            markdown = markdown[:insert_at] + '\n\n' + image_block + '\n' + markdown[insert_at:]
        else:
            markdown = image_block + '\n\n' + markdown

    selected_images = [images[n - 1] for n in placeholder_nums if 1 <= n <= len(images)]
    downloads = download_wiki_images(doc_token, date, selected_images)

    for n in placeholder_nums:
        placeholder = f'[[IMAGE_{n}]]'
        if not (1 <= n <= len(images)):
            markdown = markdown.replace(placeholder, '')
            continue
        img = images[n - 1]
        saved_path = downloads.get(img['token'])
        if not saved_path:
            markdown = markdown.replace(placeholder, '')
            continue
        rel_path = f'../_images/{date}/{Path(saved_path).name}'
        markdown = markdown.replace(placeholder, f'![]({rel_path})')

    markdown = re.sub(r'\n{3,}', '\n\n', markdown).strip() + '\n'
    return markdown


def generate_daily_report(date, access_token, output_dir):
    index_map = load_index_map()
    if date not in index_map:
        print(f'[ERROR] {date} 没有日报', file=sys.stderr)
        sys.exit(1)

    tokens = index_map[date]
    print(f'[INFO] {date} 共有 {len(tokens)} 篇日报', file=sys.stderr)

    output_dir.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    emojis = ['📕', '📗', '📘', '📙', '📔', '📓', '📒', '📚']
    merged = f'---\ndate: {date}\nsource: WaytoAGI每日知识库\nurl: https://waytoagi.feishu.cn/wiki/XjxvwwCZ7ijJMxkJ3SucrVEUn4p\n---\n\n'
    merged += f'# {date} WaytoAGI知识库更新\n\n> 共 {len(tokens)} 篇文章\n\n'

    for i, token in enumerate(tokens, 1):
        print(f'[INFO] 正在导出第 {i}/{len(tokens)} 篇...', file=sys.stderr)
        raw_content = export_doc_to_markdown(token, access_token)
        emoji = emojis[(i - 1) % len(emojis)]
        merged += f'## {emoji} 文章 {i}\n\n> 文档 ID: `{token}`\n\n'
        if raw_content:
            blocks = fetch_all_blocks(token, access_token)
            images = extract_image_blocks(blocks)
            prepared_content, kept_images = inject_image_placeholders(raw_content, images)
            print(f'[INFO] 第 {i} 篇检测到图片 {len(images)} 张，保留候选 {len(kept_images)} 张', file=sys.stderr)
            print(f'[INFO] 正在提纯第 {i} 篇...', file=sys.stderr)
            refined = refine_content_with_claude(prepared_content, token)
            refined = materialize_images(refined, token, date, kept_images)
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
