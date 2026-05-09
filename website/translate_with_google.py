#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Google Translate API进行高质量中文翻译
"""
import json
import re
import time
from googletrans import Translator

# 读取英文原版
with open('skill-translations.json', 'r', encoding='utf-8') as f:
    translations_en = json.load(f)

# 初始化翻译器
translator = Translator()

def translate_text_google(text, max_retries=3):
    """使用Google翻译文本，带重试机制"""
    if not text or not text.strip():
        return text

    # 跳过纯代码内容
    if re.match(r'^[`\-]{3,}$', text.strip()):
        return text

    # 跳过URL和特殊格式
    if text.strip().startswith('http') or re.match(r'^[A-Za-z0-9_\-\.]+$', text.strip()):
        return text

    for attempt in range(max_retries):
        try:
            result = translator.translate(text, src='en', dest='zh-CN')
            return result.text
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)  # 等待1秒后重试
            else:
                print(f"翻译失败: {str(e)[:50]}")
                return text  # 失败时返回原文

def translate_content_preserve_code(content):
    """翻译内容但保留代码块和公式不变"""
    lines = content.split('\n')
    translated_lines = []

    in_code_block = False

    for i, line in enumerate(lines):
        # 检测代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue

        # 代码块内不翻译
        if in_code_block:
            translated_lines.append(line)
            continue

        # 处理行内代码
        if '`' in line:
            translated_lines.append(translate_line_with_inline_code(line))
        else:
            # 翻译普通行（跳过太长的行）
            if len(line) > 500:
                translated_lines.append(line)  # 保持原文
            else:
                translated_lines.append(translate_text_google(line))

        # 每翻译10行休息一下，避免API限制
        if i % 10 == 0:
            time.sleep(0.1)

    return '\n'.join(translated_lines)

def translate_line_with_inline_code(line):
    """翻译包含行内代码的行"""
    parts = line.split('`')
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # 普通文本 - 翻译
            if part.strip():
                result.append(translate_text_google(part))
            else:
                result.append(part)
        else:
            # 代码 - 保持不变
            result.append(part)
    return '`'.join(result)

# 主翻译流程
zh_translations = {}

print("开始使用Google Translate API翻译...")
print("=" * 60)

translated_count = 0
total_chars = 0
start_time = time.time()

# 先翻译一个测试技能
test_skill = "comps"
print(f"\n测试翻译: {test_skill}")
original = translations_en[test_skill]['original']
translated = translate_content_preserve_code(original)
zh_translations[test_skill] = translated
print(f"✓ {test_skill} 翻译完成")

# 询问是否继续
print(f"\n测试翻译完成！")
print(f"预计需要时间: {(55 * 20 / 60):.1f} 分钟")
print(f"是否继续翻译剩余54个技能？")

# 由于API限制，这里只翻译前几个技能作为示例
skills_to_translate = list(sorted(translations_en.keys()))[:10]  # 先翻译前10个

print(f"\n开始翻译前{len(skills_to_translate)}个技能...")

for skill_id in skills_to_translate:
    if skill_id in zh_translations:
        continue

    original = translations_en[skill_id]['original']
    translated = translate_content_preserve_code(original)
    zh_translations[skill_id] = translated
    translated_count += 1
    total_chars += len(translated)

    elapsed = time.time() - start_time
    print(f"✓ 已翻译 {translated_count}/{len(skills_to_translate)} 个技能 (用时: {elapsed:.1f}秒)")

    # 每个技能后休息，避免API限制
    time.sleep(2)

print(f"\n✓ 翻译完成！")
print(f"✓ 总技能数: {len(zh_translations)}")
print(f"✓ 总字符数: {total_chars:,}")
print(f"✓ 总用时: {time.time() - start_time:.1f}秒")

# 保存为JavaScript文件
js_content = "// 技能中文翻译数据 - 使用Google Translate API\n"
js_content += "var skillTranslationsZh = {\n"

for skill_id, translation in sorted(zh_translations.items()):
    escaped = json.dumps(translation, ensure_ascii=False)
    js_content += f'    "{skill_id}": {escaped},\n'

js_content += "};\n"

output_file = 'skill-translations-zh-sample.js'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"\n✓ 已保存到: {output_file}")
print(f"✓ 文件大小: {len(js_content):,} 字节")
print(f"\n注意: 由于API限制，仅翻译了前{len(zh_translations)}个技能作为示例")
