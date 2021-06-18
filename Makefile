.PHONY = test

test:
	python -m tests.shuntingyard_test -v

coverage:
	coverage run --source simplicio/ --branch -m pytest 
	coverage html
