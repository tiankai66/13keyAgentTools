# 物理硬件

本项目第一版是手焊结构，不需要定制 PCB。

从零开始装配请先看 [Rev 0.9.4 从 0 到 1 手焊装配说明书](../docs/BEGINNER_BUILD_GUIDE.md)。

## 关键选择

- Arduino Micro 兼容板：ATmega32U4，5V / 16MHz，USB-C 数据接口；实测板体 35 × 18 × 10 mm。
- 13 个物理按键使用 4×4 电气矩阵，因此需要 13 个 1N4148 二极管；面板物理布局为左上 1 键 + 下方 4×3。
- 一个 EC11 音量旋钮和 12 颗 quota RGB 灯数据线使用独立引脚。
- Arduino Micro 平放在封闭式下层盒体的 35 × 18 × 10 mm 卡槽内，左右导轨留 0.6 mm 间隙，USB-C 朝盒体前墙；上层控制盖由四角固定柱锁紧。
- 所有模块共用 GND。

## 接线顺序

1. 先焊 4 行和 4 列矩阵，不接 USB。
2. 万用表逐点确认没有行列短路。
3. 只接 Arduino Micro 和矩阵，上传固件测试按键。
4. 接 EC11 音量旋钮，测试旋转和按压。
5. 最后接 12 颗 quota RGB 灯，限制亮度后再插电脑。

详细引脚见 [wiring/pinout.md](wiring/pinout.md)，采购清单见 [purchase-list.md](purchase-list.md)，结构化物料表见 [bom.csv](bom.csv)。本版本使用封闭式下层盒体；前墙 Type-C 开口和透明主板窗共同完成防止主板外露的盒体结构。
