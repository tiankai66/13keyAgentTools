// 13keyAgentTools Rev 0.3
// Parametric enclosure for a hand-wired Arduino Micro multi-agent macro keyboard.
// Export one part at a time by changing `part`.

part = "plate"; // plate / bottom / assembly / tolerance

$fn = 48;

case_w = 164;
case_d = 104;
plate_t = 3.0;
bottom_h = 18.0;
bottom_t = 3.0;
wall = 3.0;
corner_r = 4.0;

key_pitch = 19.05;
key_hole = 14.0;
key_origin = [16, 14];

// Two EC11 encoders: action/reasoning and dedicated volume control.
action_encoder = [112, 34];
volume_encoder = [140, 34];
joystick_center = [112, 76];
touch_center = [140, 76];

// Twelve individually addressable RGB pixels arranged as a smooth quota bar.
quota_led_count = 12;
quota_led_start_x = 14;
quota_led_pitch = 12.5;
quota_led_window_w = 8;
quota_led_window_h = 5;
quota_led_center_z = 9;

// 4 x 4 electrical matrix with three unused positions.
// Rev 0.3 keeps 13 individual 1U keys and reserves the right side for controls.
key_positions = [
    [0, 0], [1, 0], [2, 0], [3, 0],
    [0, 1], [1, 1], [2, 1], [3, 1],
    [0, 2], [1, 2], [2, 2], [3, 2],
    [1, 3]
];

screw_positions = [
    [7, 7],
    [case_w - 7, 7],
    [7, case_d - 7],
    [case_w - 7, case_d - 7]
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

module screw_holes(extra = 1) {
    for (p = screw_positions) {
        translate([p[0], p[1], -extra])
            cylinder(d = 3.4, h = plate_t + bottom_h + 2 * extra);
    }
}

module control_holes(extra = 1) {
    // Action/reasoning EC11 shaft and anti-rotation clearance.
    translate([action_encoder[0], action_encoder[1], -extra])
        cylinder(d = 8.0, h = plate_t + 2 * extra);
    translate([action_encoder[0], action_encoder[1] - 8, -extra])
        cube([12, 16, plate_t + 2 * extra], center = true);

    // Dedicated volume EC11 shaft and anti-rotation clearance.
    translate([volume_encoder[0], volume_encoder[1], -extra])
        cylinder(d = 8.0, h = plate_t + 2 * extra);
    translate([volume_encoder[0], volume_encoder[1] - 8, -extra])
        cube([12, 16, plate_t + 2 * extra], center = true);

    // Generic 2-axis joystick keep-out. Tune after buying the actual module.
    translate([joystick_center[0], joystick_center[1], -extra])
        cube([19, 19, plate_t + 2 * extra], center = true);

    // TTP223 copper touch window.
    translate([touch_center[0], touch_center[1], -extra])
        cube([14, 14, plate_t + 2 * extra], center = true);

    // Rear USB opening. This is intentionally oversized for cable tolerance.
    translate([case_w / 2 - 9, case_d - 4, -extra])
        cube([18, 8, 9], center = false);
}

module quota_windows(extra = 1) {
    // Individual windows keep each RGB pixel visually separated.
    for (i = [0 : quota_led_count - 1]) {
        translate([
            quota_led_start_x + i * quota_led_pitch,
            -extra,
            quota_led_center_z - quota_led_window_h / 2
        ])
            cube([
                quota_led_window_w,
                wall + 2 * extra,
                quota_led_window_h
            ], center = false);
    }
}

module plate() {
    difference() {
        rounded_prism(case_w, case_d, plate_t, corner_r);
        key_holes();
        screw_holes();
        control_holes();
    }
}

module bottom() {
    difference() {
        rounded_prism(case_w, case_d, bottom_h, corner_r);

        // Main cavity. Keep a solid bottom and a perimeter wall.
        translate([wall, wall, bottom_t])
            cube([
                case_w - 2 * wall,
                case_d - 2 * wall,
                bottom_h
            ], center = false);

        // Through holes for M3 hardware.
        for (p = screw_positions) {
            translate([p[0], p[1], -1])
                cylinder(d = 3.4, h = bottom_h + 2);
        }

        // Rear cable relief.
        translate([case_w / 2 - 10, case_d - 5, 4])
            cube([20, 8, 10], center = false);

        quota_windows();
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
        translate([0, 0, bottom_h])
            plate();
    color("#666666")
        bottom();
}

if (part == "plate") {
    plate();
} else if (part == "bottom") {
    bottom();
} else if (part == "assembly") {
    assembly();
} else if (part == "tolerance") {
    tolerance_coupon();
}
