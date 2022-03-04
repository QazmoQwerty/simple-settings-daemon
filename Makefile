.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[1m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: lint
lint: ## Run mypy
	mypy -m libssettings.scripts.main

.PHONY: test
test: ## Run a sanity test
	python3 -m libssettings.scripts.main /tmp/test_ssettings_socket --verbose

.PHONY: build
build: ## Build the .whl file
	python3 -m build

.PHONY: install
install: ## Install the .whl file
	python3 -m pip install --force-reinstall dist/simplesettingsdaemon*.whl

.PHONY: upload
upload: ## Upload to pypi
	python3 -m twine upload dist/*

.PHONY: build-docs
build-docs: ## Generate manpage
	pandoc -s -t man docs/manpage.md -o docs/ssettings.1

.PHONY: install-docs
install-docs: ## Install manpage
	sudo bash -c "cat docs/ssettings.1 | gzip > /usr/local/man/man1/ssettings.1"
	sudo bash -c "ln -f /usr/local/man/man1/ssettings.1 /usr/local/man/man1/ssettingsd.1"

.PHONY: clean
clean: ## Clean generated files
	-rm -rf dist ssettings.egg-info/ .mypy_cache/ dist/ __pycache__/