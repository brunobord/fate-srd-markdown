# FATE SRD (raw) document

Extracted from https://fate-srd.com/ - converted into markdown.

The FATE SRD is published under the terms of the [CC-BY License](https://creativecommons.org/licenses/by/3.0/).

## Available SRDs

* Fate Core,
* Fate Accelerated,
* Fate System Toolkit.

## Setup

* A working Python3 environment.
* [tox](https://tox.readthedocs.io/en/latest/) to create a complete virtualenv and run the builder.
* Or, alternatively, you can use a plain virtualenv to run the builder.
* To browse the SRD without converting it into HTML, you can use [caddy](https://caddyserver.com/) that directly converts Markdown into web pages.

## Build

```
make build
```

## Serve

```
make serve
```

# TODO

- [ ] Problems with some bad emphasis (``_my emphasis _. hello``)
