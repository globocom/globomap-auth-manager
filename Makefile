.PHONY: help setup clean pep8 tests run

# Version package
VERSION=$(shell python -c 'import globomap_auth_manager; print(globomap_auth_manager.__version__)')

PROJECT_HOME = "`pwd`"

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo

	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Install project dependencies
	@pip install -r $(PROJECT_HOME)/requirements_test.txt

clean: ## Clear *.pyc files, etc
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

tests: clean setup ## Make tests
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_auth_manager --with-coverage; coverage report -m

tests_ci: clean setup ## Make tests to CI
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_auth_manager

dist: clean ## Make dist
	@python setup.py sdist

publish: clean dist ## Make publish
	@echo 'Ready to release version ${VERSION}? (ctrl+c to abort)' && read
	twine upload dist/*
	@git tag ${VERSION}
	@git push --tags
