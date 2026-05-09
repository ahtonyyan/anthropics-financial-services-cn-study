#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金融领域专用翻译 - 完整短语级映射
"""
import json
import re

# 读取英文原版
with open('skill-translations.json', 'r', encoding='utf-8') as f:
    translations_en = json.load(f)

# 金融专用完整翻译映射
FINANCIAL_TRANSLATIONS = {
    # === 完整句子和常用表达 ===

    # 数据获取
    "Fetch data from MCP servers": "从MCP服务器获取数据",
    "user provided data": "用户提供的数据",
    "and the web": "以及网络数据",
    "Data Sources Priority": "数据源优先级",
    "Structured financial data": "结构化金融数据",
    "from providers like": "来自等提供商",
    "Historical financials from their research": "其研究中的历史财务数据",
    "Web Search/Fetch": "网络搜索/获取",
    "Current prices, beta, debt and cash when needed": "需要时的当前价格、贝塔、债务和现金",
    "Validation Checklist": "验证清单",

    # 验证项目
    "Verify net debt vs net cash": "验证净债务与净现金",
    "Confirm diluted shares outstanding": "确认摊薄后流通股数",
    "check for recent buybacks/issuances": "检查最近的回购或发行",
    "Verify historical margins are consistent with business model": "验证历史利润率与业务模型一致",
    "Cross-check revenue growth rates with industry benchmarks": "与行业基准交叉检查收入增长率",
    "Verify tax rate is reasonable": "验证税率合理",
    "typically 21-28%": "通常为21-28%",

    # 核心原则标题
    "CRITICAL PRINCIPLES": "核心原则",
    "Read Before": "在使用之前请阅读",
    "Environment": "环境",
    "Office JS vs Python": "Office JS与Python",
    "If running inside Excel": "如果在Excel内运行",
    "Office Add-in / Office JS": "Office加载项或Office JS",
    "Use Office JS directly": "直接使用Office JS",
    "Write formulas via": "通过以下方式编写公式",
    "never": "绝不",
    "for derived cells": "对于派生单元格",
    "No separate recalc": "无需单独重新计算",
    "Excel computes natively": "Excel原生计算",
    "Use": "使用",
    "to navigate tabs": "来导航选项卡",
    "If generating a standalone": "如果生成独立的",
    "Use Python/openpyxl": "使用Python的openpyxl库",
    "then run recalc.py before delivery": "然后在交付前运行recalc.py",
    "Office JS merged cell pitfall": "Office JS合并单元格陷阱",
    "Do NOT call": "不要调用",
    "then set": "然后设置",
    "on the merged range": "在合并范围上",
    "throws": "会抛出",
    "because the range still reports its pre-merge dimensions": "因为范围仍报告其合并前的维度",
    "Instead write value to top-left cell alone": "而是仅在左上角单元格写入值",
    "then merge + format the full range": "然后合并并格式化整个范围",
    "All principles below apply identically in either environment": "以下所有原则在两种环境中同样适用",

    # 公式优于硬编码
    "Formulas over hardcodes": "公式优于硬编码",
    "non-negotiable": "不可协商",
    "Every forecast cell": "每个预测单元格",
    "roll-forward": "滚动结转",
    "linkage": "链接",
    "and subtotal": "和小计",
    "MUST be an Excel formula": "必须是Excel公式",
    "never a pre-computed value": "绝不要预计算的值",
    "When using Python/openpyxl": "当使用Python的openpyxl时",
    "write formula strings": "编写公式字符串",
    "NOT computed results": "而非计算结果",
    "The ONLY cells that should contain hardcode": "唯一应包含硬编码的单元格",
    "raw input data": "原始输入数据",
    "each with a cell comment citing its source": "每个都有单元格注释引用其来源",
    "the model must update automatically when inputs change": "当输入更改时模型必须自动更新",
    "A hardcoded margin is a silent error waiting to happen": "硬编码的利润率是等待发生的静默错误",

    # 验证流程
    "Verify incrementally with the user": "与用户逐步验证",
    "After setting up structure": "设置结构后",
    "show the header layout to the user": "向用户显示标题布局",
    "before populating data": "在填充数据之前",
    "After entering raw inputs": "输入原始输入后",
    "show the input block to the user": "向用户显示输入块",
    "and confirm source/period": "并确认来源和期间",
    "before building formulas": "在构建公式之前",
    "After building operating metrics formulas": "构建运营指标公式后",
    "show calculated margins to the user": "向用户显示计算的利润率",
    "and sanity-check them": "并进行合理性检查",
    "before moving to valuation": "在转向估值之前",
    "After building valuation multiples": "构建估值倍数后",
    "show multiples to the user": "向用户显示倍数",
    "and confirm they look reasonable": "并确认它们看起来合理",
    "before adding statistics": "在添加统计之前",
    "Don't build the entire worksheet end-to-end then present": "不要端到端构建整个工作表然后展示",
    "catch mistakes early by confirming at each section": "通过在每个部分确认来尽早捕获错误",

    # === 金融核心术语 ===

    # 可比公司分析
    "Comparable Company Analysis": "可比公司分析",
    "Comps": "可比公司分析",
    "trading multiples": "交易倍数",
    "peer companies": "同行公司",
    "comparable set": "可比公司组",
    "valuation multiples": "估值倍数",
    "operating metrics": "运营指标",
    "LTM": "过去十二个月",
    "Last Twelve Months": "过去十二个月",

    # DCF估值
    "Discounted Cash Flow": "折现现金流",
    "DCF": "折现现金流",
    "terminal value": "终值",
    "WACC": "加权平均资本成本",
    "Weighted Average Cost of Capital": "加权平均资本成本",
    "free cash flow": "自由现金流",
    "perpetuity growth rate": "永续增长率",
    "discount rate": "折现率",
    "present value": "现值",

    # LBO杠杆收购
    "Leveraged Buyout": "杠杆收购",
    "LBO": "杠杆收购",
    "private equity firm": "私募股权公司",
    "entry valuation": "进入估值",
    "exit valuation": "退出估值",
    "IRR": "内部收益率",
    "Internal Rate of Return": "内部收益率",
    "cash-on-cash return": "现金回报率",
    "debt schedule": "债务计划表",
    "senior debt": "优先债务",
    "subordinated debt": "次级债务",
    "mezzanine financing": "夹层融资",

    # 三表模型
    "Three-Statement Model": "三表模型",
    "Income Statement": "利润表",
    "Balance Sheet": "资产负债表",
    "Cash Flow Statement": "现金流量表",
    "revenue growth": "收入增长",
    "cost of goods sold": "销售成本",
    "gross profit": "毛利润",
    "operating expenses": "运营费用",
    "EBITDA": "息税折旧摊销前利润",
    "net income": "净利润",
    "working capital": "营运资本",
    "capital expenditures": "资本支出",
    "depreciation and amortization": "折旧和摊销",

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

    # 投行文档
    "Confidential Information Memorandum": "保密信息备忘录",
    "CIM": "保密信息备忘录",
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
    "DD": "尽职调查",
    "Unit Economics": "单元经济",
    "Returns Analysis": "回报分析",
    "Investment Committee": "投资委员会",
    "IC": "投资委员会",
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
    "General Ledger": "总账",
    "NAV Tieout": "NAV核对",
    "Net Asset Value": "净资产价值",
    "Variance Commentary": "差异评述",
    "Roll Forward": "滚动结转",

    # KYC
    "KYC Document Parsing": "KYC文档解析",
    "Know Your Customer": "了解你的客户",
    "KYC Rules Engine": "KYC规则引擎",

    # === Excel相关 ===
    "Excel spreadsheet": "Excel电子表格",
    "worksheet": "工作表",
    "workbook": "工作簿",
    "cell": "单元格",
    "range": "范围",
    "formula": "公式",
    "function": "函数",
    "pivot table": "数据透视表",
    "chart": "图表",
    "conditional formatting": "条件格式",
    "data validation": "数据验证",
    "audit trail": "审计追踪",

    # === 动词 ===
    "build": "构建",
    "create": "创建",
    "generate": "生成",
    "calculate": "计算",
    "populate": "填充",
    "complete": "完成",
    "verify": "验证",
    "confirm": "确认",
    "validate": "验证",
    "check": "检查",
    "ensure": "确保",
    "analyze": "分析",
    "assess": "评估",
    "evaluate": "评价",
    "review": "审查",
    "estimate": "估算",
    "forecast": "预测",
    "project": "预测",

    # === 名词 ===
    "template": "模板",
    "model": "模型",
    "analysis": "分析",
    "report": "报告",
    "data": "数据",
    "financial": "金融",
    "investment": "投资",
    "banking": "银行",
    "equity": "股权",
    "research": "研究",
    "portfolio": "投资组合",
    "asset": "资产",
    "liability": "负债",
    "debt": "债务",
    "cash": "现金",
    "revenue": "收入",
    "growth": "增长",
    "margin": "利润率",
    "profit": "利润",
    "loss": "亏损",
    "risk": "风险",
    "return": "回报",
    "company": "公司",
    "market": "市场",
    "industry": "行业",
    "sector": "板块",
    "metric": "指标",
    "ratio": "比率",
    "multiple": "倍数",
    "value": "价值",
    "valuation": "估值",
    "output": "输出",
    "input": "输入",

    # === 连接词和介词 ===
    "and": "和",
    "or": "或",
    "with": "与",
    "for": "用于",
    "from": "从",
    "to": "至",
    "in": "在",
    "on": "在",
    "at": "在",
    "by": "通过",
    "of": "的",
    "the": "",  # 删除定冠词
    "a": "",   # 删除不定冠词
    "an": "",  # 删除不定冠词
    "is": "是",
    "are": "是",
    "when": "当",
    "then": "然后",
    "before": "之前",
    "after": "之后",
    "while": "当",
    "during": "期间",
    "through": "通过",
    "using": "使用",
}

def translate_text_smart(text, depth=0):
    """智能翻译文本"""
    if not text or depth > 5:
        return text

    result = text
    changes_made = True
    iteration = 0

    # 多次迭代翻译，直到没有更多变化
    while changes_made and iteration < 10:
        changes_made = False
        iteration += 1

        # 按长度降序处理（先匹配长短语）
        for en, zh in sorted(FINANCIAL_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
            if not zh:  # 空翻译（如"the"）直接删除
                pattern = r'\b' + re.escape(en) + r'\b'
                new_result = re.sub(pattern, '', result, flags=re.IGNORECASE)
            else:
                # 使用单词边界匹配
                pattern = r'\b' + re.escape(en) + r'\b'
                new_result = re.sub(pattern, zh, result, flags=re.IGNORECASE)

            if new_result != result:
                changes_made = True
                result = new_result

    # 清理多余空格
    result = re.sub(r'\s+', ' ', result)
    result = re.sub(r'\s+([，。！？；：])', r'\1', result)  # 中文标点前的空格

    return result.strip()

def translate_content_preserve_code(content):
    """翻译内容但保留代码块不变"""
    lines = content.split('\n')
    translated_lines = []

    in_code_block = False

    for line in lines:
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
            # 翻译普通行
            translated = translate_text_smart(line)
            # 保持原始行结构（缩进等）
            indent = len(line) - len(line.lstrip())
            if indent > 0 and translated:
                translated = ' ' * indent + translated
            translated_lines.append(translated if translated else line)

    return '\n'.join(translated_lines)

def translate_line_with_inline_code(line):
    """翻译包含行内代码的行"""
    parts = line.split('`')
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # 普通文本 - 翻译
            translated = translate_text_smart(part)
            result.append(translated if translated else part)
        else:
            # 代码 - 保持不变
            result.append(part)
    return '`'.join(result)

# 主翻译流程
zh_translations = {}

print("开始金融领域专用翻译...")
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
js_content = "// 技能中文翻译数据 - 金融领域专用\n"
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
