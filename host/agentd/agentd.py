#!/usr/bin/env python3
"""Small USB CDC RGB test bridge for a multi-agent macro keyboard."""

from __future__ import annotations

import argparse
import sys
import time
from typing import Iterable


COLORS = {
    "idle": (32, 32, 32),
    "thinking": (0, 64, 255),
    "running": (160, 0, 255),
    "waiting": (255, 160, 0),
    "done": (0, 200, 64),
    "error": (255, 0, 0),
}


def load_serial():
    try:
        import serial
        from serial.tools import list_ports
    except ImportError as exc:
        raise SystemExit(
            "pyserial is required; run: pip install -r host/agentd/requirements.txt"
        ) from exc
    return serial, list_ports


def print_ports() -> int:
    _, list_ports = load_serial()
    ports = list(list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return 0
    for port in ports:
        description = port.description or "unknown device"
        print(f"{port.device}\t{description}")
    return 0


def rgb_command(index: int, state: str) -> str:
    try:
        red, green, blue = COLORS[state]
    except KeyError as exc:
        valid = ", ".join(COLORS)
        raise ValueError(f"unknown state {state!r}; use one of: {valid}") from exc
    return f"LED {index} {red} {green} {blue}\n"


def send(ser, line: str) -> None:
    ser.write(line.encode("ascii"))
    ser.flush()
    print(f"> {line.rstrip()}" )


def demo_commands(count: int) -> Iterable[str]:
    states = list(COLORS)
    for offset in range(len(states)):
        for index in range(count):
            state = states[(index + offset) % len(states)]
            yield rgb_command(index, state)
        yield "CLEAR\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="list serial ports")
    parser.add_argument("--port", help="serial port, for example /dev/cu.usbmodemXXXX")
    parser.add_argument("--demo", action="store_true", help="run a six-state RGB demo")
    parser.add_argument("--count", type=int, default=6, help="number of RGB LEDs in demo")
    args = parser.parse_args()

    if args.list:
        return print_ports()
    if not args.port:
        parser.error("--port is required unless --list is used")

    serial, _ = load_serial()
    with serial.Serial(args.port, 115200, timeout=0.2) as ser:
        time.sleep(0.5)
        if args.demo:
            for line in demo_commands(max(1, args.count)):
                send(ser, line)
                time.sleep(0.35)
            return 0

        print("Enter `LED <index> <state>`, `CLEAR`, or `quit`.")
        for raw_line in sys.stdin:
            line = raw_line.strip()
            if line.lower() in {"quit", "exit"}:
                break
            if line.upper() == "CLEAR":
                send(ser, "CLEAR\n")
                continue
            parts = line.split()
            if len(parts) != 3 or parts[0].upper() != "LED":
                print("Format: LED <index> <state>")
                continue
            try:
                send(ser, rgb_command(int(parts[1]), parts[2].lower()))
            except (ValueError, IndexError) as exc:
                print(exc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
