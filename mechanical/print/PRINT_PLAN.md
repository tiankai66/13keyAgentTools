# 打印计划

## Bambu Studio 快速开始

当前可打印文件：

- `../exports/tolerance_coupon.stl`：先打印，用来确定轴孔和 M3 热熔螺母公差。
- `../exports/plate.stl`：定位板。
- `../exports/bottom.stl`：底壳。

将 STL 拖入 Bambu Studio 后，先按实际材料选择 PLA 或 PETG 配置，再切片预览。当前文件只包含几何模型，不包含机器专用的 3MF 工程、耗材配置或 G-code。

建议首轮参数：0.4 mm 喷嘴、0.20 mm 层高、3 道墙、15～25% 填充；定位板和公差件平放打印，底壳底面朝打印床。

## 第 1 批：公差件

在 `mechanical/cad/agent_macro.scad` 中设置：

```scad
part = "tolerance";
```

打印后测试：

- 轴体能否插入和拔出
- 键帽是否会顶住定位板
- EC11 轴杆和旋钮孔是否同心
- 摇杆帽是否能活动
- M3 铜螺母孔是否过松或过紧

## 第 2 批：主体

```scad
part = "plate";
part = "bottom";
```

推荐初始切片参数：

- 材料：PLA 或 PETG
- 喷嘴：0.4 mm
- 层高：0.16～0.20 mm
- 墙数：3
- 顶底层：4
- 填充：15～25%
- 外壳打印方向：底面朝打印床

## 验收

- 上盖不翘曲
- 13 个轴体均能垂直安装
- USB 线可以插拔且不拉扯 Arduino Micro
- 底壳不压住焊点和导线
- 两个旋钮、摇杆、触摸窗口操作不干涉
- 前侧 12 个灯窗与独立 RGB 灯像素位置对齐
