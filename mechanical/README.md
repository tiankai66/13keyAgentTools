# 3D 打印建模

当前使用 OpenSCAD 做参数化 Rev 0.2。先打印公差件，再打印定位板和底壳；不要在没有装入实际轴体、两个 EC11、摇杆和灯带前锁定外壳尺寸。

## 文件

- `cad/agent_macro.scad`：定位板、底壳、装配预览和公差件。
- `exports/`：可直接导入 Bambu Studio、PrusaSlicer 或 Cura 的 STL 文件。
- `tools/generate_stl.py`：无 GUI 环境下的可重复 STL 导出脚本。
- `print/PRINT_PLAN.md`：切片、打印顺序和验收记录模板。

## 设计基准

- 外壳初始尺寸：184 × 112 mm。
- 按键间距：19.05 mm。
- MX 轴孔初始尺寸：14.0 mm。
- 上盖厚度：3 mm。
- 底壳高度：18 mm。
- 固定方式：M3 螺丝 + 热熔铜螺母。
- 中心指托：直径 36 mm，中心凸点直径 6 mm，高度约 2.2 mm。
- 前侧 quota 灯带：12 个窗口，间距 12.5 mm。

这些数值是 Rev 0.2 的可打印起点，不是最终量产尺寸。

## 导出

在 OpenSCAD 顶部修改：

```scad
part = "plate";     // plate / bottom / assembly / tolerance
```

按 `F6` 渲染后导出 STL。当前 Rev 0.2 的 STL 已提交到 `mechanical/exports/`，方便直接下载和导入切片器。

如果 OpenSCAD 命令行不可用，可安装脚本依赖后执行：

```bash
python3 -m venv /tmp/13key-cad-venv
. /tmp/13key-cad-venv/bin/activate
pip install -r mechanical/tools/requirements.txt
python mechanical/tools/generate_stl.py --part all
```

脚本生成的模型与当前 Rev 0.2 的 OpenSCAD 参数保持一致；修改尺寸时需要同步检查两个源文件。
