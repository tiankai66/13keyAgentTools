#!/usr/bin/env python3
"""Render a beginner-friendly frame sequence for the Rev 0.9.4 assembly video."""

from __future__ import annotations

import argparse
import math
import shutil
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1280
HEIGHT = 720
FPS = 24
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"

BG = (9, 17, 31)
PANEL = (22, 35, 56)
PANEL_EDGE = (74, 222, 204)
BOX = (49, 42, 82)
BOX_EDGE = (167, 139, 250)
BOARD = (33, 44, 58)
CYAN = (48, 210, 226)
ORANGE = (249, 115, 22)
YELLOW = (251, 191, 36)
BLUE = (59, 130, 246)
RED = (248, 113, 113)
GREEN = (52, 211, 153)
TEXT = (239, 246, 255)
MUTED = (167, 186, 211)


@lru_cache(maxsize=None)
def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size=size, index=0)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def txt(draw: ImageDraw.ImageDraw, xy: tuple[float, float], value: str, size: int, fill=TEXT, anchor=None) -> None:
    draw.text(xy, value, font=font(size), fill=fill, anchor=anchor)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], fill=CYAN, width=6) -> None:
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    head = 18
    points = [
        end,
        (end[0] - head * math.cos(angle - 0.45), end[1] - head * math.sin(angle - 0.45)),
        (end[0] - head * math.cos(angle + 0.45), end[1] - head * math.sin(angle + 0.45)),
    ]
    draw.polygon(points, fill=fill)


def frame_base(draw: ImageDraw.ImageDraw, step: int, title: str, detail: str) -> None:
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=BG)
    draw.rectangle((0, 0, WIDTH, 82), fill=(13, 27, 47))
    txt(draw, (46, 24), "13keyAgentTools  装配教学", 30)
    txt(draw, (WIDTH - 46, 27), f"步骤 {step}/5", 25, fill=CYAN, anchor="ra")
    txt(draw, (46, 102), title, 34)
    txt(draw, (46, 145), detail, 21, fill=MUTED)
    draw.line((46, HEIGHT - 73, WIDTH - 46, HEIGHT - 73), fill=(39, 61, 88), width=2)
    labels = ["焊接面板", "卡入主板", "对齐 Type-C", "装透明窗", "合盖测试"]
    for i, label in enumerate(labels, start=1):
        x = 85 + (i - 1) * 278
        color = CYAN if i <= step else (87, 105, 132)
        draw.ellipse((x - 13, HEIGHT - 47, x + 13, HEIGHT - 21), fill=color)
        txt(draw, (x, HEIGHT - 10), label, 17, fill=color, anchor="ms")


def draw_top_plate(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0, closed: bool = False) -> None:
    w, h = int(560 * scale), int(400 * scale)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=int(22 * scale), fill=PANEL, outline=PANEL_EDGE, width=max(2, int(4 * scale)))
    key_size = int(52 * scale)
    gap = int(18 * scale)
    ox, oy = x + int(40 * scale), y + int(55 * scale)
    positions = [(0, 0)] + [(c, r) for r in range(1, 4) for c in range(4)]
    names = ["A"] + list("BCDEFGHIJKLM")
    for (col, row), name in zip(positions, names):
        kx = ox + col * (key_size + gap)
        ky = oy + row * (key_size + gap)
        fill = (35, 48, 68) if not closed else (26, 38, 57)
        draw.rounded_rectangle((kx, ky, kx + key_size, ky + key_size), radius=int(7 * scale), fill=fill, outline=(116, 139, 169), width=2)
        txt(draw, (kx + key_size / 2, ky + key_size / 2), name, max(12, int(17 * scale)), anchor="mm")
    led_x = x + int(345 * scale)
    led_y = y + int(63 * scale)
    for row in range(2):
        for i in range(6):
            lx = led_x + int(i * 30 * scale)
            ly = led_y + int(row * 24 * scale)
            draw.rounded_rectangle((lx, ly, lx + int(22 * scale), ly + int(14 * scale)), radius=3, fill=CYAN, outline=(93, 231, 243), width=1)
    draw.rounded_rectangle((x + int(367 * scale), y + int(186 * scale), x + int(500 * scale), y + int(358 * scale)), radius=10, fill=(29, 52, 79), outline=BLUE, width=max(2, int(3 * scale)))
    txt(draw, (x + int(433 * scale), y + int(270 * scale)), "透明\n窗", max(14, int(20 * scale)), fill=(147, 197, 253), anchor="mm")
    draw.ellipse((x + int(302 * scale), y + int(342 * scale), x + int(342 * scale), y + int(382 * scale)), fill=ORANGE, outline=(255, 180, 90), width=2)
    if closed:
        draw.rectangle((x + int(4 * scale), y + int(4 * scale), x + w - int(4 * scale), y + h - int(4 * scale)), outline=(255, 255, 255), width=2)


def draw_closed_box(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0, board: bool = True, lens: bool = False) -> None:
    w, h = int(560 * scale), int(400 * scale)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=int(22 * scale), fill=BOX, outline=BOX_EDGE, width=max(2, int(4 * scale)))
    inner = (x + int(28 * scale), y + int(28 * scale), x + w - int(28 * scale), y + h - int(28 * scale))
    draw.rounded_rectangle(inner, radius=int(13 * scale), fill=(28, 25, 48), outline=(129, 108, 202), width=max(2, int(3 * scale)))
    pad_x = x + int(254 * scale)
    pad_y = y + int(101 * scale)
    pad_w = int(180 * scale)
    pad_h = int(235 * scale)
    draw.rounded_rectangle((pad_x - int(17 * scale), pad_y - int(12 * scale), pad_x + pad_w + int(17 * scale), pad_y + pad_h + int(12 * scale)), radius=8, fill=(87, 72, 137), outline=YELLOW, width=max(2, int(4 * scale)))
    if board:
        draw.rounded_rectangle((pad_x, pad_y, pad_x + pad_w, pad_y + pad_h), radius=7, fill=BOARD, outline=(151, 171, 195), width=2)
        txt(draw, (pad_x + pad_w / 2, pad_y + 72 * scale), "Arduino Micro", max(14, int(21 * scale)), anchor="mm")
        txt(draw, (pad_x + pad_w / 2, pad_y + 106 * scale), "35×18×10 mm", max(13, int(17 * scale)), fill=CYAN, anchor="mm")
        draw.rectangle((pad_x + int(68 * scale), y + int(22 * scale), pad_x + int(112 * scale), y + int(57 * scale)), fill=(8, 13, 23), outline=RED, width=3)
    if lens:
        draw.rounded_rectangle((x + int(368 * scale), y + int(184 * scale), x + int(502 * scale), y + int(355 * scale)), radius=9, fill=(81, 152, 211), outline=(186, 230, 253), width=3)
        txt(draw, (x + int(435 * scale), y + int(270 * scale)), "透明窗片", max(13, int(18 * scale)), fill=TEXT, anchor="mm")
    draw.line((x + int(30 * scale), y + h - int(18 * scale), x + int(530 * scale), y + h - int(18 * scale)), fill=(138, 151, 178), width=max(3, int(8 * scale)))


def draw_solder_scene(draw: ImageDraw.ImageDraw, p: float) -> None:
    draw_top_plate(draw, 75, 184, 0.86)
    # simplified backside wires
    for yy in [245, 325, 405, 485]:
        draw.line((105, yy, 395, yy), fill=ORANGE, width=7)
    for xx in [145, 222, 299, 376]:
        draw.line((xx, 230, xx, 540), fill=BLUE, width=6)
    # diode markers around every switch
    for i in range(13):
        col, row = (0, 0) if i == 0 else ((i - 1) % 4, 1 + (i - 1) // 4)
        xx = 110 + col * 60
        yy = 226 + row * 69
        draw.rectangle((xx - 15, yy - 5, xx + 15, yy + 5), fill=YELLOW, outline=(255, 230, 120), width=2)
        draw.line((xx - 5, yy - 9, xx - 5, yy + 9), fill=(81, 51, 8), width=3)
    draw.rounded_rectangle((690, 196, 1170, 405), radius=18, fill=(18, 31, 51), outline=CYAN, width=3)
    txt(draw, (725, 228), "这一面完成焊接", 27, fill=CYAN)
    txt(draw, (725, 280), "① 每个按键串 1 只 1N4148", 22)
    txt(draw, (725, 320), "② 黑环端统一接橙色行线", 22, fill=ORANGE)
    txt(draw, (725, 360), "③ 同列按键接蓝色列线", 22, fill=BLUE)
    txt(draw, (725, 430), "先用万用表检查，再接 USB-C", 22, fill=GREEN)
    arrow(draw, (620, 310), (680, 310), fill=YELLOW)


def draw_insert_scene(draw: ImageDraw.ImageDraw, p: float) -> None:
    draw_closed_box(draw, 85, 184, 0.9, board=False)
    target_x, target_y = 85 + 254 * 0.9, 184 + 101 * 0.9
    # Keep the moving board below the explanatory line at the top of the frame.
    start_y = target_y - 120
    board_y = start_y + (target_y - start_y) * ease(p)
    draw.rounded_rectangle((target_x, board_y, target_x + 162, board_y + 212), radius=7, fill=BOARD, outline=CYAN, width=3)
    txt(draw, (target_x + 81, board_y + 70), "Arduino Micro", 20, anchor="mm")
    txt(draw, (target_x + 81, board_y + 105), "35×18×10", 17, fill=CYAN, anchor="mm")
    draw.rectangle((target_x + 61, board_y + 190, target_x + 101, board_y + 218), fill=(8, 13, 23), outline=RED, width=3)
    arrow(draw, (target_x + 81, start_y - 20), (target_x + 81, target_y - 10), fill=YELLOW)
    txt(draw, (735, 212), "把主板平放压入卡槽", 27, fill=YELLOW)
    txt(draw, (735, 255), "左右导轨各留 0.6 mm", 22)
    txt(draw, (735, 295), "后端贴住后挡块", 22)
    txt(draw, (735, 335), "不要用胶水固定主板", 22, fill=RED)
    txt(draw, (735, 420), "主板顶部与上盖保留间隙", 21, fill=MUTED)


def draw_typec_scene(draw: ImageDraw.ImageDraw, p: float) -> None:
    # Front-wall close-up with a sliding plug.
    draw.rounded_rectangle((100, 205, 1130, 485), radius=18, fill=BOX, outline=BOX_EDGE, width=4)
    draw.rectangle((100, 205, 1130, 260), fill=(67, 57, 108), outline=BOX_EDGE, width=3)
    draw.rectangle((535, 338, 695, 442), fill=(18, 27, 41), outline=(151, 171, 195), width=3)
    draw.rectangle((600, 360, 630, 420), fill=(8, 13, 23), outline=RED, width=3)
    plug_x = 180 + 350 * ease(p)
    draw.rounded_rectangle((plug_x, 365, plug_x + 180, 417), radius=12, fill=(112, 128, 150), outline=TEXT, width=3)
    draw.rectangle((plug_x + 160, 378, plug_x + 205, 405), fill=(206, 218, 232), outline=TEXT, width=2)
    arrow(draw, (plug_x - 85, 391), (plug_x - 15, 391), fill=RED, width=5)
    txt(draw, (730, 300), "Type-C 从前墙直进", 28, fill=RED)
    txt(draw, (730, 345), "开口 14×9 mm", 22)
    txt(draw, (730, 385), "插拔力由盒体承受", 22, fill=GREEN)
    txt(draw, (730, 425), "不要让插头撬动主板焊盘", 22, fill=YELLOW)


def draw_lens_scene(draw: ImageDraw.ImageDraw, p: float) -> None:
    draw_closed_box(draw, 65, 192, 0.86, board=True)
    # lid hovering then moving down
    lid_y = 30 + 132 * (1.0 - ease(p))
    draw_top_plate(draw, 665, int(lid_y), 0.82, closed=True)
    lens_y = int(448 - 110 * ease(p))
    draw.rounded_rectangle((665 + 0.82 * 367, lens_y, 665 + 0.82 * 500, lens_y + 0.82 * 172), radius=8, fill=(81, 152, 211), outline=(186, 230, 253), width=3)
    txt(draw, (735, 205), "透明窗片从下方装入", 27, fill=CYAN)
    txt(draw, (735, 245), "25.4×51.4×1.5 mm", 21)
    txt(draw, (735, 285), "覆盖 24×50 mm 主板窗口", 21)
    arrow(draw, (640, 420), (705, 420), fill=CYAN)


def draw_close_scene(draw: ImageDraw.ImageDraw, p: float) -> None:
    draw_closed_box(draw, 165, 168, 0.98, board=False)
    lid_y = 90 + int(88 * (1.0 - ease(p)))
    draw_top_plate(draw, 165, lid_y, 0.98, closed=True)
    for cx, cy in [(186, 187), (682, 187), (186, 544), (682, 544)]:
        draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=(224, 231, 239), outline=CYAN, width=3)
        draw.line((cx - 7, cy - 7, cx + 7, cy + 7), fill=(66, 82, 103), width=2)
    draw.rounded_rectangle((852, 332, 1075, 395), radius=14, fill=(112, 128, 150), outline=TEXT, width=3)
    draw.rectangle((1040, 348, 1095, 379), fill=(206, 218, 232), outline=TEXT, width=2)
    txt(draw, (850, 210), "合盖后就是完整盒子", 30, fill=GREEN)
    txt(draw, (850, 255), "4 个 M3×16 mm 螺丝", 23)
    txt(draw, (850, 300), "最后插 USB-C 测试", 23, fill=CYAN)
    txt(draw, (850, 470), "完成：按键 / 旋钮 / RGB / USB-C", 21, fill=MUTED)


def render_scene(image: Image.Image, scene: int, progress: float) -> None:
    draw = ImageDraw.Draw(image)
    if scene == 0:
        frame_base(draw, 1, "先认识 5 个打印件", "公差件、上盖、封闭盒底、透明窗、灯珠承载条；不要先合盖。")
        draw_top_plate(draw, 70, 188, 0.82)
        draw_closed_box(draw, 700, 210, 0.78, board=True)
        txt(draw, (250, 610), "plate.stl  上层控制盖", 22, fill=CYAN, anchor="mm")
        txt(draw, (930, 610), "bottom.stl  封闭盒底 + 主控卡槽", 22, fill=BOX_EDGE, anchor="mm")
        txt(draw, (630, 420), "→", 60, fill=YELLOW, anchor="mm")
        txt(draw, (640, 530), "window_lens.stl 装在透明窗下方", 22, fill=(186, 230, 253), anchor="mm")
    elif scene == 1:
        frame_base(draw, 1, "第 1 步：翻转上盖，焊好面板", "每个按键串 1 只二极管；二极管黑环统一朝橙色行线。")
        draw_solder_scene(draw, progress)
    elif scene == 2:
        frame_base(draw, 2, "第 2 步：把主板卡入下层盒体", "主板平放，35×18×10 mm；左右导轨留 0.6 mm 间隙。")
        draw_insert_scene(draw, progress)
    elif scene == 3:
        frame_base(draw, 3, "第 3 步：确认 Type-C 对准前墙", "USB-C 插口在下层盒体前墙，插拔力由盒体承受。")
        draw_typec_scene(draw, progress)
    elif scene == 4:
        frame_base(draw, 4, "第 4 步：从下方安装透明窗片", "透明窗片覆盖主板窗口；这是封闭主板的必要步骤。")
        draw_lens_scene(draw, progress)
    else:
        frame_base(draw, 5, "第 5 步：合盖、锁螺丝、最后通电", "四个 M3×16 mm 螺丝均匀锁紧；先开盖测试，再插 USB-C。")
        draw_close_scene(draw, progress)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames-dir", type=Path, default=Path("/tmp/agent-assembly-frames"))
    parser.add_argument("--fps", type=int, default=FPS)
    args = parser.parse_args()
    if args.frames_dir.exists():
        shutil.rmtree(args.frames_dir)
    args.frames_dir.mkdir(parents=True)

    durations = [2.4, 4.0, 3.6, 3.0, 3.2, 3.0]
    frame_index = 0
    for scene, duration in enumerate(durations):
        total = max(1, round(duration * args.fps))
        for i in range(total):
            image = Image.new("RGB", (WIDTH, HEIGHT), BG)
            render_scene(image, scene, i / max(1, total - 1))
            image.save(args.frames_dir / f"frame_{frame_index:05d}.png")
            frame_index += 1
    print(f"wrote {frame_index} frames to {args.frames_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
