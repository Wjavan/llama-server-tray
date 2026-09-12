# llama-server-tray

Windows 托盘静默启动器 for [llama.cpp](https://github.com/ggerganov/llama.cpp) 的 `llama-server.exe`。

## 特性

- 🔇 **全程静默**：`.pyw` + `pythonw.exe` + `CREATE_NO_WINDOW`，无任何控制台窗口
- 🔁 **自动重启**：服务异常退出自动重启，连续失败保护（默认 3 次）
- 🔒 **单实例锁**：端口锁防止重复启动
- 📝 **双日志**：托盘程序日志 + llama-server 输出日志
- 🖱️ **托盘菜单**：查看状态、打开日志、手动重启、退出
- ⚙️ **开箱即用**：放到版本目录同级，双击即跑

## 目录结构

```
llama-server-tray/
├── llama-b5560-bin-win-cuda-12.4/   # llama.cpp 发布包（自行下载解压）
│   └── llama-server.exe
├── Models/                          # 模型文件目录（自建）
│   └── your-model.gguf
├── llama_server_tray.pyw            # 本启动器（双击运行）
├── llama_tray.log                   # 托盘程序日志（自动生成）
└── llama_server.log                 # llama-server 输出日志（自动生成）
```

## 快速开始

### 1. 准备 llama-server

从 [llama.cpp Releases](https://github.com/ggerganov/llama.cpp/releases) 下载对应 CUDA 版本的 `llama-b*-bin-win-cuda-*.zip`，解压到本脚本**同级目录**（文件夹名形如 `llama-b5560-bin-win-cuda-12.4`）。

### 2. 准备模型

在脚本同级目录创建 `Models` 文件夹，放入 `.gguf` 模型文件。

### 3. 安装依赖（仅首次）

```bash
py -m pip install pystray pillow
```

### 4. 运行

**双击 `llama_server_tray.pyw`** 即可（或命令行：`pythonw llama_server_tray.pyw`）。

右下角托盘区出现青色圆环图标 → 右键可操作。

## 配置

编辑 `llama_server_tray.pyw` 顶部 **配置区**：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MODELS_DIR` | `./Models` | 模型目录路径 |
| `SERVER_PORT` | `8080` | 服务监听端口 |
| `CTX_SIZE` | `65536` | 上下文大小（`--ctx-size`） |
| `AUTO_RESTART` | `True` | 异常退出是否自动重启 |
| `MAX_FAIL_STREAK` | `3` | 连续快速失败阈值 |
| `LOCK_PORT` | `45679` | 单实例锁端口（避免冲突即可） |

## 托盘菜单

- **LLaMA 服务：运行中 (端口 8080)** — 状态显示（不可点击）
- **打开托盘日志** — 查看启动器自身日志
- **打开服务日志** — 查看 llama-server 完整输出（排错首选）
- **重启服务** — 手动重启 llama-server（重置失败计数）
- **退出** — 停止服务并退出托盘程序

## 故障排查

1. **双击没反应** → 查看 `llama_tray.log`，通常是缺 `pystray`/`pillow`
2. **启动失败** → 查看 `llama_server.log`，常见原因：
   - 未找到版本文件夹（检查文件夹命名 `llama-b*-bin-win-cuda-*`）
   - 模型目录为空或路径错误
   - 端口被占用
3. **频繁自动重启** → 连续 3 次快速失败后会停止重启并弹窗，需手动点“重启服务”或修复后重启托盘程序

## 打包为单文件 .exe（可选）

```bash
py -m pip install pyinstaller
pyinstaller --noconsole --onefile --name llama-server-tray llama_server_tray.pyw
```

生成的 `dist/llama-server-tray.exe` 可直接分发（无需安装 Python）。

## 许可证

MIT License