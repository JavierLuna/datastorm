import pytest

from datastorm.fields import IntField, FloatField, StringField, BooleanField


def test_query_get_no_filter_no_result(ds_entity, uuid_gen):
    result = ds_entity.query.get(uuid_gen())
    assert result is None


def test_query_get_no_filter_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen).save()
    result = ds_entity.query.get(uuid_gen)
    assert result is not None


def test_query_get_int_filter_eq_no_result(ds_entity, uuid_gen):
    result = ds_entity.query.filter(IntField("int_field") == 1).get(uuid_gen())
    assert result is None


def test_query_get_float_filter_eq_no_result(ds_entity, uuid_gen):
    result = ds_entity.query.filter(FloatField("float_field") == 1.0).get(uuid_gen())
    assert result is None


def test_query_get_str_filter_eq_no_result(ds_entity, uuid_gen):
    result = ds_entity.query.filter(StringField("str_field") == "foo").get(uuid_gen())
    assert result is None


def test_query_get_dict_filter_eq_no_result(ds_entity, uuid_gen):
    result = ds_entity.query.filter(ds_entity.dict_field == {}).get(uuid_gen())
    assert result is None


def test_query_get_list_filter_eq_no_result(ds_entity, uuid_gen):
    result = ds_entity.query.filter(ds_entity.list_field == []).get(uuid_gen())
    assert result is None


def test_query_get_int_filter_eq_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, int_field=1, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(IntField("int_field") == 1).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_float_filter_eq_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, float_field=1.0, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(FloatField("float_field") == 1.0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_str_filter_eq_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foo", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField("str_field") == "foo").filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_int_filter_lt_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, int_field=2, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(IntField("int_field") < 1).filter(StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_float_filter_lt_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, float_field=2.0, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(FloatField("float_field") < 1.0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_str_filter_lt_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foo", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField("str_field") < "foe").filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_int_filter_lt_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, int_field=1, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(IntField("int_field") < 2).filter(StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_float_filter_lt_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    a = ds_entity(uuid_gen, float_field=1.0, uuid_gen=uuid_gen)
    a.save()
    result = ds_entity.query.filter(FloatField("float_field") < 2.0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_str_filter_lt_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foo", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField("str_field") < "fop").filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_int_filter_gt_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, int_field=1, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(IntField("int_field") > 1).filter(StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_float_filter_gt_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, float_field=1.0, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(FloatField("float_field") > 1.0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_str_filter_gt_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foo", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField("str_field") > "foo").filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_int_filter_gt_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, int_field=2, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(IntField("int_field") > 1).filter(StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_float_filter_gt_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, float_field=2.0, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(FloatField("float_field") > 1.0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    results = list(ds_entity.query.all())
    assert result is not None


def test_query_get_str_filter_gt_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foe", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField("str_field") > "foa").filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_int_filter_le_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, int_field=1, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(IntField("int_field") <= 0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_float_filter_le_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, float_field=1.0, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(FloatField("float_field") <= 0.0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_str_filter_le_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foo", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField("str_field") <= "foa").filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_int_filter_le_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, int_field=2, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(IntField("int_field") <= 2).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_float_filter_le_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, float_field=2.0, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(FloatField("float_field") <= 2.0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_str_filter_le_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foe", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField("str_field") <= "foe").filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_int_filter_ge_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, int_field=0, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(IntField("int_field") >= 1).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_float_filter_ge_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, float_field=0.0, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(FloatField("float_field") >= 1.0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_str_filter_ge_no_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foa", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField("str_field") >= "foo").filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is None


def test_query_get_int_filter_ge_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, int_field=2, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(IntField("int_field") >= 2).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_float_filter_ge_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, float_field=2.0, uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(FloatField("float_field") >= 2.0).filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_get_str_filter_ge_result(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foe", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField("str_field") >= "foe").filter(
        StringField("uuid_gen") == uuid_gen).first()
    assert result is not None


def test_query_multiple_filters(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foe", other_field="foe2", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField('str_field') == "foe",
                                    StringField('other_field') == "foe2").first()
    assert result.uuid_gen == uuid_gen


def test_query_chained_filters(ds_entity, uuid_gen):
    uuid_gen = uuid_gen()
    ds_entity(uuid_gen, str_field="foe", other_field="foe2", uuid_gen=uuid_gen).save()
    result = ds_entity.query.filter(StringField('str_field') == "foe").filter(
        StringField('other_field') == "foe2").first()
    assert result.uuid_gen == uuid_gen


def test_query_ordered_ascendent_results(ds_entity, uuid_gen):
    uuid_gen1, uuid_gen2 = uuid_gen(), uuid_gen()
    ds_entity(uuid_gen1, int_field=1, uuid_gen=uuid_gen1).save()
    ds_entity(uuid_gen2, int_field=2, uuid_gen=uuid_gen2).save()
    results = list(ds_entity.query.order(ds_entity.int_field).all())
    assert len(results) == 2
    assert uuid_gen1 == results[0].uuid_gen
    assert uuid_gen2 == results[1].uuid_gen


def test_query_ordered_descendent_results(ds_entity, uuid_gen):
    uuid_gen1, uuid_gen2 = uuid_gen(), uuid_gen()
    ds_entity(uuid_gen1, int_field=1, uuid_gen=uuid_gen1).save()
    ds_entity(uuid_gen2, int_field=2, uuid_gen=uuid_gen2).save()
    results = list(ds_entity.query.order(ds_entity.int_field, inverted=True).all())
    assert len(results) == 2
    assert uuid_gen2 == results[0].uuid_gen
    assert uuid_gen1 == results[1].uuid_gen


def test_chained_order_and_filters(ds_entity, uuid_gen):
    uuid_gen1, uuid_gen2 = uuid_gen(), uuid_gen()
    ds_entity(uuid_gen1, int_field=1, foo=True, uuid_gen=uuid_gen1).save()
    ds_entity(uuid_gen2, int_field=2, foo=True, uuid_gen=uuid_gen2).save()
    results = list(
        ds_entity.query.order(ds_entity.int_field).filter(BooleanField('foo') == True).all())

    assert len(results) == 2
    assert uuid_gen1 == results[0].uuid_gen
    assert uuid_gen2 == results[1].uuid_gen


def test_chained_filters_and_order(ds_entity, uuid_gen):
    uuid_gen1, uuid_gen2 = uuid_gen(), uuid_gen()
    ds_entity(uuid_gen1, int_field=1, foo=True, uuid_gen=uuid_gen1).save()
    ds_entity(uuid_gen2, int_field=2, foo=True, uuid_gen=uuid_gen2).save()
    results = list(
        ds_entity.query.filter(BooleanField('foo') == True).order(ds_entity.int_field).all())
    assert len(results) == 2
    assert uuid_gen1 == results[0].uuid_gen
    assert uuid_gen2 == results[1].uuid_gen


def test_query_parent_key(ds_entity, datastorm_client, uuid_gen):
    parent_uuid_gen, descendant_uuid_gen = uuid_gen(), uuid_gen()

    class TestEntity2(datastorm_client.DSEntity):
        __kind__ = "TestEntity2"

    parent = TestEntity2(parent_uuid_gen, int_field=1, uuid_gen=parent_uuid_gen)
    parent.save()
    ds_entity(
        datastorm_client.generate_key(ds_entity.__kind__, descendant_uuid_gen, parent_key=parent.key),
        int_field=2, uuid_gen=descendant_uuid_gen).save()

    result = list(ds_entity.query.all(parent_key=parent.key))
    assert len(result) == 1
    assert result[0].uuid_gen == descendant_uuid_gen


def test_query_projection(ds_entity, uuid_gen):
    uuid_gen1 = uuid_gen()
    ds_entity(uuid_gen1, int_field=1, float_field=1.2).save()
    result = ds_entity.query.only('int_field').first()
    assert result['int_field'] == 1
    assert not hasattr(result, 'float_field')


def test_query_chained_projection_and_filters(ds_entity, uuid_gen):
    uuid_gen1 = uuid_gen()
    ds_entity(uuid_gen1, int_field=1, float_field=1.2).save()
    result = ds_entity.query.only('int_field').filter(IntField('int_field') >= 1).first()
    assert result['int_field'] == 1
    assert not hasattr(result, 'float_field')
