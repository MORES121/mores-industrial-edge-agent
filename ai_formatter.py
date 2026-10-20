# ==============================================================================
# MORES Industrial Edge Agent - LLM Gateway
# 大模型网关接口，支持 DeepSeek / Qwen 等云端模型。
# ==============================================================================

# 墨睿思工业智能体 · 输出格式化器

import re

def format_ai_response(text):
    """格式化AI输出为整齐段落 + 图标 + 企业文化"""
    
    if not text or len(text) < 10:
        return text
    
    # 移除多余换行
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    
    # 按句子拆分段落（每2-3句一段）
    sentences = re.split(r'(?<=[。！？])\s*', text)
    sentences = [s for s in sentences if s.strip()]
    
    # 构建格式化段落
    formatted_parts = []
    
    # 检测是否为列表/要点风格
    if any('。' not in s and '，' in s and len(s) < 30 for s in sentences[:3]):
        # 要点风格
        for i, s in enumerate(sentences):
            if s.strip():
                icons = ['🔹', '🔸', '▪️', '▫️', '•']
                icon = icons[i % len(icons)]
                formatted_parts.append(f"{icon} {s.strip()}")
    else:
        # 段落风格（每2句合并一段）
        i = 0
        while i < len(sentences):
            para = sentences[i].strip()
            if i + 1 < len(sentences) and len(sentences[i + 1]) < 50:
                para += sentences[i + 1].strip()
                i += 2
            else:
                i += 1
            if para:
                formatted_parts.append(para)
    
    # 添加企业文化标识
    result = "\n\n".join(formatted_parts)
    
    # 如果内容包含建议或分析，添加互动引导
    if any(kw in text for kw in ['建议', '推荐', '优化', '改善', '提升']):
        result += "\n\n💡 如需更详细的分析，请告诉我您的具体需求，我将为您深入解答。"
    
    # 添加墨睿思品牌标识（每段回复结尾）
    result += "\n\n---\n*墨睿思 · 轻量化 · 可解释 · 国产化*"
    
    return result


def add_icons_to_answer(text):
    """根据内容自动添加图标"""
    
    icon_map = {
        '数据': '📊',
        '分析': '📈',
        '设备': '🏭',
        '机器': '🏭',
        '工艺': '⚙️',
        '优化': '⚡',
        '建议': '💡',
        '决策': '🎯',
        '预测': '🔮',
        '质量': '✅',
        '缺陷': '⚠️',
        '预警': '🚨',
        '温度': '🌡️',
        '压力': '📏',
        '效率': '🚀',
        '成本': '💰',
        '安全': '🔒',
        '国产': '🇨🇳'
    }
    
    # 在合适位置插入图标（不破坏现有结构）
    for keyword, icon in icon_map.items():
        if keyword in text and f'{icon}' not in text[:50]:
            # 在段落开头或关键句前插入
            text = text.replace(f'{keyword}', f'{icon} {keyword}', 1)
    
    return text


def format_response(raw_text):
    """完整格式化流程"""
    if not raw_text:
        return "墨睿思工业智能体正在思考，请稍后再问。"
    
    # 1. 基础格式化
    formatted = format_ai_response(raw_text)
    
    # 2. 添加图标
    formatted = add_icons_to_answer(formatted)
    
    # 3. 确保品牌标识
    if '墨睿思' not in formatted:
        formatted = "🤖 **墨睿思工业智能体**\n\n" + formatted
    
    return formatted
