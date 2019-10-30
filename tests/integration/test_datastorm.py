import uuid

import pytest

from datastorm.limits.batching import MAX_BATCH_SIZE


@pytest.fixture
def uuid_gen():
    return lambda: str(uuid.uuid4())


def test_create_entity_str_key_ok(uuid_gen, ds_entity):
    key = uuid_gen()
    test_entity = ds_entity(key)
    test_entity.save()


def test_create_entity_key_ok(datastorm_client, uuid_gen, ds_entity):
    key = datastorm_client.generate_key(ds_entity.__kind__, uuid_gen())
    test_entity = ds_entity(key)
    test_entity.save()


def test_create_entity_parent_key_ok(datastorm_client, uuid_gen, ds_entity):
    parent_key = datastorm_client.generate_key(ds_entity.__kind__, uuid_gen())
    key = datastorm_client.generate_key(ds_entity.__kind__, uuid_gen(), parent_key=parent_key)
    test_entity = ds_entity(key)
    test_entity.save()


def test_create_entity_no_kind_ko(datastorm_client, uuid_gen, ds_entity):
    class TestEntity2(datastorm_client.DSEntity):
        pass

    with pytest.raises(ValueError):
        test_entity = TestEntity2(uuid_gen())
        test_entity.save()


def test_save_multi_ok(datastorm_client, uuid_gen, ds_entity):
    entity_batch = [ds_entity(uuid_gen()) for _ in range(100)]
    datastorm_client.save_multi(entity_batch)


def test_save_multi_auto_batches(datastorm_client, uuid_gen, ds_entity):
    entity_batch = [ds_entity(uuid_gen()) for _ in range(MAX_BATCH_SIZE + 100)]
    datastorm_client.save_multi(entity_batch)
