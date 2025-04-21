# 简易分类广告系统 - 使用说明
## 📌 项目概述
这是一个基于Flask和MongoDB构建的简易分类广告系统，包含广告发布、浏览和数据统计功能。系统采用现代化的响应式设计，适配各种设备屏幕。
## ✨ 功能特性
### 核心功能
- ✅ 广告发布与管理
- ✅ 多维度数据统计与可视化
- ✅ 响应式网页设计
- ✅ 实时数据展示
### 统计面板特色
- 📊 交互式数据图表（饼图、柱状图、趋势图）
- 🔢 智能数据卡片（悬停动画、动态指标）
- 📈 7天趋势分析
- � 分类详细数据表格
## 🛠️ 技术栈
### 前端技术
- Bootstrap 5 - 响应式框架
- Chart.js - 数据可视化
- Font Awesome - 图标库
- jQuery - DOM操作
### 后端技术
- Python Flask - Web框架
- MongoDB - 数据库
- PyMongo - MongoDB驱动
## 🚀 快速开始
### 环境要求
- Python 3.8+
- MongoDB 4.4+
- Pipenv（推荐）或 pip
### 安装步骤
1. 克隆仓库：
```bash
git clone https://github.com/XXTZ-fia/toy_craigslist.git
cd toy_craigslist
```
2. 安装依赖：
```bash
conda create -n env python=3.9
conda activate env
conda install -r requirements.txt
```
3. 启动应用：
```bash
python app.py
```
4. 访问应用：
打开浏览器访问 
## 📊 统计页面说明
### 数据概览
- 广告总数及月增长率
- 今日新增广告数
- 平均价格和价格区间分布
- 活跃广告和总浏览量
### 图表功能
1. **分类分布图**：
   - 直观展示各分类广告占比
   - 悬停显示详细数据
2. **价格分布图**：
   - 四个价格区间的广告数量对比
   - 柱状图直观比较
3. **7天趋势图**：
   - 平滑曲线展示广告发布趋势
   - 每日数据点精确显示
