# 金融分析技能库学习版

基于 Anthropic Claude FSI 插件库的中文学习版网站，涵盖投行、私募股权、财富管理、会计、合规等金融核心领域的 55 个专业技能。

## ✨ 特性

- 📚 **55个金融技能** - 涵盖投行、私募股权、财富管理、会计、合规等核心领域
- 🌍 **中英文双语** - 支持中英文无缝切换
- 📱 **响应式设计** - 完美适配桌面、平板、手机
- 🎨 **专业UI设计** - 采用金融行业风格的视觉设计
- 📖 **结构化文档** - 每个技能包含概述、分析步骤、关键原则
- 🔍 **快速导航** - 左侧目录固定，支持点击跳转

## 🚀 快速开始

### 在线访问

访问在线演示：[https://ahtonyyan.github.io/anthropics-financial-services-cn-study/](https://ahtonyyan.github.io/anthropics-financial-services-cn-study/)

### 本地运行

```bash
# 克隆仓库
git clone https://github.com/ahtonyyan/anthropics-financial-services-cn-study.git
cd anthropics-financial-services-cn-study/学习版/website

# 启动本地服务器
python server.py

# 或使用 Python 内置服务器
python -m http.server 8000
```

然后在浏览器中打开 `http://localhost:8000`

## 📁 项目结构

```
学习版/
├── website/                 # 网站文件
│   ├── index.html          # 首页
│   ├── skill.html          # 技能详情页
│   ├── vertical-*.html     # 垂直分类页面
│   ├── translations/       # 翻译文件
│   └── server.py          # 本地服务器
├── 01-投行/                # 投行相关技能
├── 02-卖方/                # 卖方顾问技能
├── 03-私募股权/            # 私募股权技能
├── 04-财富管理/            # 财富管理技能
├── 05-运营/                # 运营相关技能
├── 06-会计/                # 会计技能
├── 07-合规/                # 合规技能
└── managed-agent-cookbooks/ # Claude 托管代理配置
```

## 📊 技能分类

### 01-投行 (Investment Banking)
- **可比公司分析 (Comps)** - 上市公司估值分析
- **DCF估值** - 折现现金流模型
- **LBO模型** - 杠杆收购分析
- **三表联动** - 财务报表建模
- **Excel模型审计** - 模型质量控制
- **数据清洗** - 财务数据处理
- **竞争分析** - 行业竞争格局研究
- **财报分析** - 上市公司财报解读

### 02-卖方 (M&A Advisory)
- **并购模型** - 收购兼并分析
- **融资演示文稿** - 投资推介材料
- **投委会备忘录** - 投资决策文档
- **财务规划** - 财务预测模型
- **KYC信息解析** - 客户身份识别

### 03-私募股权 (Private Equity)
- **财报预览** - 财报预期分析
- **首次覆盖报告** - 股票研究报告
- **模型更新** - 模型维护更新
- **晨会笔记** - 投资晨会纪要
- **投资论点跟踪** - 投资逻辑监控
- **行业概览** - 行业研究报告
- **催化剂日历** - 事件驱动分析
- **投资想法生成** - 机会挖掘

### 04-财富管理 (Wealth Management)
- **客户会议** - 客户沟通服务
- **投资建议** - 资产配置建议
- **投资组合再平衡** - 组合调整
- **税收损失收割** - 税务优化

### 05-运营 (Operations)
- **应计进度表** - 权责发生制
- **余额分解追踪** - 账户变动分析
- **净值对账** - 基金净值核算
- **差异分析说明** - 预算差异解释

### 06-会计 (Accounting)
- **总账对账** - 账务核对流程
- **PPT生成** - 演示文稿自动化
- **Excel生成** - 报表自动化
- **技能构建器** - 技能文档工具

### 07-合规 (Compliance)
- **KYC规则管理** - 合规规则引擎
- **文档解析** - 合规文档处理

## 🛠️ 技术栈

- **前端**: 纯 HTML + CSS + JavaScript
- **字体**: Noto Serif SC (中文) + Inter (英文)
- **设计**: 响应式布局、渐变背景、卡片式设计
- **图标**: Emoji 表情符号

## 📝 技能文档结构

每个技能包含以下部分：

1. **概述** - 技能简介和核心原则
2. **分析步骤** - 详细的操作步骤
   - 做什么：具体操作
   - 为什么：操作目的
   - 注意：关键提示
3. **关键原则** - 核心要点总结

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目基于 Apache License 2.0 开源。

## 🙏 致谢

- 基于 [Anthropic Claude FSI Plugin Library](https://github.com/anthropics/financial-services-plugins)
- 使用 Claude Code 进行开发和文档生成

## 📞 联系方式

- GitHub Issues: [https://github.com/ahtonyyan/anthropics-financial-services-cn-study/issues](https://github.com/ahtonyyan/anthropics-financial-services-cn-study/issues)

---

**注意**: 本项目为学习版，仅供学习和参考使用。
