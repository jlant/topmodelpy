.PHONY: clean clean-pyc

help:
	@echo "clean - remove all test and Python artifacts"
	@echo "clean-pyc - remove Python file artifacts"

clean: clean-pyc 

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;
	find . -name '__pycache__' -exec rm -fr {} \;


