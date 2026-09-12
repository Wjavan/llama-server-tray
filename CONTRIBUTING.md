# 贡献指南

非常感谢你对 `llama-server-tray` 的关注！欢迎提交 Issue 和 PR。

## 如何贡献

### 报告问题

1. 访问 [Issues](https://github.com/Wjavan/llama-server-tray/issues)
2. 点击 "New Issue"
3. 使用模板：
   - **🐛 Bug 报告**：描述问题 + 环境信息 + 复现步骤
   - **✨ 新功能请求**：说明用途 + 理想用法
   - **📖 文档改进**：指出文档哪里不清楚
   - **🤔 Other**：其他想法

### 提交 Pull Request

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交修改：`git commit -m "feat: your feature description"`
4. Push 分支：`git push origin feature/your-feature`
5. 提交 PR 到 `main` 分支

#### Commit 消息规范

- `feat: ...` - 新功能
- `fix: ...` - 修复 bug
- `docs: ...` - 文档更新
- `refactor: ...` - 重构（非功能改进）
- `chore: ...` - 构建/工具链更新

## 开发环境

### 本地安装

```bash
git clone https://github.com/Wjavan/llama-server-tray.git
cd llama-server-tray

# 安装依赖
py -m pip install pystray pillow

# 运行启动器
pythonw llama_server_tray.pyw
```

### 打包测试

```bash
py -m pip install pyinstaller
pyinstaller --noconsole --onefile --name llama-server-tray llama_server_tray.pyw
```

## 开发准则

- **测试边界情况**：Windows 不同版本、不同 llama.cpp 版本
- **保持向后兼容**：不要删除现有配置项
- **更新文档**：改代码时同步更新 README
- **保持简洁**：最小改动解决问题

## 标签说明

- `good first issue` - 适合新手
- `help wanted` - 还在招帮手
- `bug` - 问题
- `enhancement` - 新功能

## 问题？

- GitHub Discussions: https://github.com/Wjavan/llama-server-tray/discussions
- 提 issue: https://github.com/Wjavan/llama-server-tray/issues
