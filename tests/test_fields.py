import unittest

from datastorm.fields import BaseField, AnyField, BooleanField, IntField, FloatField, StringField, DictField, ListField


class TestBaseField(unittest.TestCase):


    def test_base_field_loads(self):
        field = BaseField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.loads(value))

    def test_base_field_dumps_no_enforce_type(self):
        field = BaseField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_base_field_dumps_enforce_type(self):
        field = BaseField(enforce_type=True)
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_base_field_default_default_None(self):
        field = BaseField()
        self.assertIsNone(field.default)

    def test_base_field_default_value(self):
        field = BaseField(default=1)
        self.assertEqual(1, field.default)

    def test_base_field_default_callable(self):
        field = BaseField(default=lambda : 1)
        self.assertEqual(1, field.default)


class TestAnyField(unittest.TestCase):

    def test_any_field_loads(self):
        field = AnyField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.loads(value))

    def test_any_field_dumps_no_enforce_type(self):
        field = AnyField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_any_field_dumps_enforce_type(self):
        field = AnyField(enforce_type=True)
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_any_field_default_default_None(self):
        field = AnyField()
        self.assertIsNone(field.default)

    def test_any_field_default_value(self):
        field = AnyField(default=1)
        self.assertEqual(1, field.default)

    def test_any_field_default_callable(self):
        field = AnyField(default=lambda: 1)
        self.assertEqual(1, field.default)

class TestBooleanField(unittest.TestCase):

    def test_boolean_field_loads(self):
        field = BooleanField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.loads(value))

    def test_boolean_field_dumps_no_enforce_type(self):
        field = BooleanField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_boolean_field_dumps_enforce_type(self):
        field = BooleanField(enforce_type=True)
        for value in [1, 1.2, "foo", object(), {}, []]:
            with self.assertRaises(ValueError):
                field.dumps(value)
        self.assertEqual(True, field.dumps(True))

    def test_boolean_field_default_default_None(self):
        field = BooleanField()
        self.assertIsNone(field.default)

    def test_boolean_field_default_value(self):
        field = BooleanField(default=True)
        self.assertEqual(True, field.default)

    def test_boolean_field_default_callable(self):
        field = BooleanField(default=bool)
        self.assertEqual(bool(), field.default)

class TestIntField(unittest.TestCase):

    def test_int_field_loads(self):
        field = IntField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.loads(value))

    def test_int_field_dumps_no_enforce_type(self):
        field = IntField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_int_field_dumps_enforce_type(self):
        field = IntField(enforce_type=True)
        for value in [1.2, True, "foo", object(), {}, []]:
            with self.assertRaises(ValueError):
                field.dumps(value)
        self.assertEqual(1, field.dumps(1))

    def test_int_field_default_default_None(self):
        field = IntField()
        self.assertIsNone(field.default)

    def test_int_field_default_value(self):
        field = IntField(default=1)
        self.assertEqual(1, field.default)

    def test_int_field_default_callable(self):
        field = IntField(default=int)
        self.assertEqual(int(), field.default)

class TestFloatField(unittest.TestCase):

    def test_float_field_loads(self):
        field = FloatField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.loads(value))

    def test_float_field_dumps_no_enforce_type(self):
        field = FloatField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_float_field_dumps_enforce_type(self):
        field = FloatField(enforce_type=True)
        for value in [1, True, "foo", object(), {}, []]:
            with self.assertRaises(ValueError):
                field.dumps(value)
        self.assertEqual(1.2, field.dumps(1.2))

    def test_float_field_default_default_None(self):
        field = FloatField()
        self.assertIsNone(field.default)

    def test_float_field_default_value(self):
        field = FloatField(default=1.2)
        self.assertEqual(1.2, field.default)

    def test_float_field_default_callable(self):
        field = FloatField(default=float)
        self.assertEqual(float(), field.default)

class TestStringField(unittest.TestCase):

    def test_string_field_loads(self):
        field = StringField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.loads(value))

    def test_string_field_dumps_no_enforce_type(self):
        field = StringField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_string_field_dumps_enforce_type(self):
        field = StringField(enforce_type=True)
        for value in [1, 1.2, True, object(), {}, []]:
            with self.assertRaises(ValueError):
                field.dumps(value)
        self.assertEqual("foo", field.dumps("foo"))

    def test_string_field_default_default_None(self):
        field = StringField()
        self.assertIsNone(field.default)

    def test_string_field_default_value(self):
        field = StringField(default="foo")
        self.assertEqual("foo", field.default)

    def test_string_field_default_callable(self):
        field = StringField(default=str)
        self.assertEqual(str(), field.default)

class TestDictField(unittest.TestCase):

    def test_dict_field_loads(self):
        field = DictField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.loads(value))

    def test_dict_field_dumps_no_enforce_type(self):
        field = DictField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_dict_field_dumps_enforce_type(self):
        field = DictField(enforce_type=True)
        for value in [1, 1.2, True, "foo", object(), []]:
            with self.assertRaises(ValueError):
                field.dumps(value)
        self.assertEqual({}, field.dumps({}))

    def test_dict_field_default_default_None(self):
        field = DictField()
        self.assertIsNone(field.default)

    def test_dict_field_default_value(self):
        field = DictField(default={})
        self.assertEqual({}, field.default)

    def test_dict_field_default_callable(self):
        field = DictField(default=dict)
        self.assertEqual(dict(), field.default)

class TestListField(unittest.TestCase):

    def test_list_field_loads(self):
        field = ListField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.loads(value))

    def test_list_field_dumps_no_enforce_type(self):
        field = ListField()
        for value in [1, 1.2, True, "foo", object(), {}, []]:
            self.assertEqual(value, field.dumps(value))

    def test_list_field_dumps_enforce_type(self):
        field = ListField(enforce_type=True)
        for value in [1, 1.2, True, "foo", object(), {}]:
            with self.assertRaises(ValueError):
                field.dumps(value)
        self.assertEqual([], field.dumps([]))

    def test_list_field_default_default_None(self):
        field = ListField()
        self.assertIsNone(field.default)

    def test_list_field_default_value(self):
        field = ListField(default=[])
        self.assertEqual([], field.default)

    def test_list_field_default_callable(self):
        field = ListField(default=list)
        self.assertEqual(list(), field.default)