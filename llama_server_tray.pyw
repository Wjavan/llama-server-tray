# -*- coding: utf-8 -*-
"""
llama-server-tray.pyw — 静默托盘启动 llama-server（Windows）

放到 llama-b*-bin-win-cuda-* 版本文件夹同级目录，双击运行；
模型默认放同目录 Models 文件夹。依赖：py -m pip install pystray pillow
"""

import os
import sys
import time
import socket
import logging
import subprocess
import threading

# ==================== 配置区（按需修改） ====================
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR      = os.path.join(BASE_DIR, "Models")
SERVER_PORT     = 8080
CTX_SIZE        = 65536
AUTO_RESTART    = True          # 服务异常退出后自动重启
MAX_FAIL_STREAK = 3             # 连续失败超过该次数则停止自动重启
LOG_FILE        = os.path.join(BASE_DIR, "llama_tray.log")
SERVER_LOG_FILE = os.path.join(BASE_DIR, "llama_server.log")
LOCK_PORT       = 45679         # 单实例锁端口
# ============================================================

_LOG_FMT = "%(asctime)s %(levelname)s %(message)s"
try:
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=_LOG_FMT, encoding="utf-8")
except TypeError:
    # Python 3.9 以下不支持 encoding 参数
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=_LOG_FMT)


def _msgbox(text, title="LLaMA 托盘启动器"):
    # pythonw 没有控制台，弹窗是唯一的用户可见提示
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, text, title, 0x10)
    except Exception:
        pass


# 依赖缺失时直接弹窗提示，避免双击后毫无反应
try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError as e:
    _msgbox("缺少运行依赖 pystray / pillow，请先执行：\n"
            "py -m pip install pystray pillow\n\n%s" % e)
    sys.exit(1)

# gen 记录启动代数，用于区分旧进程与新进程，避免监控线程误判
server_info = {"proc": None, "gen": 0, "start": 0.0}
server_info_lock = threading.Lock()
fail_streak = {"n": 0}
stopping = False


def find_version_dir():
    # 匹配 llama-b*-bin-win-cuda-*，多个时取第一个
    try:
        names = os.listdir(BASE_DIR)
    except OSError:
        return None
    for name in names:
        full = os.path.join(BASE_DIR, name)
        if os.path.isdir(full) and name.startswith("llama-b") and "-bin-win-cuda-" in name:
            return full
    return None


def start_server():
    verdir = find_version_dir()
    if not verdir:
        logging.error("未找到版本文件夹 llama-b*-bin-win-cuda-*（当前目录：%s）", BASE_DIR)
        return False
    exe = os.path.join(verdir, "llama-server.exe")
    if not os.path.exists(exe):
        logging.error("未找到 %s", exe)
        return False

    cmd = [exe, "--port", str(SERVER_PORT), "--models-dir", MODELS_DIR, "--ctx-size", str(CTX_SIZE)]
    try:
        logf = open(SERVER_LOG_FILE, "a", encoding="utf-8", errors="replace")
    except OSError:
        logging.exception("无法打开服务日志文件 %s", SERVER_LOG_FILE)
        return False
    try:
        # CREATE_NO_WINDOW(0x08000000)：服务进程不弹控制台窗口
        proc = subprocess.Popen(
            cmd,
            cwd=verdir,
            stdout=logf,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            creationflags=0x08000000 | 0x00000200,
        )
        with server_info_lock:
            server_info["gen"] += 1
            server_info["proc"] = proc
            server_info["start"] = time.time()
        logging.info("llama-server 已启动 (PID=%s, 端口=%s)，输出见 %s",
                     proc.pid, SERVER_PORT, SERVER_LOG_FILE)
        return True
    except Exception:
        logging.exception("启动 llama-server 失败")
        logf.close()
        return False


def stop_server():
    with server_info_lock:
        proc = server_info["proc"]
        server_info["proc"] = None
    if proc is None:
        return
    if proc.poll() is None:
        logging.info("正在停止 llama-server (PID=%s)...", proc.pid)
        try:
            proc.terminate()  # Windows 下即强杀
            try:
                proc.wait(timeout=8)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
        except Exception:
            logging.exception("停止 llama-server 出错")


def monitor_loop():
    global stopping
    while True:
        time.sleep(5)
        if stopping:
            return
        with server_info_lock:
            proc = server_info["proc"]
            gen = server_info["gen"]
            started = server_info["start"]
        if proc is None or proc.poll() is None:
            continue
        # 已被“重启服务”流程替换掉的旧进程直接忽略
        with server_info_lock:
            if gen != server_info["gen"] or server_info["proc"] is not proc:
                continue
        code = proc.returncode
        if code == 0 or not AUTO_RESTART:
            logging.warning("llama-server 已退出（退出码=%s），不自动重启", code)
            continue
        # 稳定运行超过 60 秒再挂，重置失败计数
        if time.time() - started > 60:
            fail_streak["n"] = 0
        fail_streak["n"] += 1
        if fail_streak["n"] >= MAX_FAIL_STREAK:
            logging.error("llama-server 连续 %s 次异常退出，已停止自动重启；请检查 %s 或点击托盘【重启服务】",
                          MAX_FAIL_STREAK, SERVER_LOG_FILE)
            _msgbox("llama-server 连续启动失败，已停止自动重启。\n请查看：%s" % SERVER_LOG_FILE)
            fail_streak["n"] = 0
            continue
        logging.warning("llama-server 异常退出（退出码=%s），5 秒后自动重启（第 %s 次）", code, fail_streak["n"])
        time.sleep(5)
        with server_info_lock:
            if stopping or gen != server_info["gen"] or server_info["proc"] is not proc:
                continue
        start_server()


def make_icon_image():
    img = Image.new("RGB", (64, 64), "black")
    d = ImageDraw.Draw(img)
    d.ellipse((10, 10, 54, 54), fill=(0, 200, 200))
    d.ellipse((20, 20, 44, 44), fill="black")
    return img


def on_open_log(icon, item):
    try:
        os.startfile(LOG_FILE)
    except Exception:
        logging.exception("打开托盘日志失败")


def on_open_server_log(icon, item):
    try:
        os.startfile(SERVER_LOG_FILE)
    except Exception:
        logging.exception("打开服务日志失败")


def on_restart(icon, item):
    logging.info("用户触发【重启服务】")
    fail_streak["n"] = 0
    stop_server()
    time.sleep(1)
    if not start_server():
        _msgbox("llama-server 重启失败，请查看日志：%s" % LOG_FILE)


def on_quit(icon, item):
    global stopping
    logging.info("用户点击【退出】，正在结束服务...")
    stopping = True
    stop_server()
    icon.stop()
    os._exit(0)  # 强制结束后台线程


def acquire_single_instance():
    # 端口被占用说明已有实例在跑
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", LOCK_PORT))
        s.listen(1)
        return s
    except OSError:
        return None


def main():
    lock = acquire_single_instance()
    if lock is None:
        logging.warning("检测到已有实例在运行（LOCK_PORT=%s 已被占用），本次启动直接退出；若确认没有其他实例，请修改 LOCK_PORT 避免与其它程序冲突", LOCK_PORT)
        return
    logging.info("========== LLaMA 托盘启动器启动 ==========")
    if not start_server():
        _msgbox("llama-server 启动失败！\n请查看日志：%s" % LOG_FILE)

    menu = pystray.Menu(
        pystray.MenuItem("LLaMA 服务：运行中 (端口 %d)" % SERVER_PORT, None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("打开托盘日志", on_open_log),
        pystray.MenuItem("打开服务日志", on_open_server_log),
        pystray.MenuItem("重启服务", on_restart),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("退出", on_quit),
    )
    icon = pystray.Icon("llama_tray", make_icon_image(),
                        "LLaMA Server (端口 %d)" % SERVER_PORT, menu)

    threading.Thread(target=monitor_loop, daemon=True).start()
    icon.run()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("启动器发生未捕获异常")
        _msgbox("启动器异常：%r\n详见日志：%s" % (sys.exc_info()[1], LOG_FILE))