.PHONY: check python-check files

check: python-check files

python-check:
	python3 -m py_compile host/codexd/codexd.py

files:
	@test -f README.md
	@test -f mechanical/cad/codexpad.scad
	@test -f hardware/wiring/pinout.md
	@test -f firmware/arduino/codexpad_mvp/codexpad_mvp.ino
	@test -f host/codexd/codexd.py
	@echo "project files: ok"
