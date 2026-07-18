# Arduino Micro MVP 固件

这是 Rev 0.1 的 Arduino IDE 固件，不依赖定制 PCB。

## 上传

1. 安装 Arduino IDE。
2. 打开 `agent_macro_mvp.ino`。
3. 选择 `Tools > Board > Arduino Micro`。
4. 选择对应串口并上传。
5. 如果上传时端口消失，快速按两次 Arduino Micro 的 Reset，再选择 Bootloader 端口。

## 当前行为

- A：Enter / Accept
- B：Esc / Reject
- C：Ctrl+N / New Chat
- D：Ctrl+Shift+D / Push-to-talk
- E～M：F1～F9，留给主机端工作流映射
- 旋钮：F11/F12，留给 reasoning level 映射
- 触摸：F10，切换 Layer
- 摇杆：F1～F4，分别代表 Review、Debug、Refactor、Test

这些快捷键是 MVP 占位符。不同 Agent 终端的实际快捷键应在主机端确认后再固化，固件本身保持通用 HID 宏键盘定位。

## RGB

默认 `ENABLE_RGB` 为 `0`，这样可以先不安装 RGB 库和灯珠测试输入。

需要灯光时：

1. 安装 Arduino Library Manager 中的 `Adafruit NeoPixel`。
2. 将 `ENABLE_RGB` 改为 `1`。
3. 将 `RGB_COUNT` 改为实际灯珠数量。
4. 使用 `host/agentd/agentd.py` 发送 `LED` 命令。
