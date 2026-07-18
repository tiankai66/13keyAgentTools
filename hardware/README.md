# 物理硬件

本项目第一版是手焊结构，不需要定制 PCB。

## 关键选择

- Arduino Micro：ATmega32U4，5V / 16MHz，Micro-USB。
- 13 个按键使用 4×4 矩阵，因此需要 13 个 1N4148 二极管。
- 两个 EC11、摇杆、TTP223 和 12 颗 quota RGB 灯数据线使用独立引脚。
- 所有模块共用 GND。

## 接线顺序

1. 先焊 4 行和 4 列矩阵，不接 USB。
2. 万用表逐点确认没有行列短路。
3. 只接 Arduino Micro 和矩阵，上传固件测试按键。
4. 接两个 EC11 和 TTP223，分别测试工作旋钮、音量旋钮和触摸层。
5. 最后接摇杆和 12 颗 quota RGB 灯，限制亮度后再插电脑。

详细引脚见 [wiring/pinout.md](wiring/pinout.md)，采购清单见 [bom.csv](bom.csv)。
