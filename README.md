# 🛍️ Marketa-Pro 电商内容 Agent 平台

Marketa-Pro是一款面向电商品牌、小型营销代理公司、创作者团队的AI Agent平台，用于一站式生成平台适配的营销内容包（图文、封面图、KOL brief等），并可通过多智能体协作完成内容的生成、优化、复盘和节奏推荐。

## 🎯 项目简介

本平台的目标是用AI取代原本由内容团队完成的大量重复性内容策划、写作、设计和投放协作工作。核心用户群包括小型电商品牌主（主营淘宝、小红书、抖音）、营销设计外包工作室和KOL运营人员。

## 🏗️ 系统架构

系统采用多Agent协作架构，主要组件包括：

1. **Orchestrator Agent**: 调度所有下游Agent、管理任务状态和执行链
2. **规划层**:
   - Trend Radar Agent: 调用外部趋势接口，识别商品所属平台近期热词和内容走向
   - Campaign Planner Agent: 拆解任务目标，输出内容风格、受众方向、输出要求结构
3. **内容生成层**:
   - 文案Agent: 生成段落式内容文案
   - 图像Agent: 生成配套场景图、情绪图
   - CTA Agent: 生成平台适配的call-to-action文案
   - 视频脚本Agent: 生成短视频文案与分镜
4. **执行层**:
   - Multichannel Publish Agent: 模拟将内容结构导出为不同平台格式
   - KOL Brief Generator: 输出标准的达人合作内容简报
5. **监控和优化层**:
   - 包括数据收集、互动追踪、评论反馈和A/B测试等功能

## 🚀 快速开始

1. 安装依赖：
   ```
   pip install google-adk
   ```

2. 运行示例：
   ```
   python main.py
   ```

## 📝 使用示例

```python
from agents import OrchestratorAgent
import asyncio

async def run_example():
    # 初始化Orchestrator Agent
    orchestrator = OrchestratorAgent()
    
    # 准备用户输入
    user_input = {
        "goal": "新品种草",
        "product_title": "智能保温杯",
        "product_selling_points": "24小时保温、APP显示水温、提醒喝水功能",
        "product_tags": "科技,健康,生活方式",
        "platform": "小红书",
        "brand_tone": "简约科技",
        "audience": "25-35岁都市年轻人"
    }
    
    # 处理请求
    result = await orchestrator.process_user_input(user_input)
    print(result)

# 运行示例
asyncio.run(run_example())
```

## 📌 项目状态

- [x] Orchestrator Agent基础框架
- [ ] 规划层Agent实现
- [ ] 内容生成层Agent实现
- [ ] 执行层Agent实现
- [ ] 监控和优化层Agent实现
- [ ] 完整闭环工作流整合

## 📄 许可证

[MIT](LICENSE) 