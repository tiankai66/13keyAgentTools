# 项目状态

当前版本：`0.2.0-design-iteration`

## 已完成

- 独立 Git 项目目录和远程仓库连接
- Arduino Micro 5V/16MHz 方案
- 4×4 按键矩阵接线定义
- EC11、摇杆、TTP223、RGB 引脚定义
- OpenSCAD 参数化外壳初稿
- 中心防误触指托、第二个音量旋钮和 12 灯 quota 灯带布局
- Bambu Studio 可导入的 Rev 0.2 STL 导出链路
- Arduino IDE MVP 固件骨架
- 主机端 USB CDC 灯效测试工具

## 尚未验证

- Rev 0.2 外壳与实际轴体、两个旋钮、摇杆和灯带的尺寸配合
- 二极管方向和矩阵扫描
- Arduino Micro 与所有输入设备同时工作时的电流余量
- 12 灯带满亮度下的 USB 供电能力
- 各 Agent CLI 的最终状态 hooks

## 当前不做

- 蓝牙和电池
- 裸 ATmega32U4 专用 PCB
- 任一厂商的官方图标键帽
- 自动批准 Agent 操作
