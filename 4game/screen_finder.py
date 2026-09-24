#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
screen_finder.py —— 根据一张特征图片，在屏幕中实时捕获它的位置坐标。

原理：屏幕截图 + OpenCV 模板匹配（matchTemplate）。
支持：多目标、多缩放、自定义搜索区域、可调捕获间隔、JSON / 自定义格式输出、
      找到后自动点击或移动鼠标、保存标注图。

常用示例：
    python screen_finder.py --template tpl/btn.png --interval 0.5
    python screen_finder.py --template tpl/btn.png --interval 1 --threshold 0.9 --json
    python screen_finder.py --config targets.json --format "{name} {cx},{cy}"
    python screen_finder.py --template tpl/btn.png --once --click
    python screen_finder.py --list-monitors
"""

from __future__ import annotations

import argparse
import ctypes
import json
import re
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

try:
    import cv2
    import numpy as np
except ImportError as exc:  # pragma: no cover
    raise SystemExit("缺少依赖，请先执行：pip install -r requirements.txt") from exc

try:
    import mss
except ImportError as exc:  # pragma: no cover
    raise SystemExit("缺少依赖 mss，请先执行：pip install mss") from exc


# --------------------------------------------------------------------------- #
# 基础工具
# --------------------------------------------------------------------------- #

def log(msg: str) -> None:
    """提示信息统一走 stderr，保证 stdout 只输出结果，方便管道/重定向。"""
    print(msg, file=sys.stderr, flush=True)


def enable_dpi_awareness() -> None:
    """Windows 下开启 DPI 感知，否则截图尺寸与鼠标坐标会被系统缩放搞乱。"""
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PER_MONITOR_DPI_AWARE
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def imread_unicode(path: Path, flags: int = cv2.IMREAD_UNCHANGED) -> np.ndarray:
    """读图，支持中文/空格路径（cv2.imread 在 Windows 上处理不了非 ASCII 路径）。"""
    buf = np.fromfile(str(path), dtype=np.uint8)
    if buf.size == 0:
        raise FileNotFoundError(f"读取不到文件或文件为空：{path}")
    img = cv2.imdecode(buf, flags)
    if img is None:
        raise ValueError(f"无法解码图片：{path}")
    return img


def imwrite_unicode(path: Path, img: np.ndarray) -> None:
    ext = path.suffix or ".png"
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise ValueError(f"无法编码图片：{path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    buf.tofile(str(path))


def parse_scales(text: Any) -> tuple[float, ...]:
    """'0.9,1.0,1.1' -> (0.9, 1.0, 1.1)"""
    if text is None:
        return (1.0,)
    if isinstance(text, (list, tuple)):
        values = [float(v) for v in text]
    else:
        values = [float(v) for v in re.split(r"[,\s]+", str(text).strip()) if v]
    values = sorted({round(v, 4) for v in values if v > 0})
    return tuple(values) or (1.0,)


def parse_region(text: Any) -> tuple[int, int, int, int] | None:
    """'x,y,w,h' -> (x, y, w, h)"""
    if text is None:
        return None
    if isinstance(text, (list, tuple)):
        if len(text) != 4:
            raise ValueError("region 需要 4 个整数：x,y,w,h")
        return tuple(int(v) for v in text)  # type: ignore[return-value]
    parts = [int(v) for v in re.split(r"[,\s]+", str(text).strip()) if v]
    if len(parts) != 4:
        raise ValueError("region 需要 4 个整数：x,y,w,h")
    return tuple(parts)  # type: ignore[return-value]


# --------------------------------------------------------------------------- #
# 数据结构
# --------------------------------------------------------------------------- #

@dataclass
class Match:
    """一个匹配结果，坐标是【屏幕绝对坐标】（虚拟桌面坐标系）。"""
    x: int          # 左上角 x
    y: int          # 左上角 y
    w: int          # 宽
    h: int          # 高
    score: float    # 相似度 0~1
    scale: float = 1.0

    @property
    def cx(self) -> int:
        return self.x + self.w // 2

    @property
    def cy(self) -> int:
        return self.y + self.h // 2

    @property
    def box(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.x + self.w, self.y + self.h)

    def as_dict(self) -> dict[str, Any]:
        return {
            "x": self.x, "y": self.y, "w": self.w, "h": self.h,
            "cx": self.cx, "cy": self.cy,
            "score": round(self.score, 4), "scale": round(self.scale, 3),
        }


@dataclass
class Target:
    """一个要找的特征（模板图片）。"""
    name: str
    image: np.ndarray                      # BGR
    mask: np.ndarray | None = None         # 来自 PNG 的 alpha 通道
    threshold: float = 0.85
    scales: tuple[float, ...] = (1.0,)
    region: tuple[int, int, int, int] | None = None   # 相对所选显示器
    max_matches: int = 1                   # <=0 表示不限制

    @classmethod
    def from_file(cls, path: str | Path, name: str | None = None, **kwargs: Any) -> "Target":
        path = Path(path)
        raw = imread_unicode(path)
        mask = None
        if raw.ndim == 2:
            image = cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR)
        elif raw.shape[2] == 4:
            image = np.ascontiguousarray(raw[:, :, :3])
            alpha = raw[:, :, 3]
            mask = alpha if int(alpha.min()) < 255 else None
        else:
            image = np.ascontiguousarray(raw[:, :, :3])
        return cls(name=name or path.stem, image=image, mask=mask, **kwargs)


# --------------------------------------------------------------------------- #
# 屏幕捕获
# --------------------------------------------------------------------------- #

class Screen:
    """基于 mss 的屏幕捕获。坐标原点为虚拟桌面左上角（多屏时可能为负）。"""

    def __init__(self, monitor: int = 1):
        self.sct = mss.mss()
        monitors = self.sct.monitors
        if not 0 <= monitor < len(monitors):
            raise SystemExit(f"--monitor 取值范围 0..{len(monitors) - 1}（0 表示所有显示器拼接）")
        self.monitor = monitor
        self.bbox = dict(monitors[monitor])

    def describe(self) -> str:
        b = self.bbox
        kind = "全部显示器拼接" if self.monitor == 0 else f"显示器 {self.monitor}"
        return (f"{kind}：left={b['left']} top={b['top']} "
                f"size={b['width']}x{b['height']}")

    def grab(self, region: Sequence[int] | None = None) -> tuple[np.ndarray, tuple[int, int]]:
        """返回 (BGR 图像, 该图像左上角在屏幕上的绝对坐标)。"""
        left, top = self.bbox["left"], self.bbox["top"]
        if region:
            rx, ry, rw, rh = (int(v) for v in region)
            box = {"left": left + rx, "top": top + ry, "width": rw, "height": rh}
            origin = (left + rx, top + ry)
        else:
            box = self.bbox
            origin = (left, top)
        shot = self.sct.grab(box)
        frame = np.asarray(shot)[:, :, :3]      # BGRA -> BGR
        return np.ascontiguousarray(frame), origin

    def close(self) -> None:
        try:
            self.sct.close()
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# 模板匹配
# --------------------------------------------------------------------------- #

def _iou(a: Sequence[int], b: Sequence[int]) -> float:
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def _dedupe(matches: list[Match], iou_thr: float) -> list[Match]:
    """非极大值抑制：同一目标在多尺度/邻近位置会被重复检出，只保留最优的。"""
    kept: list[Match] = []
    for m in sorted(matches, key=lambda m: m.score, reverse=True):
        if all(_iou(m.box, k.box) <= iou_thr for k in kept):
            kept.append(m)
    return kept


def find_matches(
    frame: np.ndarray,
    target: Target,
    *,
    origin: tuple[int, int] = (0, 0),
    gray: bool = False,
    nms_iou: float = 0.3,
    screen_scale: float = 1.0,
) -> list[Match]:
    """在 frame 中查找 target，返回按相似度降序排列的匹配列表。"""
    ox, oy = origin
    if target.region:
        rx, ry, rw, rh = target.region
        frame = frame[max(0, ry):ry + rh, max(0, rx):rw + rx]
        ox += max(0, rx)
        oy += max(0, ry)
    if frame.size == 0:
        return []

    s = screen_scale
    work = cv2.resize(frame, None, fx=s, fy=s, interpolation=cv2.INTER_AREA) if s != 1.0 else frame
    search = cv2.cvtColor(work, cv2.COLOR_BGR2GRAY) if gray else work
    sh, sw = search.shape[:2]

    found: list[Match] = []
    for scale in target.scales:
        eff = scale * s
        tpl, mask = target.image, target.mask
        if abs(eff - 1.0) > 1e-6:
            interp = cv2.INTER_AREA if eff < 1 else cv2.INTER_LINEAR
            tpl = cv2.resize(tpl, None, fx=eff, fy=eff, interpolation=interp)
            if mask is not None:
                mask = cv2.resize(mask, (tpl.shape[1], tpl.shape[0]), interpolation=cv2.INTER_NEAREST)

        th, tw = tpl.shape[:2]
        if th < 2 or tw < 2 or th > sh or tw > sw:
            continue  # 该缩放下模板比搜索区域还大，跳过

        src = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY) if gray else tpl
        # 注意：OpenCV 仅 TM_SQDIFF / TM_CCORR_NORMED 支持 mask，所以带 alpha 时换算法
        method = cv2.TM_CCORR_NORMED if mask is not None else cv2.TM_CCOEFF_NORMED
        res = cv2.matchTemplate(search, src, method, mask=mask)
        res = np.nan_to_num(res, nan=0.0, posinf=0.0, neginf=0.0)

        ys, xs = np.where(res >= target.threshold)
        for x, y in zip(xs.tolist(), ys.tolist()):
            found.append(Match(
                x=int(round(x / s)) + ox,
                y=int(round(y / s)) + oy,
                w=max(1, int(round(tw / s))),
                h=max(1, int(round(th / s))),
                score=float(res[y, x]),
                scale=scale,
            ))

    limit = target.max_matches if target.max_matches and target.max_matches > 0 else None
    return _dedupe(found, nms_iou)[:limit]


# --------------------------------------------------------------------------- #
# 标注与输出
# --------------------------------------------------------------------------- #

COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 255, 0)]


def annotate(frame: np.ndarray, results: list[tuple[Target, list[Match]]],
             origin: tuple[int, int] = (0, 0)) -> np.ndarray:
    out = frame.copy()
    ox, oy = origin
    for i, (target, matches) in enumerate(results):
        color = COLORS[i % len(COLORS)]
        for m in matches:
            x1, y1 = m.x - ox, m.y - oy
            cv2.rectangle(out, (x1, y1), (x1 + m.w, y1 + m.h), color, 2)
            cv2.circle(out, (x1 + m.w // 2, y1 + m.h // 2), 3, color, -1)
            label = f"{target.name} {m.score:.3f}"
            pos = (x1, max(14, y1 - 6))
            cv2.putText(out, label, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(out, label, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1, cv2.LINE_AA)
    return out


def render_line(fmt: str, target: Target, m: Match, index: int, stamp: str) -> str:
    fields = {
        "name": target.name, "index": index, "time": stamp, "found": 1,
        "x": m.x, "y": m.y, "w": m.w, "h": m.h,
        "cx": m.cx, "cy": m.cy,
        "score": m.score, "scale": m.scale,
    }
    try:
        return fmt.format(**fields)
    except KeyError as exc:
        raise SystemExit(f"--format 中存在未知占位符：{exc}") from None


def emit(args: argparse.Namespace, results: list[tuple[Target, list[Match]]],
         elapsed: float, stamp: str) -> None:
    found_any = any(ms for _, ms in results)

    if args.json:
        if not found_any and args.only_found:
            return
        payload = {
            "time": stamp,
            "found": found_any,
            "elapsed_ms": round(elapsed * 1000, 1),
            "targets": [
                {"name": t.name, "found": bool(ms), "matches": [m.as_dict() for m in ms]}
                for t, ms in results
            ],
        }
        print(json.dumps(payload, ensure_ascii=False), flush=True)
        return

    lines: list[str] = []
    for target, matches in results:
        for i, m in enumerate(matches):
            if args.format:
                lines.append(render_line(args.format, target, m, i, stamp))
            else:
                lines.append(
                    f"[{stamp}] {target.name}: #{i} 中心=({m.cx},{m.cy}) "
                    f"左上=({m.x},{m.y}) 尺寸={m.w}x{m.h} "
                    f"相似度={m.score:.4f} 缩放={m.scale:.2f}"
                )
    if not lines and args.verbose:
        names = ", ".join(t.name for t, _ in results)
        lines.append(f"[{stamp}] 未找到：{names} （耗时 {elapsed * 1000:.0f} ms）")

    for line in lines:
        print(line, flush=True)


# --------------------------------------------------------------------------- #
# 鼠标动作
# --------------------------------------------------------------------------- #

def move_mouse(x: int, y: int) -> None:
    if sys.platform == "win32":
        ctypes.windll.user32.SetCursorPos(int(x), int(y))
        return
    try:
        import pyautogui  # type: ignore
        pyautogui.moveTo(int(x), int(y))
    except ImportError:
        log("未安装 pyautogui，无法移动鼠标（pip install pyautogui）")


def click_mouse(button: str = "left", count: int = 1) -> None:
    if sys.platform == "win32":
        flags = {"left": (0x0002, 0x0004), "right": (0x0008, 0x0010), "middle": (0x0020, 0x0040)}
        down, up = flags.get(button, flags["left"])
        user32 = ctypes.windll.user32
        for _ in range(max(1, count)):
            user32.mouse_event(down, 0, 0, 0, 0)
            time.sleep(0.02)
            user32.mouse_event(up, 0, 0, 0, 0)
            time.sleep(0.05)
        return
    try:
        import pyautogui  # type: ignore
        pyautogui.click(button=button, clicks=max(1, count))
    except ImportError:
        log("未安装 pyautogui，无法点击（pip install pyautogui）")


def perform_actions(args: argparse.Namespace, results: list[tuple[Target, list[Match]]]) -> None:
    """默认只对相似度最高的第一个匹配执行动作。"""
    hit = next(((t, ms[0]) for t, ms in results if ms), None)
    if hit is None:
        return
    target, m = hit
    if args.click_delay > 0:
        time.sleep(args.click_delay)
    if args.move or args.click:
        move_mouse(m.cx, m.cy)
        log(f"-> 鼠标移动到 ({m.cx},{m.cy}) [{target.name}]")
    if args.click:
        click_mouse(args.click_button, args.click_count)


# --------------------------------------------------------------------------- #
# 参数与配置
# --------------------------------------------------------------------------- #

def load_config(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    text = Path(path).read_text(encoding="utf-8")
    cfg = json.loads(text)
    if not isinstance(cfg, dict):
        raise SystemExit("配置文件根节点必须是 JSON 对象")
    return cfg


def build_targets(args: argparse.Namespace, cfg: dict[str, Any]) -> list[Target]:
    targets: list[Target] = []

    for entry in cfg.get("targets", []) or []:
        if "template" not in entry:
            raise SystemExit('配置文件中的每个 target 必须有 "template" 字段')
        targets.append(Target.from_file(
            entry["template"],
            name=entry.get("name"),
            threshold=float(entry.get("threshold", args.threshold)),
            scales=parse_scales(entry.get("scales")) if entry.get("scales") else args.scales,
            region=parse_region(entry.get("region")),
            max_matches=int(entry.get("max_matches", args.max_matches)),
        ))

    for path in args.template or []:
        targets.append(Target.from_file(
            path,
            threshold=args.threshold,
            scales=args.scales,
            region=args.region,
            max_matches=args.max_matches,
        ))

    if not targets:
        raise SystemExit("请用 --template 指定特征图片，或用 --config 指定配置文件")

    for t in targets:
        if t.image.shape[0] < 3 or t.image.shape[1] < 3:
            raise SystemExit(f"模板太小（{t.name}），至少需要 3x3 像素")
        log(f"载入模板 [{t.name}] {t.image.shape[1]}x{t.image.shape[0]} "
            f"阈值={t.threshold} 缩放={list(t.scales)} 上限={t.max_matches}")
    return targets


def resolve(args: argparse.Namespace, cfg: dict[str, Any]) -> None:
    """命令行优先，未给出的项用配置文件/默认值补齐。"""
    if args.interval is None:
        args.interval = float(cfg.get("interval", 0.5))
    if args.threshold is None:
        args.threshold = float(cfg.get("threshold", 0.85))
    if args.monitor is None:
        args.monitor = int(cfg.get("monitor", 1))
    if args.region is None and cfg.get("region"):
        args.region = parse_region(cfg["region"])
    if args.scales is None:
        args.scales = parse_scales(cfg.get("scales", "1.0"))
    if args.gray is None:
        args.gray = bool(cfg.get("gray", False))
    if args.screen_scale is None:
        args.screen_scale = float(cfg.get("screen_scale", 1.0))

    if args.interval < 0:
        raise SystemExit("--interval 不能为负数")
    if not 0.0 < args.threshold <= 1.0:
        raise SystemExit("--threshold 需在 (0, 1] 之间")
    if not 0.0 < args.screen_scale <= 1.0:
        raise SystemExit("--screen-scale 需在 (0, 1] 之间")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="screen_finder.py",
        description="根据特征图片在屏幕中定位坐标（模板匹配），捕获间隔可调。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python screen_finder.py --template tpl/btn.png --interval 0.5\n"
            "  python screen_finder.py --template tpl/btn.png --interval 1 --json --only-found\n"
            "  python screen_finder.py --config targets.json --format \"{name} {cx},{cy} {score:.3f}\"\n"
            "  python screen_finder.py --template tpl/btn.png --once --click\n"
        ),
    )

    g = p.add_argument_group("特征与搜索")
    g.add_argument("-t", "--template", action="append", metavar="IMG",
                   help="特征图片路径，可重复指定以同时搜索多个特征")
    g.add_argument("-c", "--config", metavar="JSON", help="配置文件（见 targets.example.json）")
    g.add_argument("--threshold", type=float, default=None,
                   help="相似度阈值 0~1，越大越严格（默认 0.85）")
    g.add_argument("--scales", default=None,
                   help="多尺度匹配，逗号分隔，例如 0.9,1.0,1.1（默认 1.0）")
    g.add_argument("--region", default=None, metavar="x,y,w,h",
                   help="只在该区域内搜索（相对所选显示器）")
    g.add_argument("--max-matches", type=int, default=1,
                   help="每个特征最多输出几个匹配，<=0 表示不限（默认 1）")
    g.add_argument("--nms-iou", type=float, default=0.3,
                   help="去重阈值，重叠比例超过该值的框会被合并（默认 0.3）")
    g.add_argument("--gray", action="store_true", default=None,
                   help="转灰度匹配，速度更快但更容易误判")

    g = p.add_argument_group("速度")
    g.add_argument("--monitor", type=int, default=None,
                   help="显示器编号，0=全部拼接，1=主屏，2=副屏…（默认 1）")
    g.add_argument("--screen-scale", type=float, default=None,
                   help="截图缩放系数 (0,1]，缩小可大幅提速（默认 1.0）")
    g.add_argument("--list-monitors", action="store_true", help="列出所有显示器后退出")

    g = p.add_argument_group("循环控制")
    g.add_argument("-i", "--interval", type=float, default=None,
                   help="捕获间隔秒数，按「开始到开始」计时（默认 0.5）")
    g.add_argument("--once", action="store_true", help="只捕获一次就退出")
    g.add_argument("--max-runs", type=int, default=0, help="最多捕获多少次后退出，0 表示不限")
    g.add_argument("--exit-on-found", action="store_true", help="一旦找到就退出（退出码 0）")
    g.add_argument("--exit-code-on-miss", action="store_true",
                   help="配合 --once 使用：没找到时退出码为 1")

    g = p.add_argument_group("输出")
    g.add_argument("--json", action="store_true", help="每轮输出一行 JSON")
    g.add_argument("--format", metavar="TPL",
                   help="自定义输出模板，占位符：{name} {index} {x} {y} {w} {h} {cx} {cy} {score} {scale} {time}")
    g.add_argument("--only-found", action="store_true", help="只在找到时输出（JSON 模式下同样生效）")
    g.add_argument("-v", "--verbose", action="store_true", help="未找到时也输出提示")
    g.add_argument("--save-dir", metavar="DIR", help="保存带标注的截图到该目录")
    g.add_argument("--show", action="store_true", help="实时预览标注结果（按 q 退出）")

    g = p.add_argument_group("动作（可选）")
    g.add_argument("--move", action="store_true", help="找到后把鼠标移到中心")
    g.add_argument("--click", action="store_true", help="找到后点击中心（隐含 --move）")
    g.add_argument("--click-button", choices=["left", "right", "middle"], default="left")
    g.add_argument("--click-count", type=int, default=1)
    g.add_argument("--click-delay", type=float, default=0.0, help="动作前额外等待秒数")

    g = p.add_argument_group("其他")
    g.add_argument("--stop-key", metavar="KEY",
                   help="按该键停止，例如 esc（需 pip install keyboard）")
    return p


def list_monitors() -> int:
    with mss.mss() as sct:
        for i, m in enumerate(sct.monitors):
            kind = "全部显示器拼接" if i == 0 else f"显示器 {i}"
            print(f"[{i}] {kind}: left={m['left']} top={m['top']} "
                  f"width={m['width']} height={m['height']}")
    return 0


# --------------------------------------------------------------------------- #
# 主循环
# --------------------------------------------------------------------------- #

def install_stop_key(key: str | None, event: threading.Event) -> None:
    if not key:
        return
    try:
        import keyboard  # type: ignore
    except ImportError:
        log("未安装 keyboard 模块，--stop-key 无效（pip install keyboard）")
        return
    try:
        keyboard.add_hotkey(key, event.set)
        log(f"按 {key} 可停止")
    except Exception as exc:
        log(f"注册停止键失败：{exc}")


def run(args: argparse.Namespace) -> int:
    targets = build_targets(args, load_config(args.config))
    screen = Screen(args.monitor)
    log(f"捕获区域：{screen.describe()}")
    log(f"间隔={args.interval}s 阈值={args.threshold} 灰度={bool(args.gray)} "
        f"截图缩放={args.screen_scale}")

    stop = threading.Event()
    install_stop_key(args.stop_key, stop)

    runs = 0
    hits = 0
    next_at = time.perf_counter()
    preview = "screen_finder" if args.show else None

    try:
        while True:
            t0 = time.perf_counter()
            frame, origin = screen.grab(args.region)

            results: list[tuple[Target, list[Match]]] = []
            for target in targets:
                matches = find_matches(
                    frame, target,
                    origin=origin,
                    gray=bool(args.gray),
                    nms_iou=args.nms_iou,
                    screen_scale=args.screen_scale,
                )
                results.append((target, matches))

            elapsed = time.perf_counter() - t0
            runs += 1
            stamp = time.strftime("%H:%M:%S")
            found_any = any(ms for _, ms in results)
            if found_any:
                hits += 1

            emit(args, results, elapsed, stamp)

            if found_any:
                if args.save_dir or args.show:
                    canvas = annotate(frame, results, origin)
                    if args.save_dir:
                        name = results[0][0].name if len(results) == 1 else "multi"
                        out = Path(args.save_dir) / f"{name}_{time.strftime('%H%M%S')}_{runs:05d}.png"
                        imwrite_unicode(out, canvas)
                        log(f"已保存标注图：{out}")
                    if args.show:
                        cv2.imshow(preview, canvas)
                perform_actions(args, results)

            if args.show and cv2.waitKey(1) & 0xFF == ord("q"):
                break
            if args.once or (args.exit_on_found and found_any):
                break
            if args.max_runs and runs >= args.max_runs:
                break
            if stop.is_set():
                log("收到停止信号")
                break

            # 按「开始到开始」计时，保证间隔稳定；单轮耗时超过间隔时立即进入下一轮
            next_at += args.interval
            delay = next_at - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            else:
                next_at = time.perf_counter()

    except KeyboardInterrupt:
        log("已中断")
    finally:
        screen.close()
        if args.show:
            cv2.destroyAllWindows()

    log(f"结束：共捕获 {runs} 次，命中 {hits} 次")
    if args.exit_code_on_miss and hits == 0:
        return 1
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    enable_dpi_awareness()
    args = build_parser().parse_args(argv)
    if args.list_monitors:
        return list_monitors()

    cfg = load_config(args.config)
    resolve(args, cfg)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
