.PHONY = test

test:
	python -m tests.shuntingyard_test -v

coverage:
	coverage run -m pytest 
	coverage report
	coverage html
