// 13keyAgentTools Rev 0.7
// Two-panel layout: controls on the upper panel, Arduino Micro on the lower panel.
// Export one part at a time by changing `part`.

part = "plate"; // plate / bottom / controller_panel / assembly / tolerance / pixel_carrier

$fn = 48;

case_w = 120;
case_d = 95;
plate_t = 3.0;
controller_panel_t = 4.0;
spacer_h = 10.0;
corner_r = 4.0;

// Use the large right-side blank area under the upper panel for the controller.
// The board is rotated vertically and its USB connector faces the rear edge.
controller_board_x = 89;
controller_board_y = 43;
controller_usb_x = 98;
controller_usb_opening_w = 16;
controller_usb_opening_d = 7;

key_pitch = 19.05;
key_hole = 14.0;
// One EC11 encoder, reserved for future system-volume control.
volume_encoder = [104, 15];

// Twelve individually addressable RGB pixels on a horizontal top-panel rail.
quota_led_count = 12;
quota_led_start_x = 32;
quota_led_y = 15;
quota_led_pitch = 5.3;
quota_led_window_w = 5;
quota_led_window_d = 4.5;

// One key in the top-left plus a compact 4 x 3 matrix below it: 13 individual 1U keys.
key_positions = [
    [0, 0],
    [0, 1], [1, 1], [2, 1], [3, 1],
    [0, 2], [1, 2], [2, 2], [3, 2],
    [0, 3], [1, 3], [2, 3], [3, 3]
];
key_origin = [10, 8];

screw_positions = [
    [5, 5],
    [case_w - 5, 5],
    [5, case_d - 5],
    [case_w - 5, case_d - 5]
];

module rounded_prism(w, d, h, r) {
    linear_extrude(height = h)
        offset(r = r)
            offset(delta = -r)
                square([w, d], center = false);
}

module key_holes(extra = 1) {
    for (p = key_positions) {
        translate([
            key_origin[0] + p[0] * key_pitch,
            key_origin[1] + p[1] * key_pitch,
            -extra
        ])
            cube([key_hole, key_hole, plate_t + 2 * extra], center = false);
    }
}

module screw_holes(extra = 1, height = plate_t + 2) {
    for (p = screw_positions) {
        translate([p[0], p[1], -extra])
            cylinder(d = 3.4, h = height);
    }
}

module usb_opening(extra = 1, height = plate_t + 2) {
    // Right-rear Type-C relief under the controller area.
    translate([
        controller_usb_x - controller_usb_opening_w / 2,
        case_d - controller_usb_opening_d / 2,
        -extra
    ])
        cube([controller_usb_opening_w, controller_usb_opening_d, height], center = false);
}

module control_holes(extra = 1) {
    // Dedicated volume EC11 shaft and anti-rotation clearance.
    translate([volume_encoder[0], volume_encoder[1], -extra])
        cylinder(d = 8.0, h = plate_t + 2 * extra);
    translate([volume_encoder[0], volume_encoder[1] + 8, -extra])
        cube([12, 16, plate_t + 2 * extra], center = true);

    usb_opening(extra);
}

module quota_windows(extra = 1) {
    // Individual top-panel windows keep each RGB pixel visually separated.
    for (i = [0 : quota_led_count - 1]) {
        translate([
            quota_led_start_x + i * quota_led_pitch - quota_led_window_w / 2,
            quota_led_y - quota_led_window_d / 2,
            -extra
        ])
            cube([
                quota_led_window_w,
                quota_led_window_d,
                plate_t + 2 * extra
            ], center = false);
    }
}

module plate() {
    difference() {
        rounded_prism(case_w, case_d, plate_t, corner_r);
        key_holes();
        screw_holes();
        control_holes();
        quota_windows();
    }
}

module controller_spacers() {
    // Four integrated M3 spacer rings hold the upper panel 10 mm above the
    // controller panel. The rings are printed as part of the lower panel.
    for (p = screw_positions) {
        translate([p[0], p[1], controller_panel_t - 0.1])
            difference() {
                cylinder(d = 8, h = spacer_h + 0.1);
                translate([0, 0, -1])
                    cylinder(d = 3.4, h = spacer_h + 2);
            }
    }
}

module controller_panel() {
    union() {
        difference() {
            rounded_prism(case_w, case_d, controller_panel_t, corner_r);

            // Through holes and rear USB cable relief.
            screw_holes(height = controller_panel_t + spacer_h + 2);
            usb_opening(height = controller_panel_t + 2);
        }
        controller_spacers();
        micro_board_shelf();
    }
}

module micro_board_shelf() {
    // Generic Arduino Micro mounted vertically: 18 x 48 mm board outline.
    // Retention blocks avoid depending on clone-specific mounting-hole spacing.
    board_x = controller_board_x;
    board_y = controller_board_y;
    shelf_w = 22;
    shelf_d = 52;
    translate([board_x - 2, board_y - 2, controller_panel_t])
        cube([shelf_w, shelf_d, 2], center = false);
    for (p = [
        [board_x - 2, board_y - 2],
        [board_x + 17, board_y - 2],
        [board_x - 2, board_y + 47],
        [board_x + 17, board_y + 47]
    ]) {
        translate([p[0], p[1], controller_panel_t + 2])
            cube([3, 3, 4], center = false);
    }
}

module pixel_carrier() {
    // Thin horizontal carrier for 12 individually wired 5 mm-class RGB pixels.
    carrier_w = (quota_led_count - 1) * quota_led_pitch + quota_led_window_w + 4;
    carrier_d = 8;
    carrier_t = 2;
    carrier_x = quota_led_start_x - 2;
    carrier_y = quota_led_y - carrier_d / 2;
    difference() {
        translate([carrier_x, carrier_y, 0])
            rounded_prism(carrier_w, carrier_d, carrier_t, 1.5);
        for (i = [0 : quota_led_count - 1]) {
            translate([
                quota_led_start_x + i * quota_led_pitch - 2.8,
                quota_led_y - 2.8,
                -1
            ])
                cube([5.6, 5.6, carrier_t + 2], center = false);
        }
    }
}

module tolerance_coupon() {
    coupon_w = 70;
    coupon_d = 42;
    difference() {
        rounded_prism(coupon_w, coupon_d, 4, 2);

        // Four switch-hole variants: 13.8, 14.0, 14.2, 14.4 mm.
        for (i = [0 : 3]) {
            translate([9 + i * 17, 21, -1])
                cube([13.8 + i * 0.2, 13.8 + i * 0.2, 6], center = true);
        }

        // M3 insert-hole variants.
        for (i = [0 : 2]) {
            translate([12 + i * 18, 8, -1])
                cylinder(d = 4.0 + i * 0.2, h = 6);
        }
    }
}

module assembly() {
    color("#d8d8d8")
        translate([0, 0, controller_panel_t + spacer_h])
            plate();
    color("#666666")
        controller_panel();
    color("#555555")
        translate([0, 0, controller_panel_t + spacer_h - 2])
            pixel_carrier();
}

if (part == "plate") {
    plate();
} else if (part == "bottom") {
    controller_panel();
} else if (part == "controller_panel") {
    controller_panel();
} else if (part == "assembly") {
    assembly();
} else if (part == "tolerance") {
    tolerance_coupon();
} else if (part == "pixel_carrier") {
    pixel_carrier();
}
