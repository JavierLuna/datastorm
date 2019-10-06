def test_create_fetch_entity_with_list(ds_entity):
    entity_key = "test_entity"
    list_values = [1, 2, 3]
    dict_values = {"test": "test"}
    int_value = 3
    test_entity = ds_entity(entity_key, list_field=list_values, dict_field=dict_values, int_field=int_value)
    test_entity.save()
    fetched_test_entity = ds_entity.query.get(entity_key)

    assert fetched_test_entity.list_field == list_values

    assert fetched_test_entity.dict_field == dict_values

    assert fetched_test_entity.int_field == int_value
