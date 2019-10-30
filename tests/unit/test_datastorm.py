from unittest.mock import Mock

import pytest
from google.cloud import datastore

from datastorm import DataStorm
from datastorm.exceptions.datastore import BatchSizeLimitExceeded
from datastorm.limits.batching import MAX_BATCH_SIZE


@pytest.fixture
def environ_project_id():
    import os
    environ_project_id = "env-test-project-id"
    os.environ['DATASTORE_PROJECT_ID'] = environ_project_id
    return environ_project_id


def test_init_datastorm_no_args_uses_env_project_id(environ_project_id):
    d = DataStorm()
    assert d.project == environ_project_id


def test_init_datastorm_project_id_supplied_overrides_env_project_id(datastorm_client, environ_project_id,
                                                                     mock_project_id):
    assert datastorm_client.project == mock_project_id


def test_datastorm_client_proxies_gcp_datastore_client(datastorm_client, mock_project_id):
    assert type(datastorm_client.client) == datastore.Client


def test_datastorm_client_proxies_gcp_datastore_client_supplied_project_id(datastorm_client, mock_project_id):
    assert datastorm_client.client.project == mock_project_id


@pytest.mark.parametrize("n_entities, batch_size, n_save_multi_calls", [(1, 1, 1),
                                                                        (2, 1, 2),
                                                                        (1, 2, 1),
                                                                        (500, 500, 1),
                                                                        (2, 500, 1)])
def test_save_multi_proxies_gcp_datastore_put_multi(datastorm_client, mocked_datastore, n_entities, batch_size,
                                                    n_save_multi_calls):
    mocked_put_multi = Mock()
    mocked_entity = Mock()
    mocked_datastore.put_multi = mocked_put_multi
    datastorm_client.save_multi([mocked_entity] * n_entities, batch_size=batch_size)
    assert datastorm_client.client.put_multi.call_count == n_save_multi_calls


def test_save_multi_raises_value_error_batch_size_zero(datastorm_client, mocked_datastore):
    mocked_put_multi = Mock()
    mocked_datastore.put_multi = mocked_put_multi
    with pytest.raises(ValueError):
        datastorm_client.save_multi([], batch_size=0)


def test_save_multi_raises_size_limit_exceeded(datastorm_client, mocked_datastore):
    mocked_put_multi = Mock()
    mocked_datastore.put_multi = mocked_put_multi
    with pytest.raises(BatchSizeLimitExceeded):
        datastorm_client.save_multi([], batch_size=MAX_BATCH_SIZE + 1)


def test_save_multi_converts_datastore_entities(datastorm_client, mocked_datastore):
    n_entities = 3
    entities = [Mock() for _ in range(n_entities)]
    datastorm_client.save_multi(entities)
    assert all(entity.get_datastore_entity.called for entity in entities)


def test_ds_entity_proxies_provisioned_datastore_client(datastorm_client, mock_project_id):
    ds_entity = datastorm_client.DSEntity
    assert ds_entity._datastore_client.project == mock_project_id


def test_generate_key_proxies_datastore_key(datastorm_client, mocked_datastore):
    datastorm_client.generate_key("test", "test")
    assert datastorm_client.client.key.called
