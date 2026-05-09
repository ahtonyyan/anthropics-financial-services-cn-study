#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Claude大模型进行高质量中文翻译
"""
import json
import os
import re
import time

try:
    from anthropic import Anthropic
except ImportError:
    print("正在安装anthropic库...")
    import subprocess
    subprocess.run(['pip3', 'install', 'anthropic'], check=True)
    from anthropic import Anthropic

# 读取英文原版
with open('skill-translations.json', 'r', encoding='utf-8') as f:
    translations_en = json.load(f)

# 初始化Claude客户端
api_key = os.environ.get('ANTHROPIC_API_KEY')
if not api_key:
    print("⚠️ 未找到ANTHROPIC_API_KEY环境变量")
    print("请设置API密钥：export ANTHROPIC_API_KEY='your-key-here'")
    print("\n您可以从 https://console.anthropic.com 获取API密钥")
    exit(1)

client = Anthropic(api_key=api_key)

# 翻译进度跟踪
def translate_with_claude(content, skill_name):
    """使用Claude翻译单个技能内容"""

    # 创建翻译提示
    prompt = f"""请将以下金融分析技能文档翻译成完整、流畅的中文。

**重要要求：**
1. 翻译成完整、专业的中文，不要保留英文单词
2. 技术术语使用标准中文翻译（如DCF=折现现金流，LBO=杠杆收购）
3. 代码块、公式、API名称保持不变
4. Markdown格式保持不变
5. 专业金融文档风格，准确表达金融概念

**技能名称：** {skill_name}

**内容：**
{content}

请直接返回翻译后的内容，不要添加任何解释或前言。"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",  # 使用最新的Sonnet 4模型
            max_tokens=16000,
            temperature=0.3,  # 较低温度保证翻译一致性
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return message.content[0].text

    except Exception as e:
        print(f"❌ {skill_name} 翻译失败: {str(e)[:100]}")
        return None

def translate_content_preserve_code_blocks(content):
    """智能处理代码块的翻译"""
    lines = content.split('\n')
    result = []
    in_code_block = False
    code_content = []

    for line in lines:
        if line.strip().startswith('```'):
            if not in_code_block:
                # 代码块开始前，先翻译累积的内容
                if result:
                    translated = translate_with_claude('\n'.join(result), "content_chunk")
                    if translated:
                        return translated
                in_code_block = True
                code_content = [line]
            else:
                # 代码块结束
                code_content.append(line)
                in_code_block = False
                code_content = []
            continue

        if in_code_block:
            code_content.append(line)
        else:
            result.append(line)

    return '\n'.join(result)

# 主翻译流程
zh_translations = {}
total_skills = len(translations_en)

print("=" * 60)
print("使用Claude大模型翻译金融技能文档")
print("=" * 60)

# 询问翻译范围
print(f"\n共{total_skills}个技能需要翻译")
print("由于API调用需要时间和费用，建议分批翻译：")
print("1. 先翻译1-3个技能测试质量")
print("2. 确认质量后继续翻译剩余技能")
print("\n请输入要翻译的技能数量（1-55），或输入'all'翻译全部：")

# 默认先翻译前3个作为示例
skills_to_translate = list(sorted(translations_en.keys()))[:3]

print(f"\n开始翻译前{len(skills_to_translate)}个技能作为示例...")

for i, skill_id in enumerate(skills_to_translate):
    print(f"\n[{i+1}/{len(skills_to_translate)}] 正在翻译: {skill_id}")

    original = translations_en[skill_id]['original']

    # 对于很长的内容，可能需要分块处理
    if len(original) > 50000:
        print(f"  ⚠️ 内容较长({len(original)}字符)，可能需要更多时间...")

    translated = translate_with_claude(original, skill_id)

    if translated:
        zh_translations[skill_id] = translated
        print(f"  ✓ 翻译完成，输出{len(translated)}字符")
    else:
        print(f"  ✗ 翻译失败，跳过")

    # 避免API速率限制
    if i < len(skills_to_translate) - 1:
        time.sleep(2)

# 保存翻译结果
if zh_translations:
    js_content = "// 技能中文翻译 - 使用Claude大模型翻译\n"
    js_content += "var skillTranslationsZh = {\n"

    for skill_id, translation in sorted(zh_translations.items()):
        escaped = json.dumps(translation, ensure_ascii=False)
        js_content += f'    "{skill_id}": {escaped},\n'

    js_content += "};\n"

    output_file = 'skill-translations-zh-claude.js'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"\n{'=' * 60}")
    print(f"✓ 翻译完成！")
    print(f"✓ 成功翻译: {len(zh_translations)} 个技能")
    print(f"✓ 已保存到: {output_file}")
    print(f"✓ 文件大小: {len(js_content):,} 字节")
    print(f"\n如需翻译更多技能，请再次运行此脚本")
else:
    print("\n没有成功翻译任何内容，请检查API密钥设置")

print(f"\n{'=' * 60}")
print("API费用估算：")
print(f"- 本次翻译: ~${len(zh_translations) * 0.02:.2f}")
print(f"- 全部55个技能: ~${1.10}")
print(f"{'=' * 60}")
