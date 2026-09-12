# llama-server-tray

A silent tray launcher for [llama.cpp](https://github.com/ggerganov/llama.cpp)'s `llama-server.exe` on Windows.

[![CI](https://github.com/Wjavan/llama-server-tray/workflows/Validate/badge.svg)](https://github.com/Wjavan/llama-server-tray/actions)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

⭐ If this project helps you, please give it a Star! ⭐

## ⬇️ Download

Latest version: [![Latest Release](https://img.shields.io/github/v/release/Wjavan/llama-server-tray)](https://github.com/Wjavan/llama-server-tray/releases/latest)

**Windows users can download directly**:
- [llama-server-tray.exe](https://github.com/Wjavan/llama-server-tray/releases/latest) - Pre-packaged executable
- See also [CHANGELOG](CHANGELOG.md)

## Features

- 🔇 **Silent operation** - No console window (`pythonw.exe` + `CREATE_NO_WINDOW`)
- 🔁 **Auto-restart** - Automatically restarts on failure (stops after 3 consecutive failures)
- 🔒 **Single instance** - Port-based lock prevents duplicate launches
- 📝 **Dual logging** - Tray log + llama-server output log
- 🖱️ **Tray menu** - View status, open logs, restart, exit
- ⚙️ **Ready to use** - Place in same directory and double-click to run

## Directory Structure

```
llama-server-tray/
├── llama-b5560-bin-win-cuda-12.4/   # llama.cpp release package (download & extract)
│   └── llama-server.exe
├── Models/                          # Model directory (create yourself)
│   └── your-model.gguf
├── llama_server_tray.pyw            # Launcher (double-click to run)
├── llama_tray.log                   # Tray program log (auto-generated)
└── llama_server.log                 # llama-server log (auto-generated)
```

## Quick Start

### 1. Prepare llama-server

Download the CUDA build `llama-b*-bin-win-cuda-*.zip` from [llama.cpp Releases](https://github.com/ggerganov/llama.cpp/releases) and extract it **to the same directory** as this script (folder name format: `llama-b5560-bin-win-cuda-12.4`).

### 2. Prepare models

Create a `Models` folder next to the script and place your `.gguf` model files inside.

### 3. Install dependencies (first time only)

```bash
py -m pip install pystray pillow
```

### 4. Run

**Double-click `llama_server_tray.pyw`** or run from command line: `pythonw llama_server_tray.pyw`

A cyan ring icon should appear in the system tray → right-click to access menu.

## Configuration

Edit the **Configuration Section** at the top of `llama_server_tray.pyw`:

| Variable | Default | Description |
|------|--------|------|
| `MODELS_DIR` | `./Models` | Model directory path |
| `SERVER_PORT` | `8080` | Server listening port |
| `CTX_SIZE` | `65536` | Context size (`--ctx-size`) |
| `AUTO_RESTART` | `True` | Auto-restart on failure |
| `MAX_FAIL_STREAK` | `3` | Failure threshold before stopping |
| `LOCK_PORT` | `45679` | Single-instance lock port |

## Tray Menu

- **LLaMA Server: Running (port 8080)** — Status display (not clickable)
- **Open Tray Log** — View launcher's own log
- **Open Server Log** — View full llama-server output (preferred for debugging)
- **Restart Service** — Manually restart llama-server (resets failure count)
- **Exit** — Stop server and quit tray

## Troubleshooting

1. **Nothing happens on double-click** → Check `llama_tray.log`, usually missing `pystray`/`pillow`
2. **Startup fails** → Check `llama_server.log`, common causes:
   - Version folder not found (check naming: `llama-b*-bin-win-cuda-*`)
   - Empty or wrong model directory
   - Port already in use
3. **Frequent auto-restart** → After 3 quick failures, auto-restart stops and shows a dialog. Click "Restart Service" in tray or fix and relaunch the tray program

## Build standalone .exe (optional)

```bash
py -m pip install pyinstaller
pyinstaller --noconsole --onefile --name llama-server-tray llama_server_tray.pyw
```

Generated `dist/llama-server-tray.exe` can be distributed without Python installation.

## Testing new builds (auto-released)

Pushing a tag will trigger automatic build and release: https://github.com/Wjavan/llama-server-tray/releases/latest

```bash
git tag v1.0.0
git push origin v1.0.0

# Automatically triggers build and uploads to Releases (about 3-5 minutes)
```

## Contributing

Contributions are welcome! Check out [Good First Issue](https://github.com/Wjavan/llama-server-tray/labels/good%20first%20issue) if you're new.

## License

MIT License - See [LICENSE](LICENSE) for details.
