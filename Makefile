.PHONY: help setup clean pep8 tests run

# Version package
VERSION=$(shell python -c 'import globomap_auth_manager; print(globomap_auth_manager.__version__)')

PROJECT_HOME = "`pwd`"

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Install project dependencies
	@pip install -r $(PROJECT_HOME)/requirements_test.txt

clean: ## Clear *.pyc files, etc
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

pep8: ## Check source-code for PEP8 compliance
	@-pep8 globomap_auth_manager

exec_tests: clean pep8 ## Run all tests with coverage
	@python3.6 -m unittest discover -s tests/
	#@run --source=globomap_auth_manager -m unittest2 discover -s tests/; coverage report -m

tests:
	@docker exec -it globomap_auth_manager make exec_tests

dist: clean
	@python setup.py sdist

publish: clean dist
	@echo 'Ready to release version ${VERSION}? (ctrl+c to abort)' && read
	twine upload dist/*
	@git tag ${VERSION}
	@git push --tags