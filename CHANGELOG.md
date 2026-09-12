# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0] - 2026-09-12

### Added
- 首次发布
- 静默托盘启动器，全程无控制台窗口
- 自动重启机制（连续失败保护）
- 单实例锁防止重复启动
- 双日志系统（托盘日志 + 服务日志）
- 托盘菜单（查看状态、打开日志、重启、退出）
- PyInstaller 打包支持
- SHA256 校验文件生成
- GitHub Actions CI/CD 自动构建
- MIT License 开源协议

### Changed
- 无

### Deprecated
- 无

### Removed
- 无

### Fixed
- Linux CI 下 .pyw 导入测试问题（改用 py_compile 语法检查）

### Security
- 无

---

## [Unreleased]
### Planned
- 支持命令行参数配置（环境变量优先）
- 支持自定义托盘图标
- 支持多模型切换
- 添加健康检查端点
- 增加更多错误提示和日志级别选项