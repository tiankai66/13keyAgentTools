# Rev 0.3 引脚表

以下是 Arduino Micro 的 Arduino 引脚命名。`A0`～`A3` 既可以作模拟输入，也可以作为数字输入/输出；本项目按具体功能使用。

| 功能 | Arduino 引脚 | 方向 | 说明 |
|---|---:|---|---|
| Matrix row 0 | D4 | 输出 | 逐行扫描 |
| Matrix row 1 | D5 | 输出 | 逐行扫描 |
| Matrix row 2 | D6 | 输出 | 逐行扫描 |
| Matrix row 3 | D7 | 输出 | 逐行扫描 |
| Matrix col 0 | D8 | 输入上拉 | 读取按键 |
| Matrix col 1 | D9 | 输入上拉 | 读取按键 |
| Matrix col 2 | D10 | 输入上拉 | 读取按键 |
| Matrix col 3 | D11 | 输入上拉 | 读取按键 |
| Encoder A | D14 / MISO | 输入上拉 | SPI 标签不影响普通 GPIO 使用 |
| Encoder B | D15 / SCK | 输入上拉 | SPI 标签不影响普通 GPIO 使用 |
| Encoder push | D16 / MOSI | 输入上拉 | 旋钮按下 |
| Volume encoder A | D2 | 输入上拉 | 音量旋转 |
| Volume encoder B | D3 | 输入上拉 | 音量旋转 |
| Volume encoder push | D12 | 输入上拉 | 音量旋钮按下 |
| Joystick X | A0 | 模拟输入 | ADC |
| Joystick Y | A1 | 模拟输入 | ADC |
| Touch OUT | A2 | 输入上拉 | TTP223 数字输出 |
| Quota RGB pixel DIN | A3 | 输出 | 12 颗 WS2812B / SK6812 独立灯珠数据 |

## Rev 0.3 外壳布局

```text
[ 13 键矩阵 ] [ 工作旋钮 ][ 音量旋钮 ] [ 摇杆 ][触摸]
[       前侧 12 颗独立 RGB quota 用量灯窗                 ]
```

音量旋钮使用独立的 D2/D3/D12。前侧 12 颗 RGB 灯使用 A3 串联，按灯珠顺序从左到右显示剩余用量。

## 矩阵位置

固件中的 4×4 位置如下，`--` 是空位：

```text
[ A ][ B ][ C ][ D ]
[ E ][ F ][ G ][ H ]
[ I ][ J ][ K ][ L ]
[ --][ M ][ --][ --]
```

如果后续改成 2U 键帽，先保留两个独立开关，等固件确认后再把它们映射为同一个动作。
