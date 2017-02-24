test:
	@python ovp_users/tests/runtests.py

lint:
	@pylint ovp_users

clean-pycache:
	@rm -r **/__pycache__

clean: clean-pycache

.PHONY: clean


