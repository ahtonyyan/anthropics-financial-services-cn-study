#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高质量短语级翻译 - 产生流畅的中文而非混合语言
"""
import json
import re

# 读取英文原版
with open('skill-translations.json', 'r', encoding='utf-8') as f:
    translations_en = json.load(f)

# 翻译映射：(英文, 中文, 是否使用正则)
TRANSLATIONS = [
    # 完整句子和常用短语 - 使用正则模式
    (r"Fetch data from (\w+(?:\s+\w+)*) MCP servers", r"从\1MCP服务器获取数据", True),
    (r"Fetch data from MCP servers", "从MCP服务器获取数据", False),
    (r"user provided data", "用户提供的数据", False),
    (r"and the web", "以及网络", False),
    (r"Data Sources Priority", "数据源优先级", False),
    (r"Structured financial data", "结构化金融数据", False),
    (r"Historical financials from their research", "其研究中的历史财务数据", False),
    (r"Current prices, beta, debt and cash when needed", "需要时的当前价格、贝塔、债务和现金", False),
    (r"Validation Checklist", "验证清单", False),
    (r"Verify net debt vs net cash", "验证净债务与净现金", False),
    (r"Confirm diluted shares outstanding", "确认摊薄后流通股数", False),
    (r"check for recent buybacks/issuances", "检查最近的回购/发行", False),
    (r"Verify historical margins are consistent with business model", "验证历史利润率与业务模型一致", False),
    (r"Cross-check revenue growth rates with industry benchmarks", "与行业基准交叉检查收入增长率", False),
    (r"Verify tax rate is reasonable", "验证税率合理", False),

    # 核心原则相关
    (r"CRITICAL PRINCIPLES", "核心原则", False),
    (r"Read Before (\S+)", r"在使用\1之前请阅读", True),
    (r"Environment — Office JS vs Python", "环境 - Office JS与Python", False),
    (r"If running inside Excel", "如果在Excel内运行", False),
    (r"Office Add-in / Office JS", "Office加载项/Office JS", False),
    (r"Use Office JS directly", "直接使用Office JS", False),
    (r"never (.+?) for derived cells", r"派生单元格绝不要\1", True),
    (r"No separate recalc", "无需单独重新计算", False),
    (r"Excel computes natively", "Excel原生计算", False),
    (r"If generating a standalone", "如果生成独立的", False),
    (r"Use Python/openpyxl", "使用Python/openpyxl", False),
    (r"then run recalc.py before delivery", "然后在交付前运行recalc.py", False),
    (r"Office JS merged cell pitfall", "Office JS合并单元格陷阱", False),
    (r"Do NOT call", "不要调用", False),
    (r"Instead write value to top-left cell alone", "而是仅在左上角单元格写入值", False),
    (r"then merge \+ format the full range", "然后合并+格式化整个范围", False),
    (r"All principles below apply identically in either environment", "以下所有原则在两种环境中同样适用", False),

    # 公式相关
    (r"Formulas over hardcodes", "公式优于硬编码", False),
    (r"non-negotiable", "不可协商", False),
    (r"Every forecast cell, roll-forward, linkage, and subtotal MUST be an Excel formula", "每个预测单元格、滚动结转、链接和小计都必须是Excel公式", False),
    (r"Every forecast cell", "每个预测单元格", False),
    (r"When using Python/openpyxl", "当使用Python/openpyxl时", False),
    (r"write formula strings", "编写公式字符串", False),
    (r"NOT computed results", "而非计算结果", False),
    (r"The ONLY cells that should contain hardcode", "唯一应包含硬编码的单元格", False),
    (r"raw input data", "原始输入数据", False),
    (r"each with a cell comment citing its source", "每个都有单元格注释引用其来源", False),
    (r"the model must update automatically when inputs change", "当输入更改时模型必须自动更新", False),
    (r"A hardcoded margin is a silent error waiting to happen", "硬编码的利润率是等待发生的静默错误", False),

    # 验证流程
    (r"Verify incrementally with the user", "与用户逐步验证", False),
    (r"After setting up structure", "设置结构后", False),
    (r"show the header layout to the user", "向用户显示标题布局", False),
    (r"before populating data", "在填充数据之前", False),
    (r"After entering raw inputs", "输入原始输入后", False),
    (r"show the input block to the user", "向用户显示输入块", False),
    (r"and confirm source/period", "并确认来源/期间", False),
    (r"before building formulas", "在构建公式之前", False),
    (r"After building operating metrics formulas", "构建运营指标公式后", False),
    (r"show calculated margins to the user", "向用户显示计算的利润率", False),
    (r"and sanity-check them", "并进行合理性检查", False),
    (r"before moving to valuation", "在转向估值之前", False),
    (r"After building valuation multiples", "构建估值倍数后", False),
    (r"show multiples to the user", "向用户显示倍数", False),
    (r"and confirm they look reasonable", "并确认它们看起来合理", False),
    (r"before adding statistics", "在添加统计之前", False),
    (r"Don't build the entire worksheet end-to-end then present", "不要端到端构建整个工作表然后展示", False),
    (r"catch mistakes early by confirming at each section", "通过在每个部分确认来尽早捕获错误", False),

    # 核心金融术语短语
    (r"Comparable Company Analysis", "可比公司分析", False),
    (r"Discounted Cash Flow", "折现现金流", False),
    (r"Leveraged Buyout", "杠杆收购", False),
    (r"Three-Statement Model", "三表模型", False),
    (r"Income Statement", "利润表", False),
    (r"Balance Sheet", "资产负债表", False),
    (r"Cash Flow Statement", "现金流量表", False),
    (r"Enterprise Value", "企业价值", False),
    (r"Market Cap", "市值", False),
    (r"EBITDA", "息税折旧摊销前利润", False),
    (r"Free Cash Flow", "自由现金流", False),
    (r"WACC", "加权平均资本成本", False),
    (r"Terminal Value", "终值", False),
    (r"Gross Margin", "毛利率", False),
    (r"Operating Margin", "营业利润率", False),
    (r"Net Income", "净利润", False),
    (r"Sensitivity Analysis", "敏感性分析", False),
    (r"Bear Case", "悲观情景", False),
    (r"Base Case", "基准情景", False),
    (r"Bull Case", "乐观情景", False),
    (r"Earnings Analysis", "财报分析", False),
    (r"Earnings Preview", "财报前瞻", False),
    (r"Initiating Coverage", "覆盖启动报告", False),
    (r"Model Update", "模型更新", False),
    (r"Morning Note", "晨会纪要", False),
    (r"Sector Overview", "行业全景", False),
    (r"Thesis Tracker", "投资论点跟踪", False),
    (r"Catalyst Calendar", "催化剂日历", False),
    (r"Idea Generation", "选股筛选", False),
    (r"Confidential Information Memorandum", "保密信息备忘录", False),
    (r"Buyer List", "买家清单", False),
    (r"Merger Model", "并购模型", False),
    (r"Deal Sourcing", "项目发掘", False),
    (r"Deal Screening", "项目筛选", False),
    (r"Due Diligence", "尽职调查", False),
    (r"Unit Economics", "单元经济", False),
    (r"Returns Analysis", "回报分析", False),
    (r"Portfolio Monitoring", "投后监控", False),
    (r"Value Creation Plan", "价值创造计划", False),
    (r"Financial Plan", "财务规划", False),
    (r"Investment Proposal", "投资提案", False),
    (r"Portfolio Rebalancing", "组合再平衡", False),
    (r"Tax Loss Harvesting", "税损收割", False),
    (r"Accrual Schedule", "应计调度", False),
    (r"Break Trace", "断点追溯", False),
    (r"GL Reconciliation", "总账对账", False),
    (r"NAV Tieout", "NAV核对", False),
    (r"Variance Commentary", "差异评述", False),
    (r"Roll Forward", "滚动结转", False),

    # 常用动词短语
    (r"Build a (.+?) model", r"构建\1模型", True),
    (r"Create a (.+?) analysis", r"创建\1分析", True),
    (r"Generate (.+?) output", r"生成\1输出", True),
    (r"Perform (.+?) analysis", r"执行\1分析", True),
    (r"Calculate (.+?) metrics", r"计算\1指标", True),
    (r"Verify that", "验证", False),
    (r"Confirm that", "确认", False),
    (r"Check for", "检查", False),
    (r"Ensure that", "确保", False),
    (r"Validate (.+?) data", r"验证\1数据", True),
    (r"Cross-check", "交叉检查", False),
    (r"Review the", "审查", False),
    (r"Analyze the", "分析", False),
    (r"Assess the", "评估", False),
    (r"Evaluate the", "评价", False),

    # 常用名词短语
    (r"financial metrics", "财务指标", False),
    (r"operating metrics", "运营指标", False),
    (r"valuation multiples", "估值倍数", False),
    (r"statistical benchmarks", "统计基准", False),
    (r"Excel spreadsheet", "Excel电子表格", False),
    (r"public company valuation", "上市公司估值", False),
    (r"M&A analysis", "并购分析", False),
    (r"investment analysis", "投资分析", False),
    (r"peer benchmarking", "同业对标", False),
    (r"IPO pricing", "IPO定价", False),
    (r"pricing round", "融资轮定价", False),
    (r"identifying valuation anomalies", "识别估值异常", False),
    (r"investment committee presentation", "投资委员会演示", False),
    (r"industry overview report", "行业概览报告", False),
    (r"private companies", "私营公司", False),
    (r"comparable public companies", "可比上市公司", False),
    (r"highly diversified conglomerates", "高度多元化的企业集团", False),
    (r"distressed/bankrupt companies", "困境/破产公司", False),
    (r"pre-revenue startups", "尚未产生收入的初创公司", False),
    (r"unique business models", "独特商业模式的公司", False),

    # 数据源相关
    (r"data sources", "数据源", False),
    (r"data source", "数据源", False),
    (r"MCP servers", "MCP服务器", False),
    (r"Bloomberg terminal", "Bloomberg终端", False),
    (r"SEC EDGAR filings", "SEC EDGAR文件", False),
    (r"institutional sources", "机构来源", False),
    (r"primary data source", "主要数据源", False),
    (r"web search", "网络搜索", False),
    (r"verified institutional-grade data", "经过验证的机构级数据", False),
    (r"proper citations", "适当的引用", False),
    (r"outdated search results", "过时的搜索结果", False),
    (r"unreliable for financial analysis", "对金融分析不可靠", False),

    # Excel相关
    (r"Excel formula", "Excel公式", False),
    (r"hardcoded values", "硬编码值", False),
    (r"pre-computed numbers", "预计算的数字", False),
    (r"cell reference", "单元格引用", False),
    (r"audit trail", "审计追踪", False),
    (r"transparency", "透明度", False),
    (r"range formulas", "范围公式", False),
    (r"range values", "范围值", False),
    (r"worksheet", "工作表", False),
    (r"workbook", "工作簿", False),
    (r"merged cells", "合并单元格", False),
    (r"formatting", "格式化", False),
    (r"conditional formatting", "条件格式", False),
    (r"data validation", "数据验证", False),

    # 方法和论
    (r"methodology", "方法论", False),
    (r"framework", "框架", False),
    (r"principles", "原则", False),
    (r"guidelines", "指导原则", False),
    (r"best practices", "最佳实践", False),
    (r"quality checks", "质量检查", False),
    (r"sanity checks", "合理性检查", False),
    (r"output checklist", "输出检查清单", False),
    (r"workflow", "工作流程", False),
    (r"step-by-step", "分步", False),
    (r"practical tips", "实用技巧", False),
    (r"professional tips", "专业技巧", False),

    # 行业和板块
    (r"Software/SaaS", "软件/SaaS", False),
    (r"Financial Services", "金融服务", False),
    (r"Manufacturing/Industrial", "制造/工业", False),
    (r"Retail/E-commerce", "零售/电商", False),
    (r"Healthcare", "医疗保健", False),
    (r"Consumer", "消费", False),
    (r"Technology", "科技", False),
    (r"Industrial", "工业", False),

    # 公司和企业
    (r"public companies", "上市公司", False),
    (r"private companies", "私营公司", False),
    (r"comparable companies", "可比公司", False),
    (r"peer group", "同行组", False),
    (r"peer companies", "同行公司", False),
    (r"target company", "目标公司", False),
    (r"business model", "业务模式", False),
    (r"management team", "管理团队", False),

    # 时间和期间
    (r"LTM \\(Last Twelve Months\\)", "LTM（过去十二个月）", False),
    (r"Year-over-year", "同比", False),
    (r"Quarter-over-quarter", "环比", False),
    (r"fiscal year", "财政年度", False),
    (r"period", "期间", False),
    (r"time period", "时间段", False),
    (r"historical", "历史的", False),
    (r"projected", "预测的", False),
    (r"forecast", "预测", False),
    (r"projection", "预测", False),

    # 通用术语
    (r"skill", "技能", False),
    (r"template", "模板", False),
    (r"analysis", "分析", False),
    (r"report", "报告", False),
    (r"data", "数据", False),
    (r"financial", "金融", False),
    (r"investment", "投资", False),
    (r"banking", "银行", False),
    (r"equity", "股权", False),
    (r"research", "研究", False),
    (r"portfolio", "投资组合", False),
    (r"asset", "资产", False),
    (r"liability", "负债", False),
    (r"debt", "债务", False),
    (r"cash", "现金", False),
    (r"revenue", "收入", False),
    (r"growth", "增长", False),
    (r"margin", "利润率", False),
    (r"profit", "利润", False),
    (r"loss", "亏损", False),
    (r"risk", "风险", False),
    (r"return", "回报", False),
    (r"company", "公司", False),
    (r"market", "市场", False),
    (r"industry", "行业", False),
    (r"sector", "板块", False),
    (r"metric", "指标", False),
    (r"ratio", "比率", False),
    (r"multiple", "倍数", False),
    (r"value", "价值", False),
    (r"valuation", "估值", False),
    (r"model", "模型", False),
    (r"spreadsheet", "电子表格", False),
    (r"output", "输出", False),
    (r"input", "输入", False),
]

def translate_text_fluent(text):
    """使用短语级翻译产生流畅中文"""
    if not text:
        return text

    result = text

    # 按长度降序处理（先匹配长短语）
    for en, zh, is_regex in sorted(TRANSLATIONS, key=lambda x: len(x[0]), reverse=True):
        try:
            if is_regex:
                # 使用正则替换
                result = re.sub(en, zh, result, flags=re.IGNORECASE)
            else:
                # 使用字面替换
                result = re.sub(r'\b' + re.escape(en) + r'\b', zh, result, flags=re.IGNORECASE)
        except Exception as e:
            # 跳过有问题的替换
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

print("开始高质量短语级翻译...")
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
js_content = "// 技能完整中文翻译数据 - 高质量短语级翻译\n"
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
