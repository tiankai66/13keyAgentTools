# 可打印模型

这些 STL 是 13keyAgentTools Rev 0.1 的可打印导出文件，可直接导入 Bambu Studio、PrusaSlicer、Cura 等切片器。

| 文件 | 用途 | 外形尺寸 |
|---|---|---|
| `tolerance_coupon.stl` | 轴孔和 M3 热熔螺母公差测试 | 70 × 42 × 4 mm |
| `plate.stl` | 13 键定位板 | 148 × 106 × 3 mm |
| `bottom.stl` | 带内腔和 USB 出线口的底壳 | 148 × 106 × 18 mm |

打印顺序：先打印 `tolerance_coupon.stl`，确认实际轴体和铜螺母配合后，再打印定位板和底壳。

STL 是当前 Rev 0.1 的导出物；参数源文件仍在 [../cad/agent_macro.scad](../cad/agent_macro.scad)，导出脚本在 [../tools/generate_stl.py](../tools/generate_stl.py)。
