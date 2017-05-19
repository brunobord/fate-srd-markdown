help:
	@echo "Help on targets"
	@echo ""
	@echo " * build: build stuff"
	@echo " * clean: clean directories"
	@echo " * serve: serve markdown directories using Caddy web server"

build:
	tox -- pages indexes

clean:
	rm -Rf markdown/

static:
	mkdir -p markdown/static/
	cp static/*.* markdown/static/

serve: static
	caddy -conf Caddyfile

.PHONY: help build clean static serve
