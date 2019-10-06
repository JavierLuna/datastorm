.PHONY: tests

e2e-tests: export DATASTORE_EMULATOR_HOST=0.0.0.0:8081
e2e-tests:
	pipenv run py.test tests/e2e

unit-tests:
	pipenv run py.test tests/unit

legacy-tests: export DATASTORE_EMULATOR_HOST=0.0.0.0:8081
legacy-tests:
	pipenv run py.test tests/legacy

tests: unit-tests legacy-tests e2e-tests

coverage:
	PYTHONPATH=. coverage run --source datastorm setup.py test
	coverage html
	coverage report -m

docker-build:
	docker build -t datastorm-test-env:255.0.0-3.6.9 .circleci/images

docker-run: docker-build
	docker run --rm --name datastorm-test-env --publish 8081:8081 datastorm-test-env:255.0.0-3.6.9

docker-tag:
	docker tag datastorm-test-env:255.0.0-3.6.9 javierluna/datastorm-test-env:255.0.0-3.6.9

docker-push: docker-build docker-tag
	docker push javierluna/datastorm-test-env

docker-clean:
	docker stop datastore-test-env
	docker rm datastore-test-env

docker-tests: docker-build
	docker run --rm -d --name datastore-test-env --publish 8081:8081 datastorm-test-env:255.0.0-3.6.9
	sleep 5
	$(MAKE) tests


clean:
	rm -rf build
	rm -rf datastorm.egg-info
	rm -rf dist
	rm -rf htmlcov
	rm .coverage

upload:
	python setup.py bdist_wheel
	twine upload dist/*
