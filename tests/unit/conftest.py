import pytest


@pytest.fixture
def mocked_datastore(mocker):
    return mocker.patch('datastorm.datastorm.datastore.Client')
