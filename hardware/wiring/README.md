# Arduino Micro 手焊接线

## 结构

13 个按键采用 4×4 矩阵，其中 3 个位置空着。每个按键串联一个 1N4148 二极管，方向统一使用 QMK 的 `COL2ROW` 约定。

QMK 手焊指南对矩阵、二极管和 Pro Micro 控制板有完整说明：<https://docs.qmk.fm/hand_wire>。

## 连接原则

- 按键矩阵的 4 行连接 Arduino Micro 的 D4～D7。
- 按键矩阵的 4 列连接 D8～D11。
- 矩阵二极管的黑色环方向必须统一。
- EC11 的 A/B/按压分别连接 D14/D15/D16。
- 摇杆 VRX/VRY 连接 A0/A1，VCC 接 5V，GND 接 GND。
- TTP223 的 OUT 接 A2，传感铜片接模块的感应端。
- RGB 的 DIN 接 A3，VCC 接 5V，GND 接 GND。

## 手焊安全

- 焊接、改线和测量电阻时拔掉 USB。
- 第一次上电只连接 Arduino Micro，不连接 RGB。
- 不要把 RGB 全白满亮度直接从 USB 长时间供电。
- 先用万用表确认 5V 与 GND 没有短路。
- USB 插口要在外壳上做支撑，避免 Micro-USB 焊盘受力。
