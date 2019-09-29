from datastorm import fields


def test_create_fetch_entity_with_list(ds_entity):
    entity_key = "test_entity"
    datastore_field_name = "datastore"

    class CustomEntity(ds_entity):
        aliased_field = fields.AnyField(field_name=datastore_field_name)

    test_entity = CustomEntity(entity_key)
    test_entity.save()
    fetched_test_entity = CustomEntity.query.get(entity_key)

    assert not hasattr(fetched_test_entity, datastore_field_name)
