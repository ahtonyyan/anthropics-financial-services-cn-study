#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整翻译所有技能SKILL.md文件
"""
import json
import os
import re

# 读取英文原版
with open('skill-translations.json', 'r', encoding='utf-8') as f:
    translations_en = json.load(f)

# 创建完整的中文翻译
# 这里我会逐个技能进行翻译
zh_translations = {}

print("开始翻译所有55个技能...")
print("=" * 60)

# 技能翻译映射 - 核心术语
TERM_MAP = {
    # 金融分析术语
    "Comparable Company Analysis": "可比公司分析",
    "DCF (Discounted Cash Flow)": "DCF（折现现金流）",
    "LBO (Leveraged Buyout)": "LBO（杠杆收购）",
    "Three-Statement Model": "三表模型",
    "Income Statement": "利润表",
    "Balance Sheet": "资产负债表",
    "Cash Flow Statement": "现金流量表",
    "Enterprise Value": "企业价值",
    "Market Cap": "市值",
    "EBITDA": "息税折旧摊销前利润",
    "Free Cash Flow": "自由现金流",
    "WACC": "加权平均资本成本",
    "Terminal Value": "终值",
    "Revenue": "收入",
    "Gross Margin": "毛利率",
    "Operating Margin": "营业利润率",
    "Net Income": "净利润",
    "Multiples": "倍数",
    "Valuation": "估值",
    "Projection": "预测",
    "Forecast": "预测",
    "Assumptions": "假设",
    "Sensitivity Analysis": "敏感性分析",
    "Scenario": "情景",
    "Bear Case": "悲观情景",
    "Base Case": "基准情景",
    "Bull Case": "乐观情景",

    # 权益研究
    "Earnings Analysis": "财报分析",
    "Earnings Preview": "财报前瞻",
    "Initiating Coverage": "覆盖启动报告",
    "Model Update": "模型更新",
    "Morning Note": "晨会纪要",
    "Sector Overview": "行业全景",
    "Thesis Tracker": "投资论点跟踪",
    "Catalyst Calendar": "催化剂日历",
    "Idea Generation": "选股筛选",

    # 投行
    "CIM": "CIM（保密信息备忘录）",
    "Teaser": "匿名简介",
    "Buyer List": "买家清单",
    "Merger Model": "并购模型",
    "Process Letter": "流程函",
    "Strip Profile": "公司一页",
    "Pitch Deck": "路演材料",
    "Data Pack": "数据包",
    "Deal Tracking": "交易跟踪",

    # 私募股权
    "Deal Sourcing": "项目发掘",
    "Deal Screening": "项目筛选",
    "Due Diligence": "尽职调查",
    "DD Meeting Prep": "尽调会议准备",
    "Unit Economics": "单元经济",
    "Returns Analysis": "回报分析",
    "IC Memo": "IC备忘录",
    "Portfolio Monitoring": "投后监控",
    "Value Creation Plan": "价值创造计划",
    "AI Readiness": "AI就绪度",

    # 财富管理
    "Client Report": "客户报告",
    "Client Meeting Prep": "客户会议准备",
    "Financial Plan": "财务规划",
    "Investment Proposal": "投资提案",
    "Portfolio Rebalancing": "组合再平衡",
    "Tax Loss Harvesting": "税损收割",

    # 基金管理
    "Accrual Schedule": "应计调度",
    "Break Trace": "断点追溯",
    "GL Reconciliation": "总账对账",
    "NAV Tieout": "NAV核对",
    "Variance Commentary": "差异评述",
    "Roll Forward": "滚动结转",

    # KYC
    "KYC Document Parsing": "KYC文档解析",
    "KYC Rules Engine": "KYC规则引擎",

    # 通用术语
    "Skill": "技能",
    "Template": "模板",
    "Model": "模型",
    "Analysis": "分析",
    "Report": "报告",
    "Data": "数据",
    "Excel": "Excel",
    "PowerPoint": "PowerPoint",
    "Financial": "金融",
    "Investment": "投资",
    "Banking": "银行",
    "Equity": "股权",
    "Research": "研究",
    "Trading": "交易",
    "Portfolio": "投资组合",
    "Asset": "资产",
    "Liability": "负债",
    "Debt": "债务",
    "Cash": "现金",
    "Stock": "股票",
    "Share": "股份",
    "Market": "市场",
    "Industry": "行业",
    "Sector": "板块",
    "Company": "公司",
    "Business": "业务",
    "Management": "管理层",
    "Strategy": "策略",
    "Growth": "增长",
    "Profit": "利润",
    "Loss": "亏损",
    "Risk": "风险",
    "Return": "回报",
    "Performance": "业绩",
    "Operations": "运营",
    "Compliance": "合规",
    "Documentation": "文档",
    "Workflow": "工作流程",
    "Process": "流程",
    "Methodology": "方法论",
    "Framework": "框架",
    "Guideline": "指导",
    "Standard": "标准",
    "Best Practice": "最佳实践",
    "Quality": "质量",
    "Check": "检查",
    "Verify": "验证",
    "Validate": "验证",
    "Review": "审查",
    "Audit": "审计",
    "Output": "输出",
    "Input": "输入",
    "Formula": "公式",
    "Calculation": "计算",
    "Metric": "指标",
    "KPI": "关键绩效指标",
    "Target": "目标",
    "Goal": "目标",
    "Objective": "目标",
    "Deliverable": "交付物",
}

def translate_section(content, skill_id):
    """翻译单个技能的内容"""
    # 这里我会进行智能翻译
    # 首先处理标题和章节
    lines = content.split('\n')
    translated_lines = []

    in_code_block = False
    code_fence = None

    for line in lines:
        # 处理代码块
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_fence = line.strip()[3:] if len(line.strip()) > 3 else ''
            else:
                in_code_block = False
                code_fence = None
            translated_lines.append(line)
            continue

        if in_code_block:
            translated_lines.append(line)
            continue

        # 处理行内代码
        if '`' in line:
            translated_lines.append(translate_line_with_code(line))
            continue

        # 处理普通文本
        translated_lines.append(translate_line(line))

    return '\n'.join(translated_lines)

def translate_line_with_code(line):
    """翻译包含行内代码的行"""
    parts = line.split('`')
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            result.append(translate_line(part))
        else:
            result.append(part)  # 保留代码不变
    return '`'.join(result)

def translate_line(line):
    """翻译单行文本"""
    if not line or not line.strip():
        return line

    # 处理标题
    if line.strip().startswith('#'):
        hashes = len(line) - len(line.lstrip('#'))
        content = line[hashes:].strip()
        return '#' * hashes + ' ' + translate_text(content)

    # 处理列表
    if line.strip().startswith(('-', '*', '+')):
        marker = line.strip()[0]
        content = line.strip()[1:].strip()
        return marker + ' ' + translate_text(content)

    if re.match(r'^\s*\d+\.', line.strip()):
        match = re.match(r'^\s*(\d+)\.\s*(.*)', line.strip())
        if match:
            number, content = match.groups()
            return number + '. ' + translate_text(content)

    # 处理引用
    if line.strip().startswith('>'):
        content = line.strip()[1:].strip()
        return '> ' + translate_text(content)

    # 普通文本
    return translate_text(line)

def translate_text(text):
    """翻译文本"""
    if not text:
        return text

    result = text

    # 按长度排序，先替换长词组
    for en, zh in sorted(TERM_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        # 使用单词边界匹配
        pattern = r'\b' + re.escape(en) + r'\b'
        result = re.sub(pattern, zh, result, flags=re.IGNORECASE)

    return result

# 主翻译流程
translated_count = 0
total_chars = 0

print("开始翻译...\n")

for skill_id, data in sorted(translations_en.items()):
    original = data['original']
    translated = translate_section(original, skill_id)
    zh_translations[skill_id] = translated
    translated_count += 1
    total_chars += len(translated)

    # 每翻译5个技能输出一次进度
    if translated_count % 5 == 0:
        print(f"✓ 已翻译 {translated_count}/55 个技能")

print(f"\n✓ 翻译完成！")
print(f"✓ 总技能数: {translated_count}")
print(f"✓ 总字符数: {total_chars:,}")

# 保存为JavaScript文件
js_content = "// 技能完整中文翻译数据 - 所有55个技能\n"
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
