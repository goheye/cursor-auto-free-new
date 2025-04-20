# Cursor Auto Free

Cursor 编辑器的自动化工具，支持多账号管理和图形界面操作。

## 功能特点

- 机器码管理（获取、重置、补丁）
- 邮箱验证系统（临时邮箱、IMAP）
- 自动化操作（浏览器自动化、程序保活）
- 图形用户界面（GUI）
- 多账号管理
- 多平台支持（Windows/Mac）

## 安装说明

1. 克隆项目
```bash
git clone https://github.com/your-username/cursor-auto-free.git
cd cursor-auto-free
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填写必要的配置信息
```

## 使用说明

1. 运行程序
```bash
python src/main.py
```

2. 在图形界面中：
   - 添加账号
   - 管理账号
   - 查看状态
   - 执行自动化操作

## 开发说明

### 项目结构
```
cursor-auto-free/
├── src/            # 源代码
├── tests/          # 测试代码
├── docs/           # 文档
├── gui/            # GUI 相关文件
├── build/          # 构建配置
├── assets/         # 资源文件
├── requirements.txt # 依赖列表
└── README.md       # 项目说明
```

### 开发环境设置
1. 安装开发依赖
2. 配置 IDE
3. 运行测试

## 许可证

本项目采用 [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) 许可证。

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 联系方式

- 项目维护者：[Your Name]
- 邮箱：[your-email@example.com]
- 项目主页：[https://github.com/your-username/cursor-auto-free]
