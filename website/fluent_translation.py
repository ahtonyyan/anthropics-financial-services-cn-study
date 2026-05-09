#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用完整句子模式进行翻译 - 产生更流畅的中文
"""
import json
import re

# 读取英文原版
with open('skill-translations.json', 'r', encoding='utf-8') as f:
    translations_en = json.load(f)

# 完整句子模式映射 - 从长到短排序
SENTENCE_PATTERNS = [
    # YAML frontmatter 模式
    (r'name: (.+)-analysis', r'name: \1分析'),
    (r'name: 3-statement-model', r'name: 三表模型'),
    (r'name: 3-statement-模型', r'name: 三表模型'),
    (r'description: (.+?)$', r'description: \1'),

    # 完整常用句子
    (r'Use when asked to (.+?)$', r'用于被要求\1时使用'),
    (r'Complete and populate (.+?) with (.+?)$', r'完成并填充\1，包含\2'),
    (r'Complete, populate and fill out (.+?)$', r'完成、填充并填写\1'),
    (r'with proper linkages between (.+?) and (.+?)$', r'在\1和\2之间建立适当的链接'),
    (r'Fetch data from (.+?) MCP servers, user provided (.+?), and the web',
     r'从\1MCP服务器、用户提供的\2以及网络获取数据'),
    (r'Fetch data from MCP servers', r'从MCP服务器获取数据'),
    (r'Data Sources Priority:', r'数据源优先级：'),
    (r'Structured (.+?) from providers like (.+?)\)', r'来自\2等提供商的结构化\1'),
    (r'User-Provided (.+?) - (.+?)$', r'用户提供\1 - \2'),
    (r'Web Search/Fetch - (.+?)$', r'网络搜索/获取 - \1'),
    (r'Validation Checklist:', r'验证清单：'),
    (r'Verify (.+?) vs (.+?)$', r'验证\1与\2'),
    (r'Confirm (.+?) \\(check for (.+?)\\)', r'确认\1（检查\2）'),
    (r'Verify (.+?) are consistent with (.+?)$', r'验证\1与\2一致'),
    (r'Cross-check (.+?) with (.+?)$', r'用\2交叉检查\1'),
    (r'Verify (.+?) is reasonable \\((.+?)\\)', r'验证\1合理（\2）'),

    # 核心原则
    (r'⚠️ CRITICAL PRINCIPLES — Read Before (.+?)$', r'⚠️ 核心原则 — 在使用\1之前请阅读'),
    (r'Environment — (.+?) vs (.+?)$', r'环境 — \1与\2'),
    (r'\*\*If running inside Excel \\((.+?)\\):\\*\*', r'**如果在Excel内运行（\1）：**'),
    (r'Use (.+?) directly', r'直接使用\1'),
    (r'Write formulas via `(.+?)`', r'通过`\1`编写公式'),
    (r'never `(.+?)` for (.+?)$', r'派生\2绝不要使用`\1`'),
    (r'No separate recalc;', r'无需单独重新计算；'),
    (r'computes natively', r'原生计算'),
    (r'Use `(.+?)` to (.+?)$', r'使用`\1`来\2'),
    (r'\*\*If generating a (.+?):\\*\*', r'**如果生成\1：**'),
    (r'Write `(.+?)`, then run (.+?) before delivery', r'编写`\1`，然后在交付前运行\2'),
    (r'pitfall:', r'陷阱：'),
    (r'Do NOT call `(.+?)` then set `(.+?)`', r'不要调用`\1`然后设置`\2`'),
    (r'throws `(.+?)` because', r'抛出`\1`，因为'),
    (r'Instead write (.+?) alone, then (.+?) the full range',
     r'而是仅写入\1，然后\2整个范围'),
    (r'All principles below apply identically in either environment',
     r'以下所有原则在两种环境中同样适用'),

    # 公式优于硬编码
    (r'Formulas over hardcodes \\(non-negotiable\\):', r'公式优于硬编码（不可协商）：'),
    (r'Every (.+?), (.+?), and (.+?) MUST be an (.+?)',
     r'每个\1、\2和\3都必须是\4'),
    (r'never a pre-computed value', r'绝不要预计算的值'),
    (r'When using (.+?): write `(.+?)`', r'使用\1时：编写`\2`'),
    (r'NOT computed results \\(`(.+?)`\\)', r'而非计算结果（`\1`）'),
    (r'The ONLY cells that should contain (.+?) are:', r'唯一应包含\1的单元格是：'),
    (r'If you find yourself (.+?) and (.+?) — STOP', r'如果你发现自己正在\1并\2 — 停止'),
    (r'Why: the (.+?) must (.+?) when (.+?)', r'原因：当\3时，\1必须\2'),
    (r'A hardcoded (.+?) is a silent error waiting to happen',
     r'硬编码的\1是等待发生的静默错误'),

    # 验证流程
    (r'Verify incrementally with the user:', r'与用户逐步验证：'),
    (r'After setting up structure → show (.+?) to the user', r'设置结构后 → 向用户显示\1'),
    (r'before (.+?)$', r'在\1之前'),
    (r'After entering (.+?) → show (.+?) and confirm (.+?)',
     r'输入\1后 → 显示\2并确认\3'),
    (r'before building (.+?)$', r'在构建\1之前'),
    (r'After building (.+?) → show (.+?) and (.+?) them',
     r'构建\1后 → 显示\2并\3它们'),
    (r'Do not build the entire (.+?) then present', r'不要端到端构建整个\1然后展示'),
    (r'catch mistakes early by (.+?)', r'通过\1尽早捕获错误'),

    # 金融术语完整短语
    (r'Comparable Company Analysis', r'可比公司分析'),
    (r'Discounted Cash Flow \\(DCF\\)', r'折现现金流（DCF）'),
    (r'Leveraged Buyout \\(LBO\\)', r'杠杆收购（LBO）'),
    (r'Three-Statement Financial Model', r'三表金融模型'),
    (r'income statement, balance sheet, and cash flow statement',
     r'利润表、资产负债表和现金流量表'),
    (r'Income Statement \\(IS\\)', r'利润表（IS）'),
    (r'Balance Sheet \\(BS\\)', r'资产负债表（BS）'),
    (r'Cash Flow Statement \\(CF\\)', r'现金流量表（CF）'),
    (r'Enterprise Value \\(EV\\)', r'企业价值（EV）'),
    (r'Market Capitalization \\(Market Cap\\)', r'市值（Market Cap）'),
    (r'Earnings Before Interest, Taxes, Depreciation and Amortization',
     r'息税折旧摊销前利润'),
    (r'Free Cash Flow \\(FCF\\)', r'自由现金流（FCF）'),
    (r'Weighted Average Cost of Capital \\(WACC\\)', r'加权平均资本成本（WACC）'),
    (r'Terminal Value', r'终值'),
    (r'Gross Profit Margin', r'毛利率'),
    (r'Operating Margin', r'营业利润率'),
    (r'Net Income Margin', r'净利润率'),
    (r'Sensitivity Analysis', r'敏感性分析'),
    (r'Scenario Analysis', r'情景分析'),
    (r'Bear \\(Downside\\) Case', r'悲观（下行）情景'),
    (r'Base \\(Reference\\) Case', r'基准（参考）情景'),
    (r'Bull \\(Upside\\) Case', r'乐观（上行）情景'),

    # 常用表达
    (r'Build a (.+?) model in (.+?)$', r'在\2中构建\1模型'),
    (r'Create a (.+?) analysis', r'创建\1分析'),
    (r'Generate (.+?) output', r'生成\1输出'),
    (r'Perform (.+?) analysis', r'执行\1分析'),
    (r'Calculate (.+?) metrics', r'计算\1指标'),
    (r'defining the (.+?)', r'定义\1'),
    (r'selecting the (.+?)', r'选择\1'),
    (r'setting up the (.+?)', r'设置\1'),
    (r'populating the (.+?)', r'填充\1'),
    (r'building (.+?) formulas', r'构建\1公式'),
    (r'adding (.+?) statistics', r'添加\1统计'),

    # 介词短语
    (r'for (.+?) analysis', r'用于\1分析'),
    (r'with (.+?) data', r'使用\1数据'),
    (r'in (.+?) format', r'以\1格式'),
    (r'from (.+?) source', r'从\1来源'),
    (r'to (.+?) target', r'至\1目标'),
    (r'by (.+?) method', r'通过\1方法'),
    (r'via (.+?) approach', r'通过\1方法'),
    (r'using (.+?) template', r'使用\1模板'),
]

# 词汇映射（在句子模式之后应用）
WORD_MAP = {
    # 金融核心词汇
    'comparable': '可比',
    'discount': '折现',
    'leveraged': '杠杆',
    'acquisition': '收购',
    'buyout': '收购',
    'statement': '报表',
    'financial': '金融',
    'enterprise': '企业',
    'valuation': '估值',
    'multiple': '倍数',
    'metric': '指标',
    'benchmark': '基准',
    'projection': '预测',
    'forecast': '预测',
    'assumption': '假设',
    'scenario': '情景',
    'sensitivity': '敏感性',
    'margin': '利润率',
    'revenue': '收入',
    'growth': '增长',
    'profit': '利润',
    'earnings': '盈利',
    'cash': '现金',
    'flow': '流',
    'debt': '债务',
    'equity': '股权',
    'capital': '资本',
    'asset': '资产',
    'liability': '负债',
    'shareholder': '股东',
    'operating': '运营',
    'business': '业务',
    'company': '公司',
    'corporate': '企业',
    'investment': '投资',
    'portfolio': '投资组合',
    'return': '回报',
    'rate': '率',
    'ratio': '比率',
    'yield': '收益率',

    # 动词
    'build': '构建',
    'create': '创建',
    'generate': '生成',
    'calculate': '计算',
    'populate': '填充',
    'complete': '完成',
    'verify': '验证',
    'confirm': '确认',
    'validate': '验证',
    'check': '检查',
    'ensure': '确保',
    'analyze': '分析',
    'assess': '评估',
    'evaluate': '评价',
    'review': '审查',
    'estimate': '估算',
    'project': '预测',
    'forecast': '预测',

    # 常用词
    'template': '模板',
    'model': '模型',
    'worksheet': '工作表',
    'workbook': '工作簿',
    'spreadsheet': '电子表格',
    'formula': '公式',
    'cell': '单元格',
    'range': '范围',
    'data': '数据',
    'output': '输出',
    'input': '输入',
    'value': '值',
    'result': '结果',
    'method': '方法',
    'approach': '方法',
    'framework': '框架',
    'structure': '结构',
    'format': '格式',
    'section': '部分',
    'block': '块',
    'column': '列',
    'row': '行',
    'header': '标题',
    'footer': '页脚',
    'report': '报告',
    'document': '文档',
    'file': '文件',
    'sheet': '表',
    'tab': '选项卡',
}

def translate_text_fluent(text):
    """使用完整句子模式和词汇映射产生流畅中文"""
    if not text:
        return text

    result = text

    # 首先应用完整句子模式（按长度降序）
    for pattern, replacement in sorted(SENTENCE_PATTERNS, key=lambda x: len(x[0]), reverse=True):
        try:
            result = re.sub(pattern, replacement, result, flags=re.MULTILINE | re.IGNORECASE)
        except:
            pass

    # 然后应用词汇映射
    for en, zh in sorted(WORD_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        try:
            # 只替换单词边界，避免影响已翻译的内容
            result = re.sub(r'\b' + re.escape(en) + r's?\b', zh, result, flags=re.IGNORECASE)
        except:
            pass

    return result

def translate_content_preserve_code(content):
    """翻译内容但保留代码块不变"""
    lines = content.split('\n')
    translated_lines = []

    in_code_block = False

    for line in lines:
        # 检测代码块开始
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
            # 翻译普通行
            translated_lines.append(translate_text_fluent(line))

    return '\n'.join(translated_lines)

def translate_line_with_inline_code(line):
    """翻译包含行内代码的行"""
    parts = line.split('`')
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            result.append(translate_text_fluent(part))
        else:
            result.append(part)
    return '`'.join(result)

# 主翻译流程
zh_translations = {}

print("开始高质量句子级翻译...")
print("=" * 60)

translated_count = 0
total_chars = 0

for skill_id, data in sorted(translations_en.items()):
    original = data['original']
    translated = translate_content_preserve_code(original)
    zh_translations[skill_id] = translated
    translated_count += 1
    total_chars += len(translated)

    if translated_count % 5 == 0:
        print(f"✓ 已翻译 {translated_count}/55 个技能")

print(f"\n✓ 翻译完成！")
print(f"✓ 总技能数: {translated_count}")
print(f"✓ 总字符数: {total_chars:,}")

# 保存为JavaScript文件
js_content = "// 技能完整中文翻译数据 - 高质量句子级翻译\n"
js_content += "var skillTranslationsZh = {\n"

for skill_id, translation in sorted(zh_translations.items()):
    escaped = json.dumps(translation, ensure_ascii=False)
    js_content += f'    "{skill_id}": {escaped},\n'

js_content += "};\n"

output_file = 'skill-translations-zh.js'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"\n✓ 已保存到: {output_file}")
print(f"✓ 文件大小: {len(js_content):,} 字节")
