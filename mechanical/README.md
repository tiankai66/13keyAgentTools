# 3D 打印建模

当前使用 OpenSCAD 做参数化 Rev 0.7。模型拆成上、下两块独立面板：先打印公差件，再打印灯珠承载条、上层控制面板和下层主板固定面板。

## 文件

- `cad/agent_macro.scad`：上层控制面板、下层主板固定面板、装配预览和公差件。
- `exports/`：可直接导入 Bambu Studio、PrusaSlicer 或 Cura 的 STL 文件。
- `exports/pixel_carrier.stl`：固定 12 颗独立 RGB 灯珠的承载条。
- `exports/window_lens.stl`：主板透明观察窗的可选透明 PETG 镜片；追求清晰度时优先使用亚克力片。
- `tools/generate_stl.py`：无 GUI 环境下的可重复 STL 导出脚本。
- `print/PRINT_PLAN.md`：切片、打印顺序和验收记录模板。

## 设计基准

- 两块面板尺寸：120 × 95 mm。
- 按键间距：19.05 mm。
- MX 轴孔初始尺寸：14.0 mm。
- 上盖厚度：3 mm。
- 下层面板厚度：4 mm；集成 10 mm 上层支柱和 Arduino Micro 承托架。
- Arduino Micro 承托架位于右侧红框空白区下方，主板竖向放置，USB-C 开口位于图示前侧上边缘。
- EC11 使用立式/垂直轴安装，轴线垂直于 3 mm 上层面板；本模型不兼容卧式/侧插编码器。
- 按照片中的小型 EC11 优化为约 12.5 × 12.5 mm 圆角开口，不再使用偏大的 12 × 16 mm 长窗。
- 上层面板右侧增加 24 × 50 mm 主板透明观察窗，窗口四周给 M3 螺丝和按键留出间隙。
- 固定方式：M3 螺丝 + 热熔铜螺母。
- 面板 quota RGB 灯：12 个独立窗口，间距 5.3 mm。

这些数值是 Rev 0.8 的可打印起点，不是最终量产尺寸。主控改为 USB-C Arduino Micro 兼容板，图示前侧开口约 16 × 7 mm；下单前仍需核对具体兼容板的 USB-C 位置。

## 导出

在 OpenSCAD 顶部修改：

```scad
part = "plate";     // plate / bottom / controller_panel / assembly / tolerance / pixel_carrier
```

按 `F6` 渲染后导出 STL。当前 Rev 0.8 的 STL 已提交到 `mechanical/exports/`，方便直接下载和导入切片器。为兼容原有链接，`plate.stl` 表示上层面板，`bottom.stl` 表示下层主板固定面板。

如果 OpenSCAD 命令行不可用，可安装脚本依赖后执行：

```bash
python3 -m venv /tmp/13key-cad-venv
. /tmp/13key-cad-venv/bin/activate
pip install -r mechanical/tools/requirements.txt
python mechanical/tools/generate_stl.py --part all
```

脚本生成的模型与当前 Rev 0.8 的 OpenSCAD 参数保持一致；修改尺寸时需要同步检查两个源文件。
