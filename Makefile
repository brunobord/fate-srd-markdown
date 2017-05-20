PORT=8080

help:
	@echo "Help on targets"
	@echo ""
	@echo " * build: build stuff"
	@echo " * clean: clean directories"
	@echo " * serve: serve markdown directories using Caddy web server"
	@echo " * html-clean: clean HTML directories"
	@echo " * html-build: build HTML pages out of the existing Markdown content"

build:
	tox -- pages indexes

clean:
	rm -Rf markdown/

static:
	mkdir -p markdown/static/
	cp static/*.* markdown/static/

serve: static
	caddy -conf Caddyfile

html-clean:
	rm -Rf docs/

html-build:
	tox -e html

html-serve:
	mkdir -p docs/static/
	cp static/*.* docs/static/
	cd docs/; python3 -m http.server $(PORT)

.PHONY: help build clean static serve html-build html-clean html-serve
