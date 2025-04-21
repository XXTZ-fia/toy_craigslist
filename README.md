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
git clone https://github.com/your-repo/simple-classified-ads.git
cd simple-classified-ads
```
2. 安装依赖：
```bash
conda create -n env python=3.9
conda activate env
conda install -r requirements.txt
```
3. 配置环境变量：
创建`.env`文件：
```ini
FLASK_APP=app.py
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/classified_ads
SECRET_KEY=your-secret-key-here
```
4. 启动应用：
```bash
flask run
```
5. 访问应用：
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
## 🖥️ 界面预览
### 统计面板
### 移动端适配
![移动端截图](https://example.com/screenshots/mobile-view.png)
## 📝 使用建议
1. **数据更新**：
   - 系统每小时自动更新统计数据
   - 手动刷新页面获取最新数据
2. **最佳实践**：
   - 使用Chrome/Firefox等现代浏览器
   - 推荐屏幕分辨率1920x1080以上
## 🤝 贡献指南
欢迎提交Pull Request或Issue：
1. Fork本仓库
2. 创建特性分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 打开Pull Request
## 📜 许可证
MIT License - 详情见LICENSE文件
## 📞 联系方式
如有问题请联系：your-email@example.com
---
> 提示：实际部署时请替换示例图片链接和联系方式，并根据需要调整配置参数。
