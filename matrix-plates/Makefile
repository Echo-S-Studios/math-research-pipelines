PY ?= python3

.PHONY: help test verify demo histogram export clean dist

help:
	@echo "make test        - run the full unittest suite (stdlib only; sympy/node checks skip if absent)"
	@echo "make verify      - run the build-spec verification checklist (Goal 1 + Goal 2)"
	@echo "make demo        - print the phi (+) phi similarity-class demonstration"
	@echo "make histogram   - print the ASCII Mahler spectrum for the seed batch"
	@echo "make export       - write spectrum + gallery HTML/SVG to ./.build"
	@echo "make clean        - remove build artifacts"

test:
	cd $(CURDIR) && PYTHONPATH=src $(PY) -m unittest discover -s tests -v

verify:
	PYTHONPATH=src $(PY) -m matrix_plates.cli verify

demo:
	PYTHONPATH=src $(PY) -m matrix_plates.cli demo

histogram:
	PYTHONPATH=src $(PY) -m matrix_plates.cli histogram --mode spectrum

export:
	mkdir -p .build
	PYTHONPATH=src $(PY) -m matrix_plates.cli histogram --mode spectrum --svg .build/spectrum.svg --html .build/spectrum.html
	PYTHONPATH=src $(PY) -m matrix_plates.cli export --html .build/gallery.html
	@echo "wrote .build/spectrum.svg .build/spectrum.html .build/gallery.html"

clean:
	rm -rf .build dist build src/*.egg-info **/__pycache__ .pytest_cache
