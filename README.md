# 13keyAgentTools

一个面向 Codex、Claude Code、Qoder 等终端工具的开源宏键盘。它本质上是一个可编程宏按键设备，通过标准 USB HID 和可选 USB CDC 与不同 Agent 工作流配合。

本项目采用“3D 打印外壳 + Arduino Micro 手焊 + 可替换固件”的第一版路线，不要求先设计定制 PCB。目标是先做出可靠的通用宏键盘，再逐步增加多 Agent 状态同步、配置工具和可选专用 PCB。

## 当前方案

- 主控：Arduino Micro 兼容板，ATmega32U4，5V / 16MHz，USB-C 数据接口
- 输入：13 键矩阵、1 个 EC11 音量旋钮
- 输出：USB HID 键盘；面板 12 颗独立 RGB 灯显示当前 Agent 剩余用量
- 外壳：OpenSCAD 参数化封闭式盒体，PLA/PETG 3D 打印；紧凑布局
- 固件：Arduino IDE MVP；稳定后迁移到 QMK/Vial
- 主机端：USB CDC 串口状态测试工具；后续接入各 Agent 的 hooks、CLI 事件或桌面自动化

## 目录

```text
13keyAgentTools/
├── mechanical/       3D 打印建模、参数、公差和打印记录
├── hardware/         BOM、手焊接线、测试计划
├── firmware/         Arduino Micro 固件和后续 QMK 迁移位置
├── host/             主机端 RGB 状态桥接和测试工具
├── docs/             工程决策、版本记录和迭代流程
└── .github/          自动检查
```

## 快速开始

1. 先阅读面向新手的 [硬件装配指南](docs/BEGINNER_BUILD_GUIDE.md)，再阅读 [硬件接线说明](hardware/wiring/README.md)。
2. 将 [公差件 STL](mechanical/exports/tolerance_coupon.stl) 导入 Bambu Studio，先验证轴孔和 M3 铜螺母配合。
3. 将 [灯珠承载条](mechanical/exports/pixel_carrier.stl)、[主板透明窗](mechanical/exports/window_lens.stl)、[定位板 STL](mechanical/exports/plate.stl) 和 [下层面板 STL](mechanical/exports/bottom.stl) 导入切片器打印；参数见 [打印计划](mechanical/print/PRINT_PLAN.md)。
4. 也可以用 OpenSCAD 打开 `mechanical/cad/agent_macro.scad`，或运行 `make cad-export` 重新生成 STL。
5. 打印外壳和定位板，先安装 6 个按键、1 个旋钮和 12 颗 RGB 灯中的一小段进行验证。
6. 在 Arduino IDE 中打开 `firmware/arduino/agent_macro_mvp/agent_macro_mvp.ino`。
7. 选择 `Arduino Micro`，上传固件后逐个验证按键、旋钮和面板 RGB 灯。
8. 安装主机端测试工具：

   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   pip install -r host/agentd/requirements.txt
   python host/agentd/agentd.py --list
   ```

## 版本路线

### Rev 0.1：手焊 MVP

- 6 个按键
- 旋钮
- 单颗 RGB 灯
- Arduino `Keyboard.h`
- 串口发送测试灯效

### Rev 0.2：完整输入设备和用量反馈

- 13 键矩阵和 13 个 1N4148 二极管
- 工作旋钮、音量旋钮、摇杆、TTP223
- 前侧 12 灯 quota 灯带
- PETG 外壳和底壳
- Accept / Reject 使用长按保护

### Rev 0.3：紧凑灯效版

- 移除中心指托，缩短外壳尺寸
- 增加音量 EC11 旋钮
- 12 颗独立可编址 RGB 灯按颗排列，支持用量条渐变显示

### Rev 0.4：面板灯和单旋钮版

- 采用 13 个按键 + 1 个音量旋钮的蓝图式布局
- 移除摇杆、触摸区和多余控制开孔
- 将 12 颗 RGB 灯移到键盘面板，使用一个数据引脚串联控制

### Rev 0.5：按键下置控制板版

- 外壳收缩到约 120 × 100 mm
- 底壳高度增加到 24 mm
- Arduino Micro 放在按键区下方的承托架上
- 右侧只保留窄灯珠轨和音量旋钮，不保留大块空白控制区

### Rev 0.6：双层分体面板版

- 左侧上层面板承载 13 个按键、水平灯带和旋钮
- 右侧示意的下层面板固定 Arduino Micro
- 两块 120 × 95 mm 面板用四角 M3 支柱连接，方便打印、焊接和检修

### Rev 0.6.1：右侧红框主板位

- Arduino Micro 移到右侧空白区下方，避免与按键矩阵重叠
- USB 开口改到右后侧，利用现有空白体积，不增加按键区高度

### Rev 0.7：USB-C 主控接口

- Arduino Micro 兼容板改为 USB-C 数据接口
- 右后侧上、下层面板开口按约 16 × 7 mm 重新导出
- 引脚、固件和矩阵/RGB 接线保持不变，仅更换主控板接口和 USB-C 数据线

### Rev 0.8：前侧供电和主板观察窗

- USB-C 入口调整到图示前侧上边缘，音量旋钮保持在下方
- 右侧主板区域增加透明观察窗
- 13 个按键整体向内收，增加与四角 M3 螺丝的安全距离

### Rev 0.8.1：紧凑 EC11 窗口

- 根据实物照片将旋钮窗口调整为约 12.5 × 12.5 mm 圆角开口
- 保留立式 EC11 结构，缩小窗口而不改变旋钮位置和接线

### Rev 0.8.2：6mm 圆形旋钮轴孔

- 按实物规格将旋钮口改为圆形 6mm 轴孔
- STL 按 6.2mm 导出，适配 FDM 打印公差

### Rev 0.9.4：实测主控与封闭式盒体

- 主控按实物尺寸 35 × 18 × 10 mm 建模，平放在下层盒体内部。
- 下层改为 2.4 mm 底板、16 mm 高的封闭盒底，左右导轨、后挡块和前侧盒壁共同卡住主板。
- Type-C 改为下层前墙 14 × 9 mm 插口，插头从盒体前侧直进，不再依赖上层面板的悬空开口。
- 主板透明窗配套 25.4 × 51.4 × 1.5 mm 透明片，从下方安装后与上层面板一起封闭内部空间；整机装配后是完整盒体。

### Rev 0.3：多 Agent 状态桥

- 主机端接收 Codex、Claude Code、Qoder 等 Agent 的状态
- Raw HID 或 USB CDC 状态协议
- 每个 Agent 独立颜色和等待/运行/完成状态

### Rev 1.0：专用 PCB

- 先保留 Arduino Micro 插座或排针
- 验证无误后再考虑裸 MCU 和集成 USB-C

## 工程原则

- 每个硬件修改先更新 `hardware/wiring/` 和 BOM。
- 每次打印保留耗材、层高、尺寸偏差和照片记录。
- 每次固件修改记录在 `docs/ITERATION_LOG.md`。
- 不把 OpenAI、Anthropic、Qoder、Work Louder 等商标或图标作为项目品牌或商品标识。

## 许可证

本项目新增代码、CAD 和文档默认采用 MIT License，见 [LICENSE](LICENSE)。第三方库和参考项目仍遵循其各自许可证。
