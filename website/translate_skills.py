#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量翻译SKILL.md文件并生成skill-translations.js
"""
import os
import re
import json

def translate_skills_to_chinese():
    """读取所有SKILL.md文件，翻译成中文，生成JavaScript数据"""

    # 定义技能文件路径映射
    skill_files = {
        # 金融分析
        "comps": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/01-comps-可比公司分析/SKILL.md",
        "dcf": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/02-dcf-估值模型/SKILL.md",
        "lbo": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/03-lbo-杠杆收购/SKILL.md",
        "3stmt": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/04-三表模型/SKILL.md",
        "audit": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/05-Excel审计/SKILL.md",
        "data-cleaning": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/06-数据清洗/SKILL.md",
        "competitive-analysis": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/07-竞品分析/SKILL.md",
        "ppt-template": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/08-PPT模板创建/SKILL.md",
        "deck-refresh": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/09-Deck刷新/SKILL.md",
        "deck-qc": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/10-Deck质检/SKILL.md",
        "ppt-gen": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/11-PPT生成/SKILL.md",
        "xlsx-gen": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/12-XLSX生成/SKILL.md",
        "skill-builder": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/01-金融分析/13-技能创建器/SKILL.md",

        # 权益研究
        "earnings": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/02-权益研究/01-earnings-财报分析/SKILL.md",
        "earnings-preview": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/02-权益研究/02-earnings-preview-财报前瞻/SKILL.md",
        "initiating-coverage": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/02-权益研究/03-覆盖启动报告/SKILL.md",
        "model-update": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/02-权益研究/04-模型更新/SKILL.md",
        "morning-note": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/02-权益研究/05-晨会纪要/SKILL.md",
        "thesis-tracker": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/02-权益研究/07-投资论点跟踪/SKILL.md",
        "sector-overview": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/02-权益研究/06-行业全景/SKILL.md",
        "catalyst-calendar": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/02-权益研究/08-催化剂日历/SKILL.md",
        "idea-generation": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/02-权益研究/09-选股筛选/SKILL.md",

        # 投行
        "cim": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/03-投行/01-CIM起草/SKILL.md",
        "teaser": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/03-投行/02-teaser-匿名简介/SKILL.md",
        "buyer-list": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/03-投行/03-买家清单/SKILL.md",
        "merger-model": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/03-投行/04-并购模型/SKILL.md",
        "process-letter": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/03-投行/05-流程函/SKILL.md",
        "strip-profile": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/03-投行/06-公司一页/SKILL.md",
        "pitch-deck": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/03-投行/07-pitch-deck/SKILL.md",
        "datapack": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/03-投行/08-数据包/SKILL.md",
        "deal-tracker": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/03-投行/09-交易跟踪/SKILL.md",

        # 私募股权
        "deal-sourcing": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/01-项目发掘/SKILL.md",
        "deal-screening": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/02-项目筛选/SKILL.md",
        "dd-checklist": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/03-尽调清单/SKILL.md",
        "dd-meeting-prep": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/04-尽调会议准备/SKILL.md",
        "unit-economics": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/05-单元经济/SKILL.md",
        "returns-analysis": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/06-回报分析/SKILL.md",
        "ic-memo": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/07-IC备忘录/SKILL.md",
        "portfolio-monitoring": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/08-投后监控/SKILL.md",
        "value-creation-plan": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/09-价值创造计划/SKILL.md",
        "ai-readiness": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/04-私募股权/10-AI就绪度/SKILL.md",

        # 财富管理
        "financial-plan": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/05-财富管理/03-财务规划/SKILL.md",
        "client-meeting": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/05-财富管理/02-客户会议准备/SKILL.md",
        "investment-proposal": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/05-财富管理/04-投资提案/SKILL.md",
        "portfolio-rebalance": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/05-财富管理/05-组合再平衡/SKILL.md",
        "tax-loss-harvesting": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/05-财富管理/06-税损收割/SKILL.md",
        "client-report": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/05-财富管理/01-客户报告/SKILL.md",

        # 基金管理
        "accrual-schedule": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/06-基金管理/01-应计调度/SKILL.md",
        "break-trace": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/06-基金管理/02-断点追溯/SKILL.md",
        "gl-recon": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/06-基金管理/03-总账对账/SKILL.md",
        "nav-tieout": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/06-基金管理/04-NAV核对/SKILL.md",
        "variance-commentary": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/06-基金管理/06-差异评述/SKILL.md",
        "roll-forward": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/06-基金管理/05-滚动结转/SKILL.md",

        # KYC
        "kyc-parse": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/07-运营KYC/01-文档解析/SKILL.md",
        "kyc-rules": "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/07-运营KYC/02-规则引擎/SKILL.md",
    }

    translations = {}

    for skill_id, file_path in skill_files.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 保存原始英文内容
                translations[skill_id] = {
                    'original': content,
                    'translated': None  # 翻译将稍后添加
                }
                print(f"✓ 读取 {skill_id}: {len(content)} 字符")
            except Exception as e:
                print(f"✗ 读取 {skill_id} 失败: {e}")
        else:
            print(f"✗ 文件不存在: {file_path}")

    return translations

if __name__ == "__main__":
    translations = translate_skills_to_chinese()
    print(f"\n共读取 {len(translations)} 个技能文件")

    # 保存到JSON文件
    output_path = "/Users/xieyan/vscode/Anthropics的金融分析工具/学习版/website/skill-translations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    print(f"✓ 已保存到 {output_path}")
