#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# MORES Industrial Edge Agent - Excel Collector Module
# 墨睿思工业边缘智能体 - 工业报表采集与清洗模块
# ==============================================================================
import os
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

class IndustrialExcelCollector:
    """Industrial Equipment Report Collector (工业设备报表采集器)"""
    
    def __init__(self):
        self.watch_folder = "data/industrial"
        os.makedirs(self.watch_folder, exist_ok=True)
        self.config = self._load_config()
        self.result_file = "data/analysis_result.json"
        self.processed_file = "data/processed_batches.json"
    
    def _load_config(self):
        """Load configuration (加载配置参数)"""
        default = {"target_defect_rate": 0.02}
        config_file = "data/collector.json"
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                return json.load(f)
        return default
    
    def _load_processed_batches(self):
        """Load processed batch history (加载已处理批次历史)"""
        if os.path.exists(self.processed_file):
            with open(self.processed_file, "r") as f:
                return set(json.load(f))
        return set()
    
    def _save_processed_batches(self, batches):
        """Save processed batches (保存已处理批次)"""
        with open(self.processed_file, "w") as f:
            json.dump(list(batches), f)
            
    def _load_accumulated_output(self):
        """Load accumulated output (加载累计产量)"""
        if os.path.exists(self.result_file):
            with open(self.result_file, "r") as f:
                data = json.load(f)
                return data.get("accumulated_output", 0)
        return 0
    
    def _save_accumulated_output(self, accumulated_output):
        """Save accumulated output (保存累计产量)"""
        with open(self.result_file, "w") as f:
            json.dump({"accumulated_output": accumulated_output, "last_update": datetime.now().isoformat()}, f, indent=2)

    def parse_device_excel(self, file_path):
        """
        Parse device Excel (解析设备参数报表)
        Extracts injection pressure and hold time.
        (提取注射压力与保压时间数据)
        """
        try:
            df = pd.read_excel(file_path, header=None)
            pressures, times = [], []
            for idx, row in df.iterrows():
                if idx < 2: continue
                try:
                    p = float(row[7]) if len(row) > 7 and pd.notna(row[7]) else 0
                    t = float(row[9]) if len(row) > 9 and pd.notna(row[9]) else 0
                    if p > 0 or t > 0:
                        pressures.append(p)
                        times.append(t)
                except: continue
            return sum(pressures), sum(times)
        except: return 0, 0

    def extract_all_quality_data(self, file_path):
        """Extract quality data (提取质量良品数据)"""
        quality_dict = {}
        try:
            df = pd.read_excel(file_path, header=None)
            for idx, row in df.iterrows():
                batch_text = None
                amount = 0
                for col in range(len(row)):
                    cell = str(row[col]) if pd.notna(row[col]) else ""
                    if "良品数" in cell and "批次" in cell:
                        batch_text = cell.replace("良品数", "").strip()
                        for j in range(col+1, len(row)):
                            try:
                                val = float(row[j]) if pd.notna(row[j]) else 0
                                if val > 0:
                                    amount = val
                                    break
                            except: continue
                        if amount > 0 and batch_text:
                            quality_dict[batch_text] = amount
                        break
            return quality_dict
        except: return {}

    def run(self):
        """Execute collection workflow (执行采集工作流)"""
        print("=" * 50)
        print("MORES Industrial Edge Collector vFinal (墨睿思边缘数据采集)")
        print(f"Time (时间): {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        device_files = list(Path(self.watch_folder).glob("*设备*.xlsx"))
        quality_files = list(Path(self.watch_folder).glob("*质检*.xlsx"))
        
        total_pressure = 0
        for f in device_files:
            p, t = self.parse_device_excel(f)
            total_pressure += p
            print(f"  Device Data (设备数据): {f.name} -> Pressure(压力): {p:,.2f}")
        
        all_quality = {}
        for f in quality_files:
            q_data = self.extract_all_quality_data(f)
            all_quality.update(q_data)
            
        processed_batches = self._load_processed_batches()
        current_accumulated = self._load_accumulated_output()
        
        new_output = 0
        for batch, amount in all_quality.items():
            if batch not in processed_batches:
                new_output += amount
                print(f"    ✅ New (新增): {batch} -> Yield(良品数): {amount:,.2f}")
                
        accumulated_output = current_accumulated + new_output
        processed_batches.update(all_quality.keys())
        
        # Calculate indicators (计算工业指标)
        actual_yield_rate = accumulated_output / total_pressure if total_pressure > 0 else 0
        print(f"\n📊 Summary (汇总)")
        print(f"Actual Yield Rate (实际良品率): {actual_yield_rate:.4%}")
        
        self._save_accumulated_output(accumulated_output)
        self._save_processed_batches(processed_batches)

if __name__ == "__main__":
    IndustrialExcelCollector().run()