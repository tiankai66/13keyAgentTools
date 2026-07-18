# 3D 打印建模

当前使用 OpenSCAD 做参数化初稿。先打印公差件，再打印定位板和底壳；不要在没有装入实际轴体、EC11 和摇杆前锁定外壳尺寸。

## 文件

- `cad/agent_macro.scad`：定位板、底壳、装配预览和公差件。
- `print/PRINT_PLAN.md`：切片、打印顺序和验收记录模板。

## 设计基准

- 外壳初始尺寸：148 × 106 mm。
- 按键间距：19.05 mm。
- MX 轴孔初始尺寸：14.0 mm。
- 上盖厚度：3 mm。
- 底壳高度：18 mm。
- 固定方式：M3 螺丝 + 热熔铜螺母。

这些数值是 Rev 0.1 的可打印起点，不是最终量产尺寸。

## 导出

在 OpenSCAD 顶部修改：

```scad
part = "plate";     // plate / bottom / assembly / tolerance
```

按 `F6` 渲染后导出 STL。导出的 STL 不提交到 Git，建议保存在本地 `mechanical/exports/`。
