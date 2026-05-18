# Build the paper. Requires latexmk + a TeX distribution.

PAPER_DIR := paper
MAIN      := main

.PHONY: all watch clean

all:
	cd $(PAPER_DIR) && latexmk -pdf -interaction=nonstopmode -halt-on-error $(MAIN).tex

watch:
	cd $(PAPER_DIR) && latexmk -pdf -pvc -interaction=nonstopmode $(MAIN).tex

clean:
	cd $(PAPER_DIR) && latexmk -C
	cd $(PAPER_DIR) && rm -f *.bbl *.run.xml *.synctex.gz
