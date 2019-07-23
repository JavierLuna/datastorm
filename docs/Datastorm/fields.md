# Datastorm fields

Fields are objects which define how to serialize/deserialize one entity's property.

Along many other things, they provide additional validation and safety for the programmer.

Currently, there is a limited and nearly dummy field collection, which you can use like this:

```python
from datastorm import fields

string_field = fields.StringField()
boolean_field = fields.BooleanField()
```

And so on.

## Field interface

Every field must expose this interface:

#### Init

```python
StringField(field_name: str= None, enforce_type: bool=False, default: Any=None)
```

* `field_name`: Name of the field in Datastore. This way you can map any Datastorm field with any Datastore field. Defaults to `None`. If value is `None`, the name of the variable in which you store the attribute will be used.
* `enforce_type`: Check if the value of the attribute is of a certain type. For example, if the field is a `StringField`, it will check whether the value of the field is of type `str`.
* `default`: This can be either a value or a `callable`. Pretty self explanatory.

#### Loads

```python
IntField().loads("123") # 123, type 'int'
```

This function's purpose is to turn a Datastore value into its type.

#### Dumps

```python
IntField().dumps(123) # 123, type 'int'
```

This function's purpose is to turn a Python object into a Datastore valid type. In this example, the usecase is pretty dumb as you may have noticed, but Datetimes could be useful to have.

#### Check Type

```python
IntField().check_type("test") # False
```

Checks the input's type.



## List of available fields

* `AnyField`: Nihilist by nature, he doesn't even care a little of what do you want to put there.
* `BooleanField`
* `IntField`
* `FloatField`
* `StringField`
* `DictField`
* `ListField`

## Creating your own field

Creating your own field is as easy as extending `BaseField` and overriding the interface described before:

```python
from datastorm.fields import BaseField

class StringyBooleanField(BaseField):
	def dumps(self, value):
		return "True" if value else "False"
	
	def loads(self, value):
		return value == "True"

```

Other thing you must take into consideration is that Datastorm produces filters from the comparison magic methods, so if you want to make cool filtering available for your field, you must override those too:

```python
from datastorm.fields import BaseField

class StringyBooleanField(BaseField):
	def dumps(self, value):
		return "True" if value else "False"
	
	def loads(self, value):
		return value == "True"
	
	def __eq__(self, other):
		return Fitler(self.field_name, '=', other)
	
	def __lt__(self, other):
		return NotImplemented
	
	def __gt__(self, other):
		return NotImplemented # We don't want to compare by gt or lt
```