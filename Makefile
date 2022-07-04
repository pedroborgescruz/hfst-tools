PREFIX ?= ~
install:
	@install -d $(DESTDIR)$(PREFIX)/bin
	install -m755 morph-test/morph-test.py $(DESTDIR)$(PREFIX)/bin/morph-test
	install -m755 morphTests2yaml.py $(DESTDIR)$(PREFIX)/bin/morphTests2yaml
	install -m755 lexccounter.py $(DESTDIR)$(PREFIX)/bin/lexccounter
	install -m755 apertium-eval-translator/apertium-eval-translator-line.pl $(DESTDIR)$(PREFIX)/bin/apertium-eval-translator-line
	install -m755 scrapeTransferTests.py $(DESTDIR)$(PREFIX)/bin/scrapeTransferTests
	install -m755 precisionRecall.py $(DESTDIR)$(PREFIX)/bin/precisionRecall
	install -m755 coverage-hfst.sh $(DESTDIR)$(PREFIX)/bin/coverage-hfst
