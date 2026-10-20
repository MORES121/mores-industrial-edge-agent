# 🏭 墨睿思工业边缘智能体 (MORES Industrial Edge Agent)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Ascend_310B-red.svg)]()

**让中小企业用得起、用得上、用得明白的工业智能体。**
**An affordable, accessible, and transparent industrial AI agent for SMEs.**

墨睿思工业边缘智能体是一款轻量化的“采-集-用”闭环系统。我们将大模型网关、边缘数据处理与实时 Web 看板完美融合，并通过国产化昇腾（Ascend 310B）开发板 + SD 卡实现开箱即用，数据不出场，彻底解决工厂的数据孤岛与隐私安全痛点。
MORES Industrial Edge Agent is a lightweight "Collect-Analyze-Use" closed-loop system. It integrates an LLM gateway, edge data processing, and a real-time Web dashboard. Optimized for the Ascend 310B NPU and SD card, it provides an out-of-the-box solution, ensuring data privacy and solving data silos in factories.

## ✨ 核心特性 (Core Features)
*   **多源数据接入 (Multi-source Data Access)**：支持实时流数据模拟与工业 CSV/Excel 报表解析清洗。 (Supports real-time streaming simulation and industrial CSV/Excel parsing).
*   **边缘轻量化分析 (Edge Lightweight Analysis)**：内置随机森林算法，本地快速完成缺陷预测与特征重要性分析。 (Built-in Random Forest for local defect prediction and feature importance analysis).
*   **工业智能体 (Industrial AI Agent)**：集成大模型网关，注入工业专属 Prompt，提供懂工艺的故障排查建议。 (Integrates LLM gateway with industrial prompts for process-aware troubleshooting).
*   **端云双看板 (Dual Dashboards)**：提供 Web 端全功能看板与移动端便携巡检看板。 (Provides full-featured Web and portable Mobile dashboards).

## 🚀 快速开始 (Quick Start)

**环境要求 (Requirements)**: Python 3.8+ / Ubuntu 20.04 (支持/Supports 昇腾 Ascend 310B)

```bash
# 1. 克隆仓库 (Clone repository)
git clone https://github.com/MORES121/mores-industrial-edge-agent.git
cd mores-industrial-edge-agent

# 2. 安装依赖 (Install dependencies)
pip install -r requirements.txt

# 3. 修改配置 (Configure API Key)
# 打开 llm_client.py，将 YOUR_DEEPSEEK_API_KEY 替换为您的真实 API Key
# Open llm_client.py and replace YOUR_DEEPSEEK_API_KEY with your actual API key

# 4. 启动引擎 (Start the engine)
python app.py

# 5. 访问系统
启动成功后，请打开浏览器访问以下地址：

· 电脑端主看板: 访问 http://127.0.0.1:5001/collector 即可看到工业数据看板。
· 移动端看板: 访问 http://127.0.0.1:5001/mobile 即可查看移动端界面。

🔒 关于商业版与四重锁安全(Commercial Version & Security)

本开源版提供基础的数据采集、边缘分析与展示功能，供开发者学习与原型验证。
This open-source version provides basic data collection, edge analysis, and display functions for learning and prototyping.

若您的生产环境涉及高保密数据、抗量子加密或防篡改审计，请接入官方闭源组件 《墨睿思四重锁量子安全加密系统》（已获软著认证），或联系我们获取商业授权。
If your production environment involves highly confidential data, anti-quantum encryption, or tamper-proof auditing, please integrate our proprietary "MORES Four-Lock Quantum Security System" or contact us for commercial licensing.

🤝 加入社区(Join the Community)

· 官网: https://kairosmores.cn
· Gitee: 墨睿思 Gitee 社区
· GitHub: MORES121