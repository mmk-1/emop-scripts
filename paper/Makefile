NAME := main
TEXS := $(wildcard *.tex)
TABLES := $(wildcard tables/*.tex)
NUMBERS := $(wildcard numbers/*.tex)
PLOTS := $(wildcard data/plots/*.eps)
CODE := $(wildcard code/*.java)
BIBS := $(wildcard *.bib)

%.pdf: %.fig 
	fig2dev -L eps -f Roman $*.fig >$*.eps

all: ${NAME}.pdf

${NAME}.pdf: ${TEXS} ${TABLES} ${NUMBERS} ${BIBS} ${CODE} ${PLOTS}
	-latex $(NAME)
	-bibtex $(NAME)
	-latex $(NAME)
	-latex $(NAME)
	@echo '****************************************************************'
	@dvips -t letter -o $(NAME).ps $(NAME).dvi
	@ps2pdf -dPDFSETTINGS=/prepress $(NAME).ps $(NAME).pdf
	@echo '******** Did you spell-check the paper? ********'

clean:
	ls $(NAME)* | grep -v ".tex" | grep -v ".bib" | xargs rm -f
	rm -f *.bak *~
