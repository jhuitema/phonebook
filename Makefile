.PHONY: help lint format venv dev doc show-doc test unit integration dist dist-doc clean


SHELL := bash
PROJECT := Phonebook
VERSION := $(shell cat VERSION)

# test information
HTML_COV := htmlcov/index.html

# doc information
HTML_DOC := docs/build/index.html
RELNOTES_DOC := docs/source/release_notes.rst
RELNOTES_FILE := release_notes.rst

help:  ## Describe all available make commands
	@echo ""
	@echo "Please use 'make <target>' where <target> is one of:"
	@grep -E '^[a-zA-Z_\(\)\$$[:space:]-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sed -r 's/[[:space:]]*\$$\([a-zA-Z_-]+\)//' | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

check:  ## Check for any Python lint errors
	@printf "\n\033[36m--- $@: Checking For Fatal Errors ---\033[0m\n"
	tox -e lint

lint:  ## Lint the source code and output the results
	@printf "\n\033[36m--- $@: Checking For Style Errors ---\033[0m\n"
	LINT=--exit-zero tox -e lint

format:  ## Autoformat the source code using Black
	@printf "\n\033[36m--- $@: Fixing Whitespace Style Errors ---\033[0m\n"
	DO_FORMAT= tox -e format

venv:  ## Create a local virtualenv and develop install
	@printf "\n\033[36m--- $@: Creating Local virtualenv '.venv' ---\033[0m\n"
	python3 -m virtualenv .venv
	.venv/bin/pip install -e .

dev: venv  ## Create a virutalenv and enter it
	@printf "\n\033[36m--- $@: Sourcing Local virtualenv in New Bash Shell ---\033[0m\n"
	bash --rcfile <(echo 'test -f ~/.bashrc && source ~/.bashrc; source .venv/bin/activate') || true

doc $(HTML_DOC):  ## Generate the documentation
	@printf "\n\033[36m--- $@: Adding Release Notes to Documentation ---\033[0m\n"
ifneq ($(wildcard $(RELNOTES_DOC)),)
	rm $(RELNOTES_DOC)
endif
	printf ".. _relnotes:\n\n" > $(RELNOTES_DOC)
	printf "#############\n" >> $(RELNOTES_DOC)
	printf "Release Notes\n" >> $(RELNOTES_DOC)
	printf "#############\n" >> $(RELNOTES_DOC)
ifneq ($(wildcard $(RELNOTES_FILE)),)
	@# Copy all but the header from the RELNOTES_FILE into the doc file
	printf "\n`cat $(RELNOTES_FILE) | tail -n +4`" >> $(RELNOTES_DOC)
endif
	echo "" >> $(RELNOTES_DOC)

	@printf "\n\033[36m--- $@: Generating Documentation ---\033[0m\n"
	DO_BUILD= tox -e doc

show-doc: $(HTML_DOC)  ## Display generated documentation
	@printf "\n\033[36m--- $@: Displaying Documentation ---\033[0m\n"
	xdg-open ./docs/_build/index.html

test:  ## Run the package tests
	@printf "\n\033[36m--- $@: Running Tests ---\033[0m\n"
	tox

unit:  ## Run the package unit tests
	@printf "\n\033[36m--- $@: Running Unit Tests ---\033[0m\n"
	tox -e py37 -- tests/unit

integration:  ## Run the package integration tests
	@printf "\n\033[36m--- $@: Running Integration Tests ---\033[0m\n"
	tox -e py37 -- tests/integration

cov: $(HTML_COV)  # Display the coverage report for the tests
	@printf "\n\033[36m--- $@: Displaying Coverage Report ---\033[0m\n"
	xdg-open $(HTML_COV) &

dist: check dist-doc  ## Distribute the package
	@printf "\n\033[36m--- $@: Distributing Package ---\033[0m\n"
	git tag v$(VERSION)
	git push origin v$(VERSION)

dist-doc: check doc  ## Distribute the package documentation
	@printf "\n\033[36m--- $@: Distributing Documentation ---\033[0m\n"
	@echo "$@ is not yet implemented!"

clean:  ## Remove temporary files
	@printf "\n\033[36m--- $@: Cleaning Package Directory ---\033[0m\n"
	git clean -Xdf
