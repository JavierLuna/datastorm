# Tests

## Via Docker (easy)

If you have [Docker](https://www.docker.com/) installed, you can run the tests via terminal like this:
```
make docker-test
```

This will:

1. Download the testing environment, containing the datastore emulator needed for the tests to pass.
2. Run the downloaded image into a container, exposing port `8081`, needed for the test suite to connect to the emulator
3. Stop the emulator and remove the image from your system

This way, you don't need to install the `google-cloud-sdk` yourself.

## Via datastore emulator

First, you must have the `datastore` emulator installed via `google-cloud-sdk`. [Link](https://cloud.google.com/datastore/docs/tools/datastore-emulator).
Then, you need to have to start the emulator with these settings:

* `consistency=1`
* `project=datastorm-test-env`
* `host-port=0.0.0.0:8081`

Once you have the emulator up and running, you can fire the tests with:
```
make test
```

This approach is recommended if you need to constantly work on the library as it is much much faster than using docker.