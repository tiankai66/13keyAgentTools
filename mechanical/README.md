# 3D 打印建模

当前使用 OpenSCAD 做参数化 Rev 0.9.4。模型拆成上层控制盖和下层封闭盒底：先打印公差件，再打印灯珠承载条、透明窗、上层控制盖和下层盒体。

## 文件

- `cad/agent_macro.scad`：上层控制盖、下层封闭盒体、主控卡槽、装配预览和公差件。
- `exports/`：可直接导入 Bambu Studio、PrusaSlicer 或 Cura 的 STL 文件。
- `../docs/media/assembly_walkthrough.mp4`：面向新手的封闭盒体装配视频。
- `exports/pixel_carrier.stl`：固定 12 颗独立 RGB 灯珠的承载条。
- `exports/window_lens.stl`：封闭主板观察窗的透明 PETG 镜片；追求清晰度时优先使用亚克力片。
- `tools/generate_stl.py`：无 GUI 环境下的可重复 STL 导出脚本。
- `print/PRINT_PLAN.md`：切片、打印顺序和验收记录模板。

## 设计基准

- 两块面板尺寸：120 × 95 mm。
- 按键间距：19.05 mm。
- MX 轴孔初始尺寸：14.0 mm。
- 上盖厚度：3 mm。
- 下层盒体底板厚度：2.4 mm；盒体高度 16 mm，和 3 mm 上层控制盖装配后总高约 19 mm。
- Arduino Micro 按 35 × 18 × 10 mm 平放，卡槽左右各留 0.6 mm，侧向导轨和后挡块防止主板移动。
- Type-C 插口位于下层盒体前墙，开口约 14 × 9 mm；上层控制盖不再承担 USB 插座受力。
- EC11 使用立式/垂直轴安装，轴线垂直于 3 mm 上层面板；本模型不兼容卧式/侧插编码器。
- 按照片中的小型 EC11 优化为圆形约 6.2 mm 轴孔，适配标称 6 mm 轴，不再使用偏大的方形窗口。
- 上层控制盖右侧保留 24 × 50 mm 主板透明观察窗；透明片改为 25.4 × 51.4 × 1.5 mm，从下方压住窗口边缘，完成封闭。
- 固定方式：M3 螺丝 + 热熔铜螺母。
- 面板 quota RGB 灯：12 个独立窗口，间距 5.3 mm。

这些数值是 Rev 0.9.4 的首件打印基准。主控必须实测为 35 × 18 × 10 mm；不同 USB-C 插座位置的兼容板不能直接套用，先打印公差件和下层盒体做干涉确认。

## 导出

在 OpenSCAD 顶部修改：

```scad
part = "plate";     // plate / bottom / controller_panel / assembly / tolerance / pixel_carrier
```

按 `F6` 渲染后导出 STL。当前 Rev 0.9.4 的 STL 已提交到 `mechanical/exports/`，方便直接下载和导入切片器。为兼容原有链接，`plate.stl` 表示上层控制盖，`bottom.stl` 表示下层封闭盒体。

如果 OpenSCAD 命令行不可用，可安装脚本依赖后执行：

```bash
python3 -m venv /tmp/13key-cad-venv
. /tmp/13key-cad-venv/bin/activate
pip install -r mechanical/tools/requirements.txt
python mechanical/tools/generate_stl.py --part all
```

脚本生成的模型与当前 Rev 0.9.4 的 OpenSCAD 参数保持一致；修改尺寸时需要同步检查两个源文件。
