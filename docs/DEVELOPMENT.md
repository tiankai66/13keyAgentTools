# 开发与迭代流程

## 分支

- `main`：可复现、可使用的版本。
- `agent/<topic>`：每个独立功能或硬件改版。
- 机械、硬件、固件尽量使用不同分支，减少互相覆盖。

## 提交信息

采用简短前缀：

```text
mech: adjust switch cutout tolerance
hw: add encoder wiring revision
fw: debounce matrix keys
host: add serial LED demo
docs: record Rev 0.2 test result
```

## 每次迭代必须记录

- 改了什么
- 为什么改
- 使用的材料或器件
- 测试方法
- 通过/失败结果
- 下一步动作

## 硬件安全

- 焊接或改线前拔掉 USB。
- RGB 供电必须和 Arduino Micro 共地。
- 不要把 LED 大电流直接从 3.3V 供电。
- Accept / Reject 等有副作用的动作使用长按或二次确认。
