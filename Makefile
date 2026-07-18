.PHONY: check python-check files

check: python-check files

python-check:
	python3 -m py_compile host/agentd/agentd.py

files:
	@test -f README.md
	@test -f mechanical/cad/agent_macro.scad
	@test -f hardware/wiring/pinout.md
	@test -f firmware/arduino/agent_macro_mvp/agent_macro_mvp.ino
	@test -f host/agentd/agentd.py
	@echo "project files: ok"
