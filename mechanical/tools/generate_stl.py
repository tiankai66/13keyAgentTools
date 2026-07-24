#!/usr/bin/env python3
"""Generate Rev 0.9.4 Bambu Studio compatible STL files for the closed-box macro keyboard.

The OpenSCAD file remains the design source. This script is a headless export
path for macOS environments where the OpenSCAD GUI binary cannot render from
the command line.

Units are millimetres. The output is standard binary STL, which can be opened
directly by Bambu Studio, PrusaSlicer, Cura, and similar slicers.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import trimesh


CASE_W = 120.0
CASE_D = 95.0
PLATE_T = 3.0
BOTTOM_FLOOR_T = 2.4
BOTTOM_WALL_T = 2.4
BOTTOM_BOX_H = 16.0
CORNER_R = 4.0
# Measured 35 x 18 x 10 mm controller board, lying flat with USB-C facing front.
CONTROLLER_BOARD_W = 18.0
CONTROLLER_BOARD_L = 35.0
CONTROLLER_BOARD_H = 10.0
CONTROLLER_BOARD_X = 89.0
CONTROLLER_BOARD_Y = 57.5
CONTROLLER_USB_X = 98.0
CONTROLLER_USB_OPENING_W = 14.0
CONTROLLER_USB_OPENING_D = 5.0
CONTROLLER_USB_OPENING_Z = 4.0
CONTROLLER_USB_OPENING_H = 9.0
CONTROLLER_BOARD_CLEARANCE = 0.6
CONTROLLER_WINDOW_X = 98.0
CONTROLLER_WINDOW_Y = 65.0
CONTROLLER_WINDOW_W = 24.0
CONTROLLER_WINDOW_D = 50.0
WINDOW_LENS_T = 1.5
WINDOW_LENS_W = 25.4
WINDOW_LENS_D = 51.4
KEY_PITCH = 19.05
KEY_HOLE = 14.0
KEY_ORIGIN = (12.0, 10.0)
KEY_POSITIONS = (
    (0, 0),
    (0, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (0, 2),
    (1, 2),
    (2, 2),
    (3, 2),
    (0, 3),
    (1, 3),
    (2, 3),
    (3, 3),
)
SCREW_POSITIONS = (
    (5.0, 5.0),
    (CASE_W - 5.0, 5.0),
    (5.0, CASE_D - 5.0),
    (CASE_W - 5.0, CASE_D - 5.0),
)
VOLUME_ENCODER = (104.0, 15.0)
# Nominal 6 mm encoder shaft; 0.2 mm clearance is intentional for FDM.
ENCODER_SHAFT_HOLE_D = 6.2
QUOTA_LED_COUNT = 12
QUOTA_LED_START_X = 32.0
QUOTA_LED_Y = 15.0
QUOTA_LED_PITCH = 5.3
QUOTA_LED_WINDOW_W = 5.0
QUOTA_LED_WINDOW_D = 4.5
PIXEL_CARRIER_W = (QUOTA_LED_COUNT - 1) * QUOTA_LED_PITCH + QUOTA_LED_WINDOW_W + 4.0
PIXEL_CARRIER_D = 8.0
PIXEL_CARRIER_T = 2.0
PIXEL_CARRIER_X = QUOTA_LED_START_X - 2.0
PIXEL_CARRIER_Y = QUOTA_LED_Y - PIXEL_CARRIER_D / 2.0


def translation(x: float, y: float, z: float):
    return trimesh.transformations.translation_matrix((x, y, z))


def box(width: float, depth: float, height: float, center: tuple[float, float, float]):
    return trimesh.creation.box(
        extents=(width, depth, height),
        transform=translation(*center),
    )


def cylinder(diameter: float, height: float, center: tuple[float, float, float]):
    return trimesh.creation.cylinder(
        radius=diameter / 2.0,
        height=height,
        sections=96,
        transform=translation(*center),
    )


def union(parts: list[trimesh.Trimesh]) -> trimesh.Trimesh:
    return trimesh.boolean.union(parts, engine="manifold")


def difference(base: trimesh.Trimesh, cutters: list[trimesh.Trimesh]) -> trimesh.Trimesh:
    return trimesh.boolean.difference([base, *cutters], engine="manifold")


def rounded_prism(width: float, depth: float, height: float, radius: float):
    """Make a rounded rectangle with its lower face at z=0."""

    center = (width / 2.0, depth / 2.0, height / 2.0)
    parts = [
        box(width - 2 * radius, depth, height, center),
        box(width, depth - 2 * radius, height, center),
    ]
    for x, y in (
        (radius, radius),
        (width - radius, radius),
        (radius, depth - radius),
        (width - radius, depth - radius),
    ):
        parts.append(cylinder(2 * radius, height, (x, y, height / 2.0)))
    return union(parts)


def panel_mount_cutters(height: float) -> list[trimesh.Trimesh]:
    cutters = []
    for x, y in SCREW_POSITIONS:
        cutters.append(cylinder(3.4, height, (x, y, height / 2.0 - 1.0)))
    return cutters


def usb_port_opening() -> trimesh.Trimesh:
    """Cut a 14 x 9 mm Type-C plug opening through the lower front wall."""

    return box(
        CONTROLLER_USB_OPENING_W,
        CONTROLLER_USB_OPENING_D,
        CONTROLLER_USB_OPENING_H,
        (
            CONTROLLER_USB_X,
            CASE_D - CONTROLLER_USB_OPENING_D / 2.0,
            CONTROLLER_USB_OPENING_Z + CONTROLLER_USB_OPENING_H / 2.0,
        ),
    )


def controller_window() -> trimesh.Trimesh:
    """Create the clear inspection-window cutter above the controller board."""

    mesh = rounded_prism(
        CONTROLLER_WINDOW_W,
        CONTROLLER_WINDOW_D,
        PLATE_T + 2.0,
        2.0,
    )
    mesh.apply_translation(
        (
            CONTROLLER_WINDOW_X - CONTROLLER_WINDOW_W / 2.0,
            CONTROLLER_WINDOW_Y - CONTROLLER_WINDOW_D / 2.0,
            -1.0,
        )
    )
    return mesh


def encoder_shaft_hole() -> trimesh.Trimesh:
    """Create the circular clearance hole for the photographed 6 mm EC11 shaft."""

    return cylinder(
        ENCODER_SHAFT_HOLE_D,
        PLATE_T + 2.0,
        (VOLUME_ENCODER[0], VOLUME_ENCODER[1], PLATE_T / 2.0),
    )


def top_panel() -> trimesh.Trimesh:
    """Upper control panel: 13 keys, RGB rail, window, and vertical EC11."""

    base = rounded_prism(CASE_W, CASE_D, PLATE_T, CORNER_R)
    cutters: list[trimesh.Trimesh] = []

    for column, row in KEY_POSITIONS:
        x = KEY_ORIGIN[0] + column * KEY_PITCH + KEY_HOLE / 2.0
        y = KEY_ORIGIN[1] + row * KEY_PITCH + KEY_HOLE / 2.0
        cutters.append(box(KEY_HOLE, KEY_HOLE, PLATE_T + 2, (x, y, PLATE_T / 2.0)))

    cutters.extend(panel_mount_cutters(PLATE_T + 2))

    # Circular clearance hole for the photographed 6 mm vertical EC11 shaft.
    cutters.append(encoder_shaft_hole())

    # Twelve horizontal individual RGB windows.
    for index in range(QUOTA_LED_COUNT):
        x = QUOTA_LED_START_X + index * QUOTA_LED_PITCH
        cutters.append(
            box(
                QUOTA_LED_WINDOW_W,
                QUOTA_LED_WINDOW_D,
                PLATE_T + 2,
                (x, QUOTA_LED_Y, PLATE_T / 2.0),
            )
        )
    cutters.append(controller_window())
    return difference(base, cutters)


def corner_bosses() -> list[trimesh.Trimesh]:
    """Four integrated M3 bosses that retain the upper lid."""

    rings = []
    for x, y in SCREW_POSITIONS:
        ring = cylinder(8.0, BOTTOM_BOX_H, (x, y, BOTTOM_BOX_H / 2.0))
        hole = cylinder(
            3.4,
            BOTTOM_BOX_H + 2.0,
            (x, y, BOTTOM_BOX_H / 2.0),
        )
        rings.append(difference(ring, [hole]))
    return rings


def micro_board_shelf() -> list[trimesh.Trimesh]:
    """Captive cradle for the measured 35 x 18 x 10 mm controller board."""

    board_x = CONTROLLER_BOARD_X
    board_y = CONTROLLER_BOARD_Y
    pad_x = board_x - CONTROLLER_BOARD_CLEARANCE
    pad_y = board_y - CONTROLLER_BOARD_CLEARANCE
    pad_w = CONTROLLER_BOARD_W + 2.0 * CONTROLLER_BOARD_CLEARANCE
    pad_d = CONTROLLER_BOARD_L + 2.0 * CONTROLLER_BOARD_CLEARANCE
    pad_t = 1.2
    rail_t = 1.4
    rail_bottom = BOTTOM_FLOOR_T + pad_t - 0.05
    rail_h = BOTTOM_BOX_H - 0.6 - rail_bottom
    shelf = box(
        pad_w,
        pad_d,
        pad_t + 0.1,
        (pad_x + pad_w / 2.0, pad_y + pad_d / 2.0, BOTTOM_FLOOR_T + pad_t / 2.0),
    )
    left_rail = box(
        rail_t,
        pad_d,
        rail_h,
        (pad_x - rail_t / 2.0, pad_y + pad_d / 2.0, rail_bottom + rail_h / 2.0),
    )
    right_rail = box(
        rail_t,
        pad_d,
        rail_h,
        (pad_x + pad_w + rail_t / 2.0, pad_y + pad_d / 2.0, rail_bottom + rail_h / 2.0),
    )
    rear_stop = box(
        pad_w + 2.0 * rail_t,
        1.4,
        5.0,
        (pad_x + pad_w / 2.0, pad_y + 0.7, rail_bottom + 2.5),
    )
    return [shelf, left_rail, right_rail, rear_stop]


def controller_panel() -> trimesh.Trimesh:
    """Closed lower box with Type-C port and captive Arduino Micro cradle."""

    base = rounded_prism(CASE_W, CASE_D, BOTTOM_BOX_H, CORNER_R)
    inner = rounded_prism(
        CASE_W - 2.0 * BOTTOM_WALL_T,
        CASE_D - 2.0 * BOTTOM_WALL_T,
        BOTTOM_BOX_H,
        CORNER_R - BOTTOM_WALL_T,
    )
    inner.apply_translation((BOTTOM_WALL_T, BOTTOM_WALL_T, BOTTOM_FLOOR_T))
    cutters = [inner, *panel_mount_cutters(BOTTOM_BOX_H + 2.0), usb_port_opening()]
    shell = difference(base, cutters)
    return union([shell, *corner_bosses(), *micro_board_shelf()])


def pixel_carrier() -> trimesh.Trimesh:
    """Print a thin horizontal carrier for individually wired RGB pixels."""

    base = rounded_prism(PIXEL_CARRIER_W, PIXEL_CARRIER_D, PIXEL_CARRIER_T, 1.5)
    cutters: list[trimesh.Trimesh] = []
    for index in range(QUOTA_LED_COUNT):
        x = QUOTA_LED_START_X + index * QUOTA_LED_PITCH - PIXEL_CARRIER_X
        y = QUOTA_LED_Y - PIXEL_CARRIER_Y
        cutters.append(
            box(
                5.6,
                5.6,
                PIXEL_CARRIER_T + 2,
                (x, y, PIXEL_CARRIER_T / 2.0),
            )
        )
    mesh = difference(base, cutters)
    mesh.apply_translation((PIXEL_CARRIER_X, PIXEL_CARRIER_Y, 0.0))
    return mesh


def window_lens() -> trimesh.Trimesh:
    """Print an optional clear-PETG lens for the controller inspection window."""

    mesh = rounded_prism(WINDOW_LENS_W, WINDOW_LENS_D, WINDOW_LENS_T, 1.5)
    mesh.apply_translation(
        (
            CONTROLLER_WINDOW_X - WINDOW_LENS_W / 2.0,
            CONTROLLER_WINDOW_Y - WINDOW_LENS_D / 2.0,
            0.0,
        )
    )
    return mesh


def tolerance_coupon() -> trimesh.Trimesh:
    coupon_w = 70.0
    coupon_d = 42.0
    base = rounded_prism(coupon_w, coupon_d, 4.0, 2.0)
    cutters: list[trimesh.Trimesh] = []

    for index in range(4):
        size = 13.8 + index * 0.2
        cutters.append(box(size, size, 6.0, (9.0 + index * 17.0, 21.0, 2.0)))

    for index in range(3):
        cutters.append(cylinder(4.0 + index * 0.2, 6.0, (12.0 + index * 18.0, 8.0, 2.0)))
    return difference(base, cutters)


# Keep the existing file names so Bambu Studio projects and links continue to
# work: plate.stl is now the upper panel and bottom.stl is the lower panel.
BUILDERS = {
    "plate": top_panel,
    "bottom": controller_panel,
    "tolerance_coupon": tolerance_coupon,
    "pixel_carrier": pixel_carrier,
    "window_lens": window_lens,
}


def export(part: str, output_dir: Path) -> Path:
    mesh = BUILDERS[part]()
    if not mesh.is_watertight:
        raise RuntimeError(f"{part} is not watertight")
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{part}.stl"
    mesh.export(output, file_type="stl")
    dimensions = mesh.extents
    print(
        f"{output}: {len(mesh.faces)} triangles, "
        f"{dimensions[0]:.2f} x {dimensions[1]:.2f} x {dimensions[2]:.2f} mm"
    )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--part",
        choices=[*BUILDERS, "all"],
        default="all",
        help="part to export (default: all)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "exports",
    )
    args = parser.parse_args()

    parts = BUILDERS if args.part == "all" else {args.part: BUILDERS[args.part]}
    for part in parts:
        export(part, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
