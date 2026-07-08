"""
武林外传剧本 — 台词提取脚本
解析 .docm 文件，提取符合答案之书要求的台词候选。
"""

import zipfile
import xml.etree.ElementTree as ET
import re
import json
import os
from pathlib import Path

# ====== 配置（来源：categories.json） ======
BASE_DIR = Path(__file__).parent
SCRIPT_FILE = BASE_DIR / "武林外传电视剧版剧本.docx"
CATEGORIES_FILE = BASE_DIR / "categories.json"
OUTPUT_FILE = BASE_DIR / "extracted_quotes.json"

# 已知角色名列表（从剧本中识别）
CHARACTER_NAMES = [
    "佟湘玉", "白展堂", "郭芙蓉", "吕轻侯", "莫小贝", "祝无双",
    "李大嘴", "邢捕头", "燕小六", "展红绫", "钱掌柜", "钱夫人",
    "佟伯达", "郭巨侠", "慕容嫣", "慕容子", "赛貂蝉", "金镶玉",
    "杨蕙兰", "杜子俊", "岳松涛", "韩娟", "白眉先生", "丐帮帮主",
    "郭蔷薇", "柳星雨", "柳月云", "扈十娘", "雷老五", "窦先生",
    "白翠萍", "一点红", "平谷一点红", "追风", "姜大娘", "谢步东",
    "公孙乌龙", "姬无命", "姬无病", "上官云", "凌腾云", "范大娘",
    "断指轩辕", "江小道", "包大仁", "展堂", "南宫残花", "清风",
    "明月", "老何", "小米", "小翠", "小卉",
]

# 需要过滤的无意义短句模式
FILTER_PATTERNS = [
    r'^[啊哎唉哦嗯嘿哼哈咦嘘啧]+$',  # 纯语气词
    r'^[。，！？、；：""''…]+$',     # 纯标点
    r'^[\d\s一二三四五六七八九十]+$',  # 纯数字
    r'^[（(].*[）)]$',                # 纯括号内动作
]

# 剧本中常见的非台词角色标记
NON_CHARACTER_MARKERS = [
    "旁白", "字幕", "画外音", "片头", "片尾", "广告", "预告",
    "第一回", "第二回", "第三回", "第四回", "第五回",
    "第六回", "第七回", "第八回", "第九回", "第十回",
    "歌曲", "插曲", "音乐", "音效",
]


def parse_docx_xml(filepath: Path) -> list[str]:
    """解析 .docx/.docm 文件，提取所有段落文本"""
    with zipfile.ZipFile(filepath, 'r') as z:
        xml_content = z.read('word/document.xml')

    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    tree = ET.fromstring(xml_content)

    paragraphs = []
    for p in tree.iter(f'{{{ns}}}p'):
        texts = []
        for t in p.iter(f'{{{ns}}}t'):
            if t.text:
                texts.append(t.text)
        line = ''.join(texts).strip()
        if line:
            paragraphs.append(line)

    return paragraphs


def find_episode_boundaries(paragraphs: list[str]) -> list[tuple[int, int, str]]:
    """找到每一回的起止位置，按段落索引排序"""
    ep_pattern = re.compile(r'^第[一二三四五六七八九十百零\d]+回\s')

    # 收集所有正文中的回目标记
    starts = []
    for i, p in enumerate(paragraphs):
        if i > 60 and ep_pattern.match(p) and len(p) < 80:
            starts.append((i, p))

    # 按段落索引排序（文档中章节顺序不是数字顺序）
    starts.sort(key=lambda x: x[0])

    episodes = []
    for idx, (start, title) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(paragraphs)
        episodes.append((start, end, title))

    return episodes


def filter_episodes_by_number(episodes: list, target_numbers: list[int]) -> list:
    """按回目数字筛选指定集数"""
    result = []
    ep_num_pattern = re.compile(r'第([一二三四五六七八九十百零\d]+)回')
    chinese_to_int = {
        '一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10
    }

    for ep in episodes:
        match = ep_num_pattern.search(ep[2])
        if match:
            num_str = match.group(1)
            num = chinese_to_int.get(num_str) if num_str in chinese_to_int else None
            if num in target_numbers:
                result.append(ep)

    # 按回目数字排序（不是段落索引）
    result.sort(key=lambda e: target_numbers.index(
        chinese_to_int.get(ep_num_pattern.search(e[2]).group(1), 0)
        if ep_num_pattern.search(e[2]) else 0
    ))
    return result


def is_dialogue_line(line: str) -> tuple[str, str] | None:
    """检查是否为 角色名：台词 格式，返回 (角色, 台词) 或 None"""
    for name in CHARACTER_NAMES:
        # 匹配 "角色名：台词" 或 "角色名:台词" 或 "角色名：(动作)台词"
        if line.startswith(name + '：') or line.startswith(name + ':'):
            rest = line[len(name) + 1:].strip()
            return (name, rest)
    return None


def clean_quote(text: str) -> str:
    """清洗台词：去除括号内动作描述、前后空白"""
    if not text:
        return ""
    # 去除开头的括号动作 "（咬牙）台词" → "台词"
    text = re.sub(r'^[（(][^）)]*[）)]\s*', '', text)
    # 去除中间的括号动作 "台词（笑）台词" → "台词台词"
    text = re.sub(r'[（(][^）)]*[）)]', '', text)
    # 去除结尾的括号动作
    text = re.sub(r'\s*[（(][^）)]*[）)]$', '', text)
    # 去除纯动作描述（整句在括号内）
    text = text.strip()
    return text


def should_filter(text: str) -> bool:
    """过滤无意义的台词"""
    if not text or len(text) < 4:
        return True
    # 纯语气词
    for pattern in FILTER_PATTERNS:
        if re.match(pattern, text):
            return True
    # 太长的台词（超过100字的不适合做答案）
    if len(text) > 100:
        return True
    # 以 "你" "我" "他" 开头且太短的，往往是日常对话
    # 保留，不过滤 —— 很多哲理句以 "你" "我" 开头
    return False


def extract_quotes(paragraphs: list[str], target_episodes: list[int] | None = None) -> list[dict]:
    """从剧本段落中提取台词"""
    if target_episodes is None:
        target_episodes = list(range(1, 11))  # 默认前10集

    all_episodes = find_episode_boundaries(paragraphs)
    selected_episodes = filter_episodes_by_number(all_episodes, target_episodes)

    print(f"找到 {len(all_episodes)} 回正文，筛选出第 {target_episodes} 回")

    all_quotes = []
    stats = {"total_paragraphs": 0, "dialogue_lines": 0, "filtered": 0, "kept": 0}

    for ep_start, ep_end, ep_title in selected_episodes:
        ep_paragraphs = paragraphs[ep_start:ep_end]
        stats["total_paragraphs"] += len(ep_paragraphs)
        ep_quotes = []

        for p in ep_paragraphs:
            result = is_dialogue_line(p)
            if not result:
                continue
            stats["dialogue_lines"] += 1
            character, raw_text = result
            cleaned = clean_quote(raw_text)
            if should_filter(cleaned):
                stats["filtered"] += 1
                continue
            stats["kept"] += 1
            ep_quotes.append({
                "quote": cleaned,
                "character": character,
                "episode": ep_title,
                "category": ""  # 待分类
            })

        all_quotes.extend(ep_quotes)
        print(f"  {ep_title}: 提取 {len(ep_quotes)} 条台词候选")

    print(f"\n总计: {stats['total_paragraphs']} 段, "
          f"对话 {stats['dialogue_lines']} 条, "
          f"过滤 {stats['filtered']} 条, "
          f"保留 {stats['kept']} 条")
    return all_quotes


def main():
    print("=" * 60)
    print("武林外传剧本 — 台词提取")
    print("=" * 60)

    paragraphs = parse_docx_xml(SCRIPT_FILE)
    print(f"总段落数: {len(paragraphs)}")

    quotes = extract_quotes(paragraphs, target_episodes=list(range(1, 11)))

    # 输出去重后的候选
    seen = set()
    unique_quotes = []
    for q in quotes:
        key = q["quote"]
        if key not in seen:
            seen.add(key)
            unique_quotes.append(q)

    print(f"去重后: {len(unique_quotes)} 条")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(unique_quotes, f, ensure_ascii=False, indent=2)

    print(f"已输出到 {OUTPUT_FILE}")

    # 打印前20条样例
    print("\n--- 前20条样例 ---")
    for q in unique_quotes[:20]:
        print(f"【{q['character']}】{q['quote'][:60]}")


if __name__ == "__main__":
    main()
