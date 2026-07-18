# USB CDC 状态协议 Rev 0.2

Arduino Micro 的 `Serial` 对象对应 USB CDC 虚拟串口。每条命令以换行结束。

## 设置单颗灯

```text
LED <index> <red> <green> <blue>
```

例如：

```text
LED 0 0 64 255
```

## 清除全部灯

```text
CLEAR
```

## 设置剩余用量条

```text
QUOTA <percent>
```

例如：

```text
QUOTA 42
```

当前 Rev 0.2 使用前侧 12 颗灯作为当前 Agent 的剩余用量条：0% 全灭，100% 全亮。颜色按剩余量显示为红色、黄色或绿色；后续可扩展为多个 Agent 分段显示。

## 设计边界

- 本协议只控制硬件灯光，不负责批准或拒绝 Agent 操作。
- 各 Agent 的状态适配器应放在主机端，不应把 API 密钥或业务逻辑写进 MCU。
- 后续如果 USB CDC 延迟或带宽不足，再迁移到 Raw HID；硬件引脚不需要改变。
