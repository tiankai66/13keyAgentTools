# 3D 打印建模

当前使用 OpenSCAD 做参数化 Rev 0.4。先打印公差件，再打印定位板和底壳；不要在没有装入实际轴体、EC11 和 RGB 灯前锁定外壳尺寸。

## 文件

- `cad/agent_macro.scad`：定位板、底壳、装配预览和公差件。
- `exports/`：可直接导入 Bambu Studio、PrusaSlicer 或 Cura 的 STL 文件。
- `exports/pixel_carrier.stl`：固定 12 颗独立 RGB 灯珠的承载条。
- `tools/generate_stl.py`：无 GUI 环境下的可重复 STL 导出脚本。
- `print/PRINT_PLAN.md`：切片、打印顺序和验收记录模板。

## 设计基准

- 外壳初始尺寸：120 × 100 mm。
- 按键间距：19.05 mm。
- MX 轴孔初始尺寸：14.0 mm。
- 上盖厚度：3 mm。
- 底壳高度：24 mm，内部增加 Arduino Micro 承托架。
- 固定方式：M3 螺丝 + 热熔铜螺母。
- 面板 quota RGB 灯：12 个独立窗口，间距 5.3 mm。

这些数值是 Rev 0.5 的可打印起点，不是最终量产尺寸。

## 导出

在 OpenSCAD 顶部修改：

```scad
part = "plate";     // plate / bottom / assembly / tolerance / pixel_carrier
```

按 `F6` 渲染后导出 STL。当前 Rev 0.5 的 STL 已提交到 `mechanical/exports/`，方便直接下载和导入切片器。

如果 OpenSCAD 命令行不可用，可安装脚本依赖后执行：

```bash
python3 -m venv /tmp/13key-cad-venv
. /tmp/13key-cad-venv/bin/activate
pip install -r mechanical/tools/requirements.txt
python mechanical/tools/generate_stl.py --part all
```

脚本生成的模型与当前 Rev 0.5 的 OpenSCAD 参数保持一致；修改尺寸时需要同步检查两个源文件。
