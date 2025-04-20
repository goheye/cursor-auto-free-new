# 配置模块测试文档

## 概述

本文档详细说明了`test_config.py`中的测试用例，该文件用于测试配置管理模块（`Config`类）的功能。测试覆盖了配置初始化、验证、账号管理、IMAP配置、浏览器配置等多个方面。

## 测试环境设置

### 清理测试环境
- 使用`@pytest.fixture(autouse=True)`装饰器自动清理测试环境
- 清理测试文件（accounts.json）
- 清理所有相关的环境变量

### 基础环境设置
- `setup_base_env`函数用于设置基本环境变量
- 包含域名、临时邮箱、IMAP、浏览器等配置项

### 临时文件设置
- `temp_env_file`：创建临时的.env文件
- `temp_accounts_file`：创建临时的accounts.json文件

## 测试用例说明

### 1. 配置初始化测试
- `test_config_initialization`：验证配置初始化是否正确
- 检查域名、临时邮箱、密码等基本配置项

### 2. 配置验证测试
- `test_check_config_valid`：验证有效配置
- `test_check_config_missing_domain`：测试缺少域名配置
- `test_check_config_missing_imap`：测试缺少IMAP配置
- `test_check_config_missing_temp_mail`：测试缺少临时邮箱配置
- `test_check_config_invalid_browser_path`：测试无效的浏览器路径
- `test_check_config_invalid_proxy`：测试无效的代理格式

### 3. 账号管理测试
- `test_save_accounts`：测试保存账号信息
- `test_load_accounts`：测试加载账号信息
- `test_load_accounts_file_not_found`：测试加载不存在的账号文件
- `test_backup_config`：测试配置备份功能

### 4. IMAP配置测试
- `test_get_imap_config`：测试获取IMAP配置
- `test_get_imap_config_missing`：测试缺少IMAP配置的情况
- `test_imap_config`：验证IMAP配置的完整性

### 5. 浏览器配置测试
- `test_get_browser_config`：测试获取浏览器配置
- `test_browser_config`：验证浏览器配置的完整性

### 6. 临时邮箱配置测试
- `test_get_temp_mail_config`：测试获取临时邮箱配置
- `test_get_temp_mail_config_missing`：测试缺少临时邮箱配置的情况
- `test_temp_mail_config`：验证临时邮箱配置的完整性

### 7. 其他测试
- `test_config_validation`：测试配置验证功能
- `test_error_handling`：测试错误处理机制
- `test_config_value_types`：测试配置值类型
- `test_file_paths`：测试文件路径处理
- `test_save_load_accounts`：测试账号信息的保存和加载
- `test_invalid_proxy_format`：测试无效的代理格式
- `test_missing_required_config`：测试缺少必需配置项
- `test_empty_config_file`：测试空配置文件的情况

## 测试数据

### 环境变量配置
```env
DOMAIN=example.com
TEMP_MAIL=test
TEMP_MAIL_EPIN=123456
TEMP_MAIL_EXT=@temp.com
IMAP_SERVER=imap.example.com
IMAP_PORT=993
IMAP_USER=test@example.com
IMAP_PASS=password
IMAP_DIR=INBOX
IMAP_PROTOCOL=IMAP
BROWSER_USER_AGENT=Mozilla/5.0
BROWSER_HEADLESS=True
BROWSER_PATH=
BROWSER_PROXY=127.0.0.1:8080
```

### 账号数据
```json
[
    {
        "username": "test1",
        "password": "pass1",
        "email": "test1@example.com"
    },
    {
        "username": "test2",
        "password": "pass2",
        "email": "test2@example.com"
    }
]
```

## 测试依赖

- pytest：测试框架
- tempfile：创建临时文件
- json：处理JSON数据
- os：文件系统操作
- datetime：时间处理
- shutil：文件操作
- pathlib：路径处理

## 运行测试

```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

# 运行测试
pytest tests/test_config.py -v
```

## 注意事项

1. 测试前确保已激活虚拟环境
2. 测试会自动清理测试文件和环境变量
3. 测试使用临时文件，不会影响实际配置文件
4. 所有测试都是独立的，可以单独运行 