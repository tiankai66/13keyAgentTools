# 项目状态

当前版本：`0.4.0-panel-light-single-encoder`

## 已完成

- 独立 Git 项目目录和远程仓库连接
- Arduino Micro 5V/16MHz 方案
- 4×4 按键矩阵接线定义
- EC11 和面板 RGB 灯引脚定义
- OpenSCAD 参数化外壳初稿
- 13 键 + 1 个音量旋钮的紧凑型布局
- 面板上的 12 颗独立 RGB quota 灯布局
- 可打印的 12 灯珠承载条，解决逐颗灯珠的面板定位
- Bambu Studio 可导入的 Rev 0.4 STL 导出链路
- Arduino IDE MVP 固件骨架
- 主机端 USB CDC 灯效测试工具

## 尚未验证

- Rev 0.4 外壳与实际轴体、EC11 和面板 RGB 灯的尺寸配合
- 二极管方向和矩阵扫描
- Arduino Micro 与所有输入设备同时工作时的电流余量
- 12 颗 RGB 灯满亮度下的 USB 供电能力
- 各 Agent CLI 的最终状态 hooks

## 当前不做

- 蓝牙和电池
- 裸 ATmega32U4 专用 PCB
- 任一厂商的官方图标键帽
- 自动批准 Agent 操作
