SPHINXBUILD   = sphinx-build
BUILDDIR      = _build

html:
	$(SPHINXBUILD) -b html -d $(BUILDDIR)/doctrees . $(BUILDDIR)/html

serve:
	cd $(BUILDDIR)/html && python3.6 -m http.server --bind 127.0.0.1 4000
