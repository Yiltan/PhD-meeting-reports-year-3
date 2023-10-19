PDF_READER='zathura'
SPELL_LANG='en_GB'

OUT_DIR=out
FILE=$(shell ls Pre*.tex)
PDF=$(OUT_DIR)/$(shell ls out/ | grep pdf)

all : $(FILE)
	rm -f *.bak *.swp
	latexmk -pdf -outdir=$(OUT_DIR) -r .latexmkrc $(FILE)

clean :
	rm $(OUT_DIR)/*

open : all $(PDF)
	nohup $(PDF_READER) $(PDF) > /dev/null &

spell :
	aspell -d $(SPELL_LANG) --mode=tex -c $(FILE)

opt : all $(PDF)
	./optfile $(PDF)
