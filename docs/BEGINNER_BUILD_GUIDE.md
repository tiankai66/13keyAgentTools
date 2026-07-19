# Rev 0.7 小白装配指南

这是一套**不需要定制 PCB**的手焊方案：13 个按键、1 个立式 EC11 旋钮、12 颗 RGB 灯和 1 块 USB-C Arduino Micro 兼容板。

最重要的原则是：**一次只增加一种硬件，确认正常后再继续。** 不要一开始把所有线全部焊上。

## 先看懂两块打印件

- `plate.stl`：上层面板，安装 13 个按键、立式 EC11 和 12 颗 RGB 灯。
- `bottom.stl`：下层主板面板，Arduino Micro 固定在右侧红框区域下方，USB-C 朝图示前侧上边缘。
- `window_lens.stl`：可选透明主板观察窗；透明亚克力通常比透明 PETG 更清晰。
- `pixel_carrier.stl`：将 12 颗独立 RGB 灯排成水平灯带。
- `tolerance_coupon.stl`：先用来测试轴孔、EC11 和 M3 热熔螺母，不要跳过。

## 0. 准备工具和安全用品

至少准备：

- 电烙铁、焊锡、助焊剂
- 万用表
- 斜口钳、剥线钳、尖嘴钳
- 热缩管或绝缘胶带
- USB-C 数据线
- Arduino IDE

安全规则：

- 焊接、改线、测量电阻时必须拔掉 USB-C 线。
- 第一次上电只连接主控板，不连接 RGB 灯。
- 任何一次上电前，先用万用表检查 5V 和 GND 没有短路。
- 不要把 RGB 灯接到 3.3V，也不要把 5V 和 GND 接反。

## 1. 先打印并试装，不要焊接

建议顺序：

1. 打印 `tolerance_coupon.stl`。
2. 确认机械轴能插入、拔出，M3 热熔螺母不会太松。
3. 打印 `pixel_carrier.stl`，确认 RGB 灯能逐颗放入。
4. 打印 `window_lens.stl`，确认它能落入上层主板窗口。
5. 打印 `plate.stl` 和 `bottom.stl`。
6. 将 13 个轴体插入上层面板。
7. 将**立式 EC11** 从面板下方装入，轴从面板上方伸出。
8. 将 USB-C 主控板放入右侧下层承托架，USB-C 朝图示前侧上边缘开口。

不要在试装通过前使用胶水。主控板需要满足：ATmega32U4、5V、16MHz、约 48×18mm、USB-C 数据接口。

## 2. 第一次只测试 Arduino Micro

1. 用 USB-C 数据线连接主控板和电脑。
2. 打开 Arduino IDE。
3. 选择 `Tools > Board > Arduino Micro`。
4. 选择新出现的串口。
5. 先上传一个简单的 `Blink` 示例，确认板子能正常上传。
6. 再打开项目中的：

   `firmware/arduino/agent_macro_mvp/agent_macro_mvp.ino`

7. 保持 `ENABLE_RGB 0`，上传固件。

如果 Arduino Micro 上传时串口消失：快速按两次板上的 Reset，再选择 Bootloader 串口重新上传。最常见原因是 USB-C 线只有充电功能，先更换数据线。

## 3. 先接一个按键

先只测试物理位置 `A` 的按键，不要马上接 13 个。

当前面板和矩阵编号如下：

```text
[ A ][ --][ --][ --]
[ B ][ C ][ D ][ E ]
[ F ][ G ][ H ][ I ]
[ J ][ K ][ L ][ M ]
```

`A` 按键的测试接线：

- A 所在行连接 Arduino `D4`。
- A 经过二极管连接 Arduino `D8`。
- 二极管黑色环的一端朝向行线，也就是 `D4` 一侧。

打开一个空白文本编辑器，按下 A 应产生 Enter。测试时不要在终端、聊天窗口或正在编辑重要文件的地方操作。

## 4. 接完整的 13 键矩阵

每个按键需要 1 个 `1N4148` 二极管。按照 `COL2ROW` 方向安装：**所有二极管黑色环朝向行线**。

| 行线 | 按键 | Arduino |
|---|---|---|
| Row 0 | A | D4 |
| Row 1 | B、C、D、E | D5 |
| Row 2 | F、G、H、I | D6 |
| Row 3 | J、K、L、M | D7 |

| 列线 | 按键 | Arduino |
|---|---|---|
| Col 0 | A、B、F、J | D8 |
| Col 1 | C、G、K | D9 |
| Col 2 | D、H、L | D10 |
| Col 3 | E、I、M | D11 |

建议用不同颜色的线区分 4 根行线和 4 根列线。焊完后拔掉 USB，用万用表逐点检查：

- 行线之间不能短路。
- 列线之间不能短路。
- 5V 和 GND 不能短路。
- 三个空位不应接任何按键。

然后逐个按 A 到 M，在空白文本编辑器中测试。

## 5. 接立式 EC11 旋钮

当前模型使用的是**立式/垂直轴 EC11**，不是卧式或侧插型。

如果编码器本体标有 `A、B、C、SW1、SW2`：

- `A` → Arduino D2
- `B` → Arduino D3
- `C` → GND
- `SW1` → Arduino D12
- `SW2` → GND

不同厂家脚位顺序可能不同，不要只按外观猜脚位。没有标识时，用万用表找出：旋转时变化的 A/B/C 三脚，以及按下时导通的 SW1/SW2 两脚。

测试结果：

- 旋转一方向发送 F12，另一方向发送 F11。
- 按下旋钮发送 F10。
- 如果方向反了，交换 A 和 B 两根线即可。

## 6. 最后接 12 颗 RGB 灯

确认按键和旋钮都正常后，再安装 RGB。先只接 1 颗灯测试。

接线方式：

```text
Arduino A3 ── 330Ω ── DIN [RGB 0] DOUT ── DIN [RGB 1] DOUT ── ...
Arduino 5V ─────────── 5V 连接所有 RGB 灯
Arduino GND ────────── GND 连接所有 RGB 灯
```

另外在 RGB 电源入口并联一个 `1000µF` 电解电容：正极接 5V，负极接 GND。灯珠上的箭头必须从 Arduino A3 方向指向下一颗灯。

测试 RGB 前：

1. Arduino IDE 安装 `Adafruit NeoPixel`。
2. 将固件中的 `ENABLE_RGB` 改为 `1`。
3. 重新上传固件。
4. 先使用低亮度测试，固件默认亮度为 32/255。

主机端测试：

```bash
python host/agentd/agentd.py --list
python host/agentd/agentd.py --port /dev/cu.usbmodemXXXX --quota 50
```

将示例中的串口替换为实际串口。Windows 下通常是 `COM3` 这类名称。

## 7. 最终装配顺序

1. 拔掉 USB-C。
2. 将 Arduino Micro 固定在下层面板右侧承托架。
3. 将 RGB 灯焊好并固定在 `pixel_carrier` 上。
4. 将按键和 EC11 固定在上层面板。
5. 将矩阵、EC11、RGB 的线整理并用热缩管绝缘。
6. 将透明观察窗贴在上层面板窗口下方，再用 4 个 M3×12mm 螺丝连接上下层面板。
7. 先不拧得太紧，确认 USB-C 插头能顺畅插拔。
8. 最后贴防滑脚垫。

## 常见问题快速判断

| 现象 | 优先检查 |
|---|---|
| 电脑完全不识别主控 | USB-C 是否为数据线、主控是否为 5V/16MHz、双击 Reset |
| 所有按键都没反应 | D4–D7/D8–D11 是否接反、是否漏接 GND、固件是否上传成功 |
| 某一行或某一列没反应 | 对应总线断线、二极管方向或焊点虚焊 |
| 按键触发错误动作 | 按键物理编号与 `actions` 矩阵不一致 |
| EC11 方向相反 | 交换 A、B 两线 |
| RGB 全不亮 | `ENABLE_RGB`、NeoPixel 库、DIN 方向、共地和 5V |
| RGB 一亮主控重启 | 降低亮度、检查 1000µF 电容、不要全白满亮度 USB 供电 |

完整测试项目见 [hardware/test-plan.md](../hardware/test-plan.md)，引脚表见 [hardware/wiring/pinout.md](../hardware/wiring/pinout.md)，采购清单见 [hardware/purchase-list.md](../hardware/purchase-list.md)。
