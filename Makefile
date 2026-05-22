# Build the paper.
#
# Primary toolchain: tectonic (single-binary LaTeX engine, self-contained,
# fetches packages on demand). Install: `brew install tectonic`.
#   tectonic does NOT provide pdflatex/latexmk — if you search for those and
#   find nothing, you still have a working LaTeX toolchain via tectonic.
#
# Fallback toolchain: latexmk + a full TeX distribution (TeX Live / MacTeX).

PAPER_DIR := paper
MAIN      := main

.PHONY: all tectonic latexmk watch clean

all: tectonic

tectonic:
	cd $(PAPER_DIR) && tectonic $(MAIN).tex

# Fallback if a classic TeX distribution is installed instead of tectonic.
latexmk:
	cd $(PAPER_DIR) && latexmk -pdf -interaction=nonstopmode -halt-on-error $(MAIN).tex

watch:
	cd $(PAPER_DIR) && tectonic --watch $(MAIN).tex

clean:
	cd $(PAPER_DIR) && rm -f *.aux *.bbl *.blg *.log *.out *.toc *.run.xml *.synctex.gz $(MAIN).pdf
