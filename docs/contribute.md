# Contributing guidelines

Hi! I'm so glad that you want to help with the Datastorm project, I really do!

All contributions and work that comes in good faith are welcome. Please, check Datastorm's [Code of Conduct](https://github.com/JavierLuna/datastorm/blob/master/CODE_OF_CONDUCT.md) before contributing.

## Questions, feature requests, bugs...

...should be reported to the [project's issue tracker](https://github.com/JavierLuna/datastorm/issues/new/choose)

## Ways to contribute

You can contribute to Datastorm by:

* Looking and comment at [opened issues](https://github.com/JavierLuna/datastorm/issues). Feedback is always welcome!
* Help with code review: ([PRs](https://github.com/JavierLuna/datastorm/pulls))
* Fixing or improving the [docs](https://datastorm.readthedocs.io/en/latest/). 
* Reporting [bugs](https://github.com/JavierLuna/datastorm/issues/new/choose)
* Giving the project a star if you feel like doing so :)

## Contribute to code

First, fork [Datastorm](https://github.com/JavierLuna/datastorm) on Github.

### Setting up your environment

This project uses the [Poetry](https://github.com/sdispater/poetry) dependency management tool, 
so you must have it installed.

Then, run `make development`. This will:
* Install `datastorm` and its dependencies
* Install `pre-commit` hooks

To be able to run the tests, you should either install [Docker](https://docs.docker.com/install/) or the [Datastore](https://cloud.google.com/datastore/docs/tools/datastore-emulator) emulator.

Docker is preferred, as the `Makefile` has targets to run the tests under a docker container, but feel free to use the emulator instead.

### Git workflow

This repository follows a modified [Github workflow](https://guides.github.com/introduction/flow/).

Differences:
* Branches will follow the naming: `DS-<issue id>-short-descriptive-name`. Example: `DS-11-pytests`
* Releases will happen when a `0.0.0a0` tag is pushed. This tag will be created manually by the project administrator.

**Note:** The `0.0.0a0` will be active until it is decided to abandon the alpha state, then it will be `0.0.0`.

#### Commits

Atomic commits are preferred over big ones, and please, write meaningful commit messages.
Commit messages should start with `DS-<issue id>: `.

#### PR acceptance criteria

* Unit tests to cover your new code. Ideally, test for all possible branches.
* Integration tests
* E2E tests if deem necessary 
* Covers the issue
* Passes code review

### Running tests

You can run all tests with `make docker-tests` to spin up a docker-based datastore emulator, or do `make tests` to use a local datastore emulator.

### Documentation

Docs are located in the `docs` directory and are written in markdown using [mkdocs](https://www.mkdocs.org/user-guide/writing-your-docs/).

You can build and take a look at the docs with `make docs`.

Docs are hosted on [Read the docs](https://datastorm.readthedocs.io) and are built and pushed automatically.
