# -*- coding: utf-8 -*-
# ==============================================================================
# MORES Industrial Edge Agent (墨睿思工业边缘智能体) - Main Application
# Description: Lightweight industrial data collection and AI analysis system.
# 描述: 轻量化工业数据采集与 AI 分析系统主入口。
# ==============================================================================
import os
import time
import random
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import logging

# Import local pure modules (导入本地纯净模块)
from llm_client import llm
from ai_formatter import format_response

# Setup logging (配置日志系统)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app (初始化 Flask 应用)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

# ==============================================================================
# Auto-generate test data for out-of-the-box experience
# (自动生成测试数据，确保开箱即用，无数据不报错)
# ==============================================================================
sample_csv = 'data/sample_data.csv'
if not os.path.exists(sample_csv):
    logger.info("Generating sample data... (生成测试数据集...)")
    df_test = pd.DataFrame({
        'timestamp': [time.strftime('%Y-%m-%d %H:%M:%S') for _ in range(20)],
        'machine_id': ['M-001'] * 20,
        'injection_pressure': np.random.uniform(40, 60, 20),
        'melt_temp': np.random.uniform(200, 240, 20),
        'mold_temp': np.random.uniform(50, 80, 20),
        'hold_pressure': np.random.uniform(30, 50, 20),
        'cycle_time': np.random.uniform(10, 15, 20),
        'defect_rate': np.random.uniform(0.01, 0.05, 20)
    })
    df_test.to_csv(sample_csv, index=False)

# ==============================================================================
# Routes: Frontend Pages (路由：前端页面)
# ==============================================================================
@app.route('/')
@app.route('/collector')
def collector_index():
    """Render PC dashboard (渲染电脑端看板)"""
    return render_template('collector.html')

@app.route('/mobile')
def mobile_page():
    """Render Mobile dashboard (渲染移动端看板)"""
    return render_template('mobile.html')

# ==============================================================================
# Routes: Data Collection APIs (路由：数据采集 API)
# ==============================================================================
@app.route('/api/collector/real-time')
def api_real_time():
    """
    Real-time data simulator (实时数据模拟接口)
    Simulates sensor data. In production, replace with PLC/MQTT connection.
    (模拟传感器数据。生产环境中，请替换为真实的 PLC/MQTT 硬件连接逻辑)
    """
    data = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'machine_id': 'M-001',
        'temperature': round(65 + random.uniform(-5, 15), 1),
        'pressure': round(40 + random.uniform(-3, 5), 1),
        'vibration': round(random.uniform(0.1, 0.8), 2),
        'cycle_time': round(12 + random.uniform(-1, 2), 1),
        'status': '运行' if random.random() > 0.08 else '预警',
        'defect_rate': round(random.uniform(0.005, 0.035), 4)
    }
    return jsonify(data)

@app.route('/api/collector/summary')
def api_summary():
    """Get data summary (获取数据摘要统计)"""
    try:
        df = pd.read_csv('data/sample_data.csv')
        summary = {
            'total_records': len(df),
            'avg_defect_rate': round(df['defect_rate'].mean() * 100, 2),
            'max_defect_rate': round(df['defect_rate'].max() * 100, 2),
            'min_defect_rate': round(df['defect_rate'].min() * 100, 2),
            'avg_cycle_time': round(df['cycle_time'].mean(), 1),
            'machines': df['machine_id'].nunique()
        }
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Data summary failed: {e}")
        return jsonify({'error': '暂无数据 (No data available)'})

@app.route('/api/collector/upload', methods=['POST'])
def api_upload():
    """Handle file upload and parse (处理文件上传与解析)"""
    if 'file' not in request.files:
        return jsonify({'error': '未上传文件 (No file uploaded)'})
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith(('.csv', '.xlsx')):
        return jsonify({'error': '文件为空或格式不支持 (Empty or unsupported format)'})
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        df = pd.read_csv(filepath) if filename.endswith('.csv') else pd.read_excel(filepath)
        return jsonify({'success': True, 'rows': len(df), 'msg': '上传解析成功 (Parsed successfully)'})
    except Exception as e:
        logger.error(f"Upload parse failed: {e}")
        return jsonify({'error': f'解析失败 (Parse failed): {str(e)}'})

# ==============================================================================
# Routes: AI & Analysis APIs (路由：AI 与分析 API)
# ==============================================================================
@app.route('/api/collector/train', methods=['POST'])
def api_train():
    """
    Train lightweight ML model (训练轻量化机器学习模型)
    Using Random Forest for defect prediction.
    (使用随机森林回归算法进行缺陷率预测)
    """
    try:
        df = pd.read_csv('data/sample_data.csv')
        features = ['injection_pressure', 'melt_temp', 'mold_temp', 'hold_pressure']
        X = df[features]
        y = df['defect_rate']
        
        model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
        model.fit(X, y)
        preds = model.predict(X)
        
        return jsonify({
            'success': True,
            'mae': round(mean_absolute_error(y, preds), 4),
            'r2': round(r2_score(y, preds), 4)
        })
    except Exception as e:
        logger.error(f"Model training failed: {e}")
        return jsonify({'error': f'训练失败 (Train failed): {str(e)}'})

# Define AI Identity (定义 AI 智能体身份提示词)
IDENTITY = """你是墨睿思工业智能体，专注于工业数据采集、智能分析与决策辅助。
回答风格：段落清晰，先总述再分点，专业且通俗易懂。
(You are MORES Industrial AI Agent, focusing on industrial data analysis. Respond clearly and professionally in Chinese.)"""

@app.route('/api/ai/chat', methods=['POST'])
def api_ai_chat():
    """Handle AI chat interaction (处理 AI 对话交互)"""
    data = request.get_json()
    question = data.get('question', '')
    
    full_prompt = f"{IDENTITY}\n\n用户问题(User Question)：{question}"
    
    # Call LLM gateway (调用大模型网关)
    result = llm.chat(full_prompt)
    raw_answer = result.get('choices', [{}])[0].get('message', {}).get('content', '')
    
    # Format response with icons and structure (格式化输出：排版与图标)
    return jsonify({'answer': format_response(raw_answer)})

if __name__ == '__main__':
    logger.info("Starting MORES Industrial Edge Agent... (启动墨睿思工业边缘智能体...)")
    app.run(host='0.0.0.0', port=5001, debug=True)