# agentd：多 Agent 主机端状态测试工具

当前版本只负责验证 Arduino Micro 的 USB CDC 串口和 RGB 协议，不直接读取某一个 Agent 的状态。后续可以将 Codex CLI、Claude Code、Qoder 或其他 coding agent 的 hooks、CLI 事件或桌面自动化适配到同一个协议。

## 安装

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r host/agentd/requirements.txt
```

## 使用

列出串口：

```bash
python host/agentd/agentd.py --list
```

交互控制：

```bash
python host/agentd/agentd.py --port /dev/cu.usbmodemXXXX
```

输入：

```text
LED 0 thinking
LED 1 running
LED 2 waiting
LED 3 done
CLEAR
```

自动灯效演示：

```bash
python host/agentd/agentd.py --port /dev/cu.usbmodemXXXX --demo
```

颜色协议：

| 状态 | 颜色 |
|---|---|
| idle | 白色 |
| thinking | 蓝色 |
| running | 紫色 |
| waiting | 黄色 |
| done | 绿色 |
| error | 红色 |
