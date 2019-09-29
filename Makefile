.PHONY: test

test: export DATASTORE_EMULATOR_HOST=0.0.0.0:8081
test:
	python -m unittest discover tests/

coverage:
	PYTHONPATH=. coverage run --source datastorm setup.py test
	coverage html
	coverage report -m

docker-build:
	docker build -t datastorm-test-env:255.0.0-3.6.9 .circleci/images

docker-run: docker-build
	docker run --name datastorm-test-env --publish 8081:8081 datastorm-test-env:255.0.0-3.6.9

docker-tag:
	docker tag datastorm-test-env:255.0.0-3.6.9 javierluna/datastorm-test-env:255.0.0-3.6.9

docker-push: docker-build docker-tag
	docker push javierluna/datastorm-test-env

docker-clean:
	docker stop datastore-test-env
	docker rm datastore-test-env

docker-test: docker-build
	docker run -d --name datastore-test-env --publish 8081:8081 datastorm-test-env:255.0.0-3.6.9
	sleep 5
	$(MAKE) test
	$(MAKE) docker-clean


clean:
	rm -rf build
	rm -rf datastorm.egg-info
	rm -rf dist
	rm -rf htmlcov
	rm .coverage

upload:
	python setup.py bdist_wheel
	twine upload dist/*
