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


def read_shell_export(name):
    """从 ~/.bashrc ~/.zshrc 读取 export 变量，解决非登录 shell 取不到环境变量的问题"""
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
CLAUDE_FALLBACK_API_KEY = 'sk-OMY2hTJgwKGLkQQlKDbgnhZVhT7KYyC8B886pIoc2gR0Mcvj'
CLAUDE_FALLBACK_BASE_URL = 'https://www.packyapi.com'

# 超长文章阈值
MAX_CHARS = 25000

# 广告/引流语义关键词（命中时过滤）
AD_CONTEXT_KEYWORDS = [
    '扫码', '二维码', '关注公众号', '公众号', '关注我们', '加群', '进群', '社群', '微信群',
    '福利领取', '领取福利', '抽奖', '报名', '海报', '转发', '点赞', '私信', '商务合作',
    '推广', '赞助', '课程咨询', '下载app', '联系客服', '添加微信', 'vx', '微信咨询',
    '长按识别', '识别二维码', '点击关注', '立即领取', '免费领取', '限时福利',
    '专属福利', '扫码添加', '扫码进群', '微信扫码', '加我微信', '优惠券', '折扣码',
    '邀请码', '推荐码', '扫码领取', '关注后回复', '广告', '赞助商', '合作推广',
    '关注有礼', '关注送', '扫码送', '扫码得', '免费领', '限时领',
    '特惠', '促销', '打折', '立减', '满减', '拼团', '砍价',
    '会员', 'vip', '充值', '付费', '订阅', '购买', '下单',
    '联系我', '找我们', '咨询我', '私聊', '私信我',
    '训练营', '培训班', '课程', '教程售卖', '资料包', '学习资料'
]

# 正文图片常见语义（命中时才保留，默认过滤）
# 重点：操作流程、步骤、技巧、知识点、结果、图解原理
CONTENT_IMAGE_KEYWORDS = [
    # 操作与流程
    '操作流程', '操作步骤', '步骤说明', '操作指南', '使用教程', '配置教程',
    '流程图', '步骤图', '操作演示', '使用演示', '配置演示',
    '点击', '选择', '输入', '设置', '配置', '保存', '提交', '确认',
    '第一步', '第二步', '第三步', '最后一步', '完成',
    
    # 界面与截图
    '如下图', '见下图', '上图', '下图', '截图所示', '如图所示', '界面截图',
    '界面展示', '页面效果', '界面效果', 'UI界面', '操作界面', '配置界面',
    
    # 技巧与知识点
    '技巧', '小窍门', '实用技巧', '关键技巧', '核心技巧',
    '知识点', '核心概念', '关键概念', '重要概念', '原理说明',
    '注意事项', '重要提示', '关键要点', '核心要点',
    
    # 结果与效果
    '生成结果', '输出结果', '运行结果', '执行结果', '最终效果', '效果展示',
    '前后对比', '效果对比', '性能对比', '对比图', '优化效果', '提升效果',
    '测试报告', '测试结果', '实验数据', '数据统计',
    
    # 架构与图表
    '架构图', '系统架构', '技术架构', '架构设计', '系统结构', '模块结构',
    '图表', '数据图表', '统计图', '趋势图', '折线图', '柱状图', '饼图',
    '思维导图', '脑图', '关系图',
    
    # 案例与示例
    '案例图', '实际案例', '真实案例', '项目案例', '实战案例', '最佳实践',
    '示例图', '代码示例', '示例代码', '演示代码', '配置示例', '使用示例',
    '效果图', '示意图', '说明图', '原理图', '结构图',
    
    # 产品与界面设计
    '产品图', '产品设计', '界面设计', 'UI设计', '原型图', '设计稿',
    '封面图', '文章封面', '头图', '题图', '配图', '相关配图',
    
    # 图解与原理（新增）
    '图解', '一图看懂', '一张图', '秒懂', '快速理解',
    '原理', '工作原理', '实现原理', '核心原理', '底层原理',
    '机制', '实现机制', '运行机制', '核心机制',
    '结构', '组成结构', '内部结构', '层次结构',
    '关系', '逻辑关系', '调用关系', '依赖关系', '关联关系',
    '演变', '发展过程', '演进过程', '变化过程',
    '分类', '类型划分', '分类说明', '种类对比',
    '层次', '层级', '分层', '架构层次', '系统层次',
    '模型', '模型图', '模型结构', '模型示意图',
    '框架', '框架图', '技术框架', '系统框架',
    '具象化', '可视化', '形象化', '直观展示', '直观理解'
]

REFINE_PROMPT = """你是 JokerSu 的首席 AGI 架构师。你的任务是将原文「脱水」并重构成一份「看后即能操作」的战术手册。

⚠️ 重要约束（必须严格遵守）：
1. 你只能输出文本，严禁调用任何工具（包括 WebFetch、搜索等）。
2. 文章中所有以 `__URL__` 开头的链接，必须原样保留 `__URL__` 前缀，不得删除或修改。例如：`__URL__mp.weixin.qq.com/s/xxx` 必须原样输出为 `__URL__mp.weixin.qq.com/s/xxx`。
3. 文章中所有 `[[IMAGE_n]]` 都是正文图片占位符，必须严格保留在原位置：
   - 占位符在原文中的位置代表了图片该出现的位置，你必须让它保留在提纯后文本的对应位置。
   - 如果这张图是正文相关配图，必须原样保留该占位符，且位置必须与原文一致，严禁把所有图片集中到文章开头。
   - 如果这张图明显是广告图、二维码、推广图、公众号引流图，可以直接删除对应占位符。
   - 禁止把 `[[IMAGE_n]]` 改写成别的格式，禁止移动占位符位置。

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
    """过滤明显广告/二维码/小图标，默认过滤，只有强正文信号才保留"""
    name = (image.get('name') or '').lower()
    width = int(image.get('width') or 0)
    height = int(image.get('height') or 0)
    context = (context_text or '').lower()

    # 1) 文件名强信号：明确二维码/图标/logo/头像/广告
    hard_bad_name_keywords = ['qrcode', 'qr_code', 'qr-', 'logo', 'avatar', 'icon', 'wechat', 'wx', 'mp', 'ad', 'banner', 'coupon']
    if any(k in name for k in hard_bad_name_keywords):
        return False

    # 2) 太小的一般不是正文图
    if width and height and (width <= 200 or height <= 200):
        return False
    if width and height and max(width, height) < 280:
        return False

    # 3) 广告图常见尺寸特征：正方形或超高瘦
    square_like = width and height and abs(width - height) <= min(width, height) * 0.25
    very_tall = width and height and height / max(width, 1) >= 2.5
    very_wide = width and height and width / max(height, 1) >= 3.0
    if square_like or very_tall or very_wide:
        # 如果是广告上下文，直接过滤
        if any(k in context for k in AD_CONTEXT_KEYWORDS):
            return False

    # 4) 上下文出现明确正文配图语义，才保留
    if any(k in context for k in CONTENT_IMAGE_KEYWORDS):
        return True

    # 5) 上下文出现强广告/引流语义，过滤
    if any(k in context for k in AD_CONTEXT_KEYWORDS):
        return False

    # 6) 默认过滤，没有明确正文信号的都不要
    return False


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

    for attempt, (base_url, api_key) in enumerate([
        (CLAUDE_BASE_URL, CLAUDE_API_KEY),
        (CLAUDE_FALLBACK_BASE_URL, CLAUDE_FALLBACK_API_KEY),
        (CLAUDE_FALLBACK_BASE_URL, CLAUDE_FALLBACK_API_KEY),
    ], 1):
        try:
            api_url = f'{base_url}/v1/messages'
            headers['x-api-key'] = api_key
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

    # 如果模型把占位符都丢了，我们在文章末尾补一个图片汇总区块，而不是堆在开头
    if not placeholder_nums:
        print(f'[WARN] 未找到图片占位符，在文章末尾追加图片', file=sys.stderr)
        placeholder_nums = list(range(1, len(images) + 1))
        image_block = '\n'.join(f'[[IMAGE_{n}]]' for n in placeholder_nums)
        markdown = markdown.rstrip() + '\n\n### 📎 本文配图\n\n' + image_block + '\n'

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
