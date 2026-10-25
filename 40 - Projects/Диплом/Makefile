.DEFAULT_GOAL := diploma

MD2GOST ?= $(HOME)/md2gost/.venv/bin/md2gost
SOURCE := Диплом_ГОСТ.md
OUTPUT ?= build/Диплом_ГОСТ.docx

.PHONY: diploma help

diploma:
	@test -x "$(MD2GOST)" || { echo "Не найден md2gost: $(MD2GOST). Задайте MD2GOST=/путь/к/md2gost" >&2; exit 1; }
	@mkdir -p "$(dir $(OUTPUT))"
	"$(MD2GOST)" convert "$(SOURCE)" --no-title-page -o "$(OUTPUT)"

help:
	@echo 'make diploma  — собрать build/Диплом_ГОСТ.docx без финальной вёрстки LibreOffice'
	@echo 'make diploma OUTPUT=/tmp/diploma.docx — собрать в другой файл'
	@echo 'make diploma MD2GOST=/путь/к/md2gost — указать другой конвертер'
