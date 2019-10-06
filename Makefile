.PHONY: tests


# Development

dependencies:
	poetry install


# Testing

e2e-tests: export DATASTORE_EMULATOR_HOST=0.0.0.0:8081
e2e-tests:
	poetry run py.test tests/e2e

unit-tests:
	poetry run py.test tests/unit

legacy-tests: export DATASTORE_EMULATOR_HOST=0.0.0.0:8081
legacy-tests:
	poetry run py.test tests/legacy

tests: unit-tests legacy-tests e2e-tests

coverage:  export DATASTORE_EMULATOR_HOST=0.0.0.0:8081
coverage:
	poetry run py.test --cov=datastorm --cov-branch --cov-fail-under=90 --cov-report=html tests


# Static analysis

lint:
	poetry run flake8 datastorm --max-line-length=120
	poetry run flake8 tests --max-line-length=120

# Docs

docs:
	mkdocs serve

# Packaging

build: tests lint
	poetry build

publish: build
	poetry publish


# Docker

docker-build:
	docker build -t datastorm-test-env:255.0.0-3.6.9 .circleci/images

docker-run: docker-build
	docker run --rm --name datastorm-test-env --publish 8081:8081 datastorm-test-env:255.0.0-3.6.9

docker-tag:
	docker tag datastorm-test-env:255.0.0-3.6.9 javierluna/datastorm-test-env:255.0.0-3.6.9

docker-push: docker-build docker-tag
	docker push javierluna/datastorm-test-env

docker-clean:
	-docker stop datastore-test-env
	-docker rm datastore-test-env

docker-tests: docker-build
	docker run --rm -d --name datastore-test-env --publish 8081:8081 datastorm-test-env:255.0.0-3.6.9
	sleep 5
	$(MAKE) tests
