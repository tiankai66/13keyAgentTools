.PHONY: check python-check files cad-export

check: python-check files

cad-export:
	python3 mechanical/tools/generate_stl.py --part all

python-check:
	python3 -m py_compile host/agentd/agentd.py mechanical/tools/generate_stl.py

files:
	@test -f README.md
	@test -f mechanical/cad/agent_macro.scad
	@test -f hardware/wiring/pinout.md
	@test -f firmware/arduino/agent_macro_mvp/agent_macro_mvp.ino
	@test -f host/agentd/agentd.py
	@test -f mechanical/tools/generate_stl.py
	@echo "project files: ok"
