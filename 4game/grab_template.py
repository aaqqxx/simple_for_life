#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
grab_template.py —— 在屏幕上用鼠标框选一个矩形区域，保存为特征图片（模板 PNG）。

用于生成 screen_finder.py 需要的 --template 图片。框选前请先让目标内容显示在屏幕上。

用法：
    python grab_template.py -o tpl/btn.png          # 默认截主屏
    python grab_template.py -o tpl/icon.png --monitor 2
"""

from __future__ import annotations

import argparse
import ctypes
import sys
import time
from pathlib import Path

import cv2
import numpy as np

try:
    import mss
except ImportError as exc:  # pragma: no cover
    raise SystemExit("缺少依赖 mss，请先执行：pip install -r requirements.txt") from exc


def enable_dpi_awareness() -> None:
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def imwrite_unicode(path: Path, img: np.ndarray) -> None:
    ext = path.suffix or ".png"
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise ValueError(f"无法编码图片：{path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    buf.tofile(str(path))


class Selector:
    """全屏半透明遮罩 + 鼠标拖拽框选。"""

    def __init__(self, monitor: int, padding: int = 0, alpha: float = 0.35):
        import tkinter as tk
        self.tk = tk
        self.monitor = monitor
        self.padding = padding
        self.alpha = alpha
        self.root = self.canvas = None
        self.start = None
        self.rect = None
        self.selected = None  # (x1, y1, x2, y2) 屏幕绝对坐标，含 padding

    def run(self) -> tuple[int, int, int, int]:
        with mss.mss() as sct:
            mon = dict(sct.monitors[self.monitor])

        root = self.tk.Tk()
        self.root = root
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", self.alpha)
        root.geometry(f"{mon['width']}x{mon['height']}+{mon['left']}+{mon['top']}")

        canvas = self.tk.Canvas(root, bg="black", cursor="cross", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.canvas = canvas

        info = f"显示器 {self.monitor}：按住左键拖拽框选，松开即自动保存；Esc/双击取消。"
        canvas.create_text(mon["width"] // 2, 30, text=info, fill="#00ff88",
                           font=("Consolas", 14), anchor="center")

        canvas.bind("<ButtonPress-1>", self._on_press)
        canvas.bind("<B1-Motion>", self._on_drag)
        canvas.bind("<ButtonRelease-1>", self._on_release)
        canvas.bind("<Double-Button-1>", self._on_cancel)
        root.bind("<Escape>", self._on_cancel)
        root.bind("<Return>", self._on_confirm)
        root.bind("<space>", self._on_confirm)

        root.mainloop()

        # 先隐藏遮罩再截图，避免把半透明遮罩一起截进去
        selected = self.selected
        if selected is not None:
            root.withdraw()
            root.update()
            time.sleep(0.2)
        root.destroy()
        return selected


    def _on_cancel(self, _e=None):
        self.selected = None
        if self.root is not None:
            self.root.quit()

    def _on_confirm(self, _e=None):
        if self.selected is not None and self.root is not None:
            self.root.quit()

    def _on_press(self, e):
        # 双击的第二次按下不要把已选好的框清掉
        if self.selected is not None and self.start is None:
            return
        self.start = (e.x_root, e.y_root)
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None

    def _on_drag(self, e):
        if not self.start:
            return
        x1, y1 = self.start
        x2, y2 = e.x_root, e.y_root
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline="#00ff88", width=2)

    def _on_release(self, e):
        if not self.start:
            return
        x1, y1 = self.start
        x2, y2 = e.x_root, e.y_root
        if abs(x2 - x1) < 3 or abs(y2 - y1) < 3:
            self.selected = None
            return
        self.start = None
        px = self.padding
        left, top = min(x1, x2), min(y1, y2)
        right, bottom = max(x1, x2), max(y1, y2)
        self.selected = (left - px, top - px, right + px, bottom + px)
        # 松开鼠标就自动保存，0.3 秒后退出（留时间看清选框，还能按 Esc 取消）
        self.canvas.after(300, self._on_confirm)


def main(argv=None) -> int:
    enable_dpi_awareness()
    p = argparse.ArgumentParser(description="框选屏幕区域保存为模板图片")
    p.add_argument("-o", "--output", default="template.png", help="输出图片路径（默认 template.png）")
    p.add_argument("--monitor", type=int, default=1, help="显示器编号，0=全部拼接，1=主屏…（默认 1）")
    p.add_argument("--padding", type=int, default=0, help="框选后向外扩展的像素数（默认 0）")
    p.add_argument("--alpha", type=float, default=0.35, help="遮罩不透明度，越大越暗（默认 0.35）")
    args = p.parse_args(argv)

    with mss.mss() as sct:
        if not 0 <= args.monitor < len(sct.monitors):
            print(f"--monitor 取值范围 0..{len(sct.monitors) - 1}", file=sys.stderr)
            return 1
        mon = dict(sct.monitors[args.monitor])
        if args.monitor == 0 and len(sct.monitors) > 1:
            print("注意：monitor=0 是全部显示器拼接，框选可能会跨屏。", file=sys.stderr)

    print(f"请在显示器 {args.monitor} 上按住左键拖拽框选区域...", file=sys.stderr)
    sel = Selector(args.monitor, args.padding, args.alpha).run()
    if sel is None:
        print("已取消，未保存任何图片。", file=sys.stderr)
        return 1

    left, top, right, bottom = sel
    with mss.mss() as sct:
        shot = sct.grab({"left": left, "top": top, "width": right - left, "height": bottom - top})
    image = np.ascontiguousarray(np.asarray(shot)[:, :, :3])

    out = Path(args.output)
    imwrite_unicode(out, image)
    print(f"已保存: {out}  ({image.shape[1]}x{image.shape[0]})  区域=({left},{top},{image.shape[1]}x{image.shape[0]})",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())