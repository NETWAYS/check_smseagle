.PHONY: lint-check test-check coverage-check lint-notify test-notify coverage-notify

lint-check:
	python -m pylint check_smseagle.py

test-check:
	python -m unittest -v -b test_check_smseagle.py

coverage-check:
	python -m coverage run -m unittest test_check_smseagle.py
	python -m coverage report -m --include check_smseagle.py

lint-notify:
	python -m pylint notify_smseagle.py

test-notify:
	python -m unittest -v -b test_notify_smseagle.py

coverage-notify:
	python -m coverage run -m unittest test_notify_smseagle.py
	python -m coverage report -m --include notify_smseagle.py
