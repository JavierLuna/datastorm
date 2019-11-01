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

#### Repository branches

This repository has two main branches:
* `master`: Latest stable version released.
* `develop`: Latest version released, including pre-releases.

**Note:** At the moment, no stable version has been released, so master and develop are being used as "latest version released" and "next version" respectively.

#### Branch naming

Please, create a separate branch to do your work, no important how little it'd be.
Use the following naming:

* **Features**: `feature/DS-<issue id>-<issue keywords>`. Example: `feature/DS-11-pytests`
* **Bugs**: `bug/DS-<issue id>-<issue keyworkds>`. Example: `bug/DS-14-list-dict-serialization`


Please branch from `develop` and target your PR to `develop` as well.

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
