# 可打印模型

这些 STL 是 13keyAgentTools Rev 0.8 的可打印导出文件，可直接导入 Bambu Studio、PrusaSlicer、Cura 等切片器。

| 文件 | 用途 | 外形尺寸 |
|---|---|---|
| `tolerance_coupon.stl` | 轴孔和 M3 热熔螺母公差测试 | 70 × 42 × 4 mm |
| `plate.stl` | 左侧上层控制面板：13 键、紧凑 EC11 窗口、水平 12 灯窗、主板透明窗和前侧 USB-C 开口 | 120 × 95 × 3 mm |
| `bottom.stl` | 右侧红框下方的主板固定面板：USB-C Arduino Micro 承托架和上层支柱 | 120 × 95 × 14 mm |
| `pixel_carrier.stl` | 水平排列的 12 颗独立 RGB 灯珠承载条 | 67.3 × 8 × 2 mm |
| `window_lens.stl` | 主板透明观察窗，可用透明 PETG 打印 | 23.4 × 49.4 × 1.5 mm |

打印顺序：先打印 `tolerance_coupon.stl`，再打印 `pixel_carrier.stl` 和 `window_lens.stl` 做尺寸验证，最后打印 `plate.stl` 和 `bottom.stl`。`plate.stl` 是上层面板，`bottom.stl` 是下层主板固定面板，不再是封闭式底壳。

STL 是当前 Rev 0.8 的导出物；参数源文件仍在 [../cad/agent_macro.scad](../cad/agent_macro.scad)，导出脚本在 [../tools/generate_stl.py](../tools/generate_stl.py)。USB-C 兼容板的插座位置和透明窗片仍需在首件打印后核对。
