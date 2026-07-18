#!/usr/bin/env python3
"""Generate Bambu Studio compatible STL files for the two-panel macro keyboard.

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
CONTROLLER_PANEL_T = 4.0
SPACER_H = 10.0
CORNER_R = 4.0
# Use the large right-side blank area under the upper panel for the controller.
CONTROLLER_BOARD_X = 89.0
CONTROLLER_BOARD_Y = 43.0
CONTROLLER_USB_X = 98.0
CONTROLLER_USB_OPENING_W = 16.0
CONTROLLER_USB_OPENING_D = 7.0
KEY_PITCH = 19.05
KEY_HOLE = 14.0
KEY_ORIGIN = (10.0, 8.0)
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


def usb_opening(height: float) -> trimesh.Trimesh:
    """Open the right-rear edge for the USB-C controller."""

    return box(
        CONTROLLER_USB_OPENING_W,
        CONTROLLER_USB_OPENING_D,
        height,
        (CONTROLLER_USB_X, CASE_D, height / 2.0 - 1.0),
    )


def top_panel() -> trimesh.Trimesh:
    """Upper control panel: 13 keys, horizontal RGB rail, and one EC11."""

    base = rounded_prism(CASE_W, CASE_D, PLATE_T, CORNER_R)
    cutters: list[trimesh.Trimesh] = []

    for column, row in KEY_POSITIONS:
        x = KEY_ORIGIN[0] + column * KEY_PITCH + KEY_HOLE / 2.0
        y = KEY_ORIGIN[1] + row * KEY_PITCH + KEY_HOLE / 2.0
        cutters.append(box(KEY_HOLE, KEY_HOLE, PLATE_T + 2, (x, y, PLATE_T / 2.0)))

    cutters.extend(panel_mount_cutters(PLATE_T + 2))

    # Dedicated volume EC11 shaft and anti-rotation clearance.
    x, y = VOLUME_ENCODER
    cutters.append(cylinder(8.0, PLATE_T + 2, (x, y, PLATE_T / 2.0)))
    cutters.append(box(12.0, 16.0, PLATE_T + 2, (x, y + 8.0, PLATE_T / 2.0)))

    # Rear-edge cable opening, intentionally oversized for tolerance.
    cutters.append(usb_opening(PLATE_T + 2))

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
    return difference(base, cutters)


def controller_spacers() -> list[trimesh.Trimesh]:
    """Four integrated M3 spacer rings for the upper panel."""

    rings = []
    for x, y in SCREW_POSITIONS:
        ring = cylinder(
            8.0,
            SPACER_H + 0.1,
            (x, y, CONTROLLER_PANEL_T - 0.1 + (SPACER_H + 0.1) / 2.0),
        )
        hole = cylinder(
            3.4,
            SPACER_H + 2.0,
            (x, y, CONTROLLER_PANEL_T - 0.1 + (SPACER_H + 0.1) / 2.0),
        )
        rings.append(difference(ring, [hole]))
    return rings


def micro_board_shelf() -> list[trimesh.Trimesh]:
    """Shelf and retention blocks for an Arduino Micro rotated vertically."""

    board_x = CONTROLLER_BOARD_X
    board_y = CONTROLLER_BOARD_Y
    shelf = box(
        22.0,
        52.0,
        2.0,
        (board_x + 9.0, board_y + 24.0, CONTROLLER_PANEL_T + 1.0),
    )
    retention_blocks = []
    for x, y in (
        (board_x - 2.0, board_y - 2.0),
        (board_x + 17.0, board_y - 2.0),
        (board_x - 2.0, board_y + 47.0),
        (board_x + 17.0, board_y + 47.0),
    ):
        retention_blocks.append(
            box(3.0, 3.0, 4.0, (x + 1.5, y + 1.5, CONTROLLER_PANEL_T + 4.0))
        )
    return [shelf, *retention_blocks]


def controller_panel() -> trimesh.Trimesh:
    """Lower panel with an Arduino Micro shelf and upper-panel spacers."""

    base = rounded_prism(CASE_W, CASE_D, CONTROLLER_PANEL_T, CORNER_R)
    cutters = panel_mount_cutters(CONTROLLER_PANEL_T + SPACER_H + 2.0)
    cutters.append(usb_opening(CONTROLLER_PANEL_T + 2.0))
    shell = difference(base, cutters)
    return union([shell, *controller_spacers(), *micro_board_shelf()])


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
