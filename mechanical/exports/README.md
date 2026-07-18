# 可打印模型

这些 STL 是 13keyAgentTools Rev 0.5 的可打印导出文件，可直接导入 Bambu Studio、PrusaSlicer、Cura 等切片器。

| 文件 | 用途 | 外形尺寸 |
|---|---|---|
| `tolerance_coupon.stl` | 轴孔和 M3 热熔螺母公差测试 | 70 × 42 × 4 mm |
| `plate.stl` | 13 键定位板、1 个旋钮开孔和 12 个面板灯窗 | 120 × 100 × 3 mm |
| `bottom.stl` | 带内腔、USB 出线口和 Arduino Micro 承托架的底壳 | 120 × 100 × 24 mm |
| `pixel_carrier.stl` | 12 颗独立 RGB 灯珠承载条 | 8 × 66.8 × 2 mm |

打印顺序：先打印 `tolerance_coupon.stl`，再打印 `pixel_carrier.stl` 确认灯珠尺寸，最后打印定位板和底壳。

STL 是当前 Rev 0.5 的导出物；参数源文件仍在 [../cad/agent_macro.scad](../cad/agent_macro.scad)，导出脚本在 [../tools/generate_stl.py](../tools/generate_stl.py)。
