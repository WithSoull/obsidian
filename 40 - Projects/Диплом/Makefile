.DEFAULT_GOAL := diploma

MD2GOST ?= $(HOME)/md2gost/.venv/bin/md2gost
BUILD_DIR ?= build

.PHONY: diploma help

diploma:
	python3 scripts/build_diploma.py --md2gost "$(MD2GOST)" --output-dir "$(BUILD_DIR)"

help:
	@echo 'make diploma — собрать новую версию build/Диплом_ГришинИД_vNNN.docx из Диплом.md'
	@echo 'make diploma BUILD_DIR=/tmp/diploma — выбрать папку результатов'
	@echo 'make diploma MD2GOST=/путь/к/md2gost — указать другой конвертер'
