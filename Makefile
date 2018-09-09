.PHONY: test

test:
	python -m unittest discover tests/

coverage:
	PYTHONPATH=. coverage run --source datastorm setup.py test
	coverage html
	coverage report -m

clean:
	rm -rf build
	rm -rf datastorm.egg-info
	rm -rf dist
	rm -rf htmlcov
	rm .coverage

upload:
	python setup.py bdist_wheel
	twine upload dist/*
