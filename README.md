# Android UI 自动化测试项目

这是一个基于Appium的Android UI自动化测试项目，用于测试Android应用的UI功能和性能。项目使用Python作为主要开发语言，结合Appium实现对Android应用的自动化测试。

## 目录结构

```
├── common/          # 通用工具类
├── config/          # 配置文件
├── core/            # 核心功能模块
├── data/            # 测试数据和配置
├── operation/       # UI操作封装
├── testcase/        # 测试用例
├── requirements.txt # 项目依赖
└── README.md       # 项目说明
```

## 环境要求

### 基础环境
- Python 3.8+
- Node.js 14+
- Java Development Kit (JDK) 8+
- Android SDK
- Appium Server 2.0+

### Android设备要求
- Android 13.0
- 已启用开发者选项和USB调试
- 推荐使用Android Studio自带的模拟器

## 安装步骤

1. 克隆项目到本地：
```bash
git clone [项目地址]
cd android_ui_auto
```

2. 安装Python依赖包：
```bash
pip install -r requirements.txt
```

3. 安装和配置Appium Server：
```bash
npm install -g appium
appium driver install uiautomator2
```

4. 启动Appium Server：
```bash
appium
```

## 使用说明

1. 配置测试环境
   - 确保Android设备已连接并启用USB调试
   - 检查Appium Server是否正常运行

2. 运行测试
```bash
python -m pytest testcase/test_app_lifecycle.py -v
```

3. 查看测试报告
   - 测试完成后，可在项目根目录下查看测试报告

## 测试用例编写

1. 在`data`目录下创建测试步骤配置文件（YAML格式）
2. 在`testcase`目录下创建对应的测试用例文件
3. 遵循项目既定的测试框架编写测试用例

## 注意事项

- 运行测试前请确保设备环境配置正确
- 建议使用虚拟环境运行项目
- 定期清理测试日志文件

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交变更
4. 发起 Pull Request

## 许可证

[许可证类型]