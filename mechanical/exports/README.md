# 可打印模型

这些 STL 是 13keyAgentTools Rev 0.9.4 的可打印导出文件，可直接导入 Bambu Studio、PrusaSlicer、Cura 等切片器。

| 文件 | 用途 | 外形尺寸 |
|---|---|---|
| `tolerance_coupon.stl` | 轴孔和 M3 热熔螺母公差测试 | 70 × 42 × 4 mm |
| `plate.stl` | 上层控制盖：13 键、6 mm 圆形 EC11 轴孔、水平 12 灯窗和主板透明窗 | 120 × 95 × 3 mm |
| `bottom.stl` | 下层封闭盒体：2.4 mm 底板、16 mm 盒体高度、35×18×10 mm 主控卡槽和前墙 Type-C 插口 | 120 × 95 × 16 mm |
| `pixel_carrier.stl` | 水平排列的 12 颗独立 RGB 灯珠承载条 | 67.3 × 8 × 2 mm |
| `window_lens.stl` | 封闭主板透明观察窗，可用透明 PETG 打印 | 25.4 × 51.4 × 1.5 mm |

打印顺序：先打印 `tolerance_coupon.stl`，再打印 `pixel_carrier.stl`、`window_lens.stl` 和 `bottom.stl` 做尺寸验证，最后打印 `plate.stl`。`bottom.stl` 是封闭式盒底，`plate.stl` 是带透明观察窗的上层控制盖。

STL 是当前 Rev 0.9.4 的导出物；参数源文件仍在 [../cad/agent_macro.scad](../cad/agent_macro.scad)，导出脚本在 [../tools/generate_stl.py](../tools/generate_stl.py)。主控卡槽和 Type-C 插口仍需用实物首件确认。
