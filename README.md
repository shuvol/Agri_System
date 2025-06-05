# 🌱 智慧农业大脑框架

本项目旨在构建一个面向智慧农业的智能大脑系统，整合多种 AI 能力，通过工作流编排、服务化部署与工具封装，提升农业生产的自动化与智能化水平。

---

## 📁 项目结构与模块说明

### 1. `src/` - 存放各类子图


### 2. `src/primary_graph/` - 存放总图


### 3. `src/primary_graph/subgraph/` - 存放各个子图在总图的调用方法


---

## ✅ TODO List

### ✅ 已完成项

- [x] 智慧农业大脑基础框架搭建
- [x] 环境监测助理模块
- [x] 病虫害管理助理模块

### 🚧 进行中 / 待完成项

- [ ] 作物生长监测子助理模块
- [ ] 农机调度决策子助理模块
- [ ] 水肥管理子助理模块
- [ ] `MCP_Servers` 模块功能完善
- [ ] 检索增强生成（RAG）能力集成
- [ ] RESTFUL风格后端接口更改

---
## 🚀 快速开始

```bash
# 安装依赖（建议使用 conda）
pip install -r requirements.txt

# 配置环境变量
根目录下按照.env.example创建自己的.env文件,在.env文件中配置自己所需要的环境变量
注意!env文件不要输入中文,会影响LangGraph Studio的运行!

# 启动 MCP 服务
python MCP_Servers/environment_server.py

# 启动 LangGraph 流程测试
python graphchat/main.py

# 启动 LangGraph Studio
pip install -U "langgraph-cli[inmem]"
langgraph dev
