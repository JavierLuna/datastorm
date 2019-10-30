def test_create_ok(uuid_gen, ds_entity):
    uuid = uuid_gen()
    assert ds_entity.query.get(uuid) is None
    ds_entity(uuid, uuid=uuid).save()
    result = ds_entity.query.get(uuid)
    assert result is not None
    assert result.uuid == uuid


def test_update_ok(uuid_gen, ds_entity):
    uuid = uuid_gen()
    assert ds_entity.query.get(uuid) is None
    a = ds_entity(uuid, uuid=uuid, int_field=1)
    a.save()
    result = ds_entity.query.get(uuid)
    assert result is not None
    assert result.uuid == uuid
    assert result.int_field == 1

    a.int_field = 2
    a.save()

    result = ds_entity.query.get(uuid)

    assert result is not None
    assert result.uuid == uuid
    assert result.int_field == 2


def test_delete_ok(uuid_gen, ds_entity):
    uuid = uuid_gen()
    assert ds_entity.query.get(uuid) is None
    a = ds_entity(uuid, uuid=uuid)
    a.save()
    result = ds_entity.query.get(uuid)

    assert result is not None
    assert result.uuid == uuid

    a.delete()

    result = ds_entity.query.get(uuid)

    assert result is None
