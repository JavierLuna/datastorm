import pytest
from google.auth.credentials import AnonymousCredentials

from datastorm import DataStorm, fields


@pytest.fixture(scope='session')
def test_project_id():
    return "datastorm-test-env"


@pytest.fixture(scope='session')
def datastorm_client(test_project_id):
    return DataStorm(test_project_id, credentials=AnonymousCredentials())


@pytest.fixture
def ds_entity(datastorm_client):
    class TestEntity1(datastorm_client.DSEntity):
        __kind__ = "TestEntity1"

        dict_field = fields.DictField()
        list_field = fields.ListField()
        int_field = fields.IntField()

    yield TestEntity1

    [entity.delete() for entity in TestEntity1.query.all()]
