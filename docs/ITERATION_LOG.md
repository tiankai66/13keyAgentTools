# 迭代记录

## 2026-07-18 — 0.1.0

### 决策

- 新建独立工程 `13keyAgentTools`，不修改同级的旧 `project/` 目录。
- 第一版采用 Arduino Micro，而不是直接设计专用 PCB。
- 13 个按键采用 4×4 矩阵，控制设备占用独立引脚。
- 第一版使用 USB 有线连接，不引入蓝牙、电池和充电电路。

### 下一步

- 打印 `mechanical/cad/agent_macro.scad` 的 `tolerance` 部件。
- 采购并测试 6 个按键、1 个 EC11、1 个 Arduino Micro。
- 在没有 RGB 的情况下完成矩阵和旋钮输入验证。
