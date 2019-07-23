# Datastorm entities

## Basic Entity definition

An entity is a mapping between Google's Datastore and Python objects.

```python
from datastorm import Datastorm
from datastorm import fields

datastorm = Datastorm("test-project")

class FruitEntity(datastorm.DSEntity):
	__kind__ = 'Fruit' # Entity's name in Datastore
	
	color = fields.StringField()
	weight = fields.IntField()

```


### Base attributes

Base attributes are fields that the instances of your entity should have.

> The tree that doesn't bend breaks. Be flexible, be like bamboo.

See, Datastore is a _schemaless_ database. For that reason, two instances of your entity could have different attributes, and without no rules your shiny Python code could turn into a bug-nest.

However, we know pretty damn well bamboo trees have structure! You ain't lying to us Bruce Lee!

Datastorm takes a bamboo-style approach and let's you define attributes that almost all entity instances will have.

Although Datastorm doesn't really limits you in how you define attributes on the fly, It isn't really a good idea to do so. The more you define your entities' structure, the less bugs you'll have.

### Entity Creation

Creating a Datastorm entity and saving it to your Datastore database is reeaaaaaally simple.

Using the `FruitEntity` we created earlier:

```python

strawberry = FruitEntity("strawberry", color="red", weight=3, is_smol=True) # "strawberry" is the datastore key

strawberry.save()

strawberry.weight = 1 # Strawberries are small ok?

strawberry.save()

```

And that's how you create and save an entity! Really simple right?

See, the only "pain" you must live with is providing the Datastore key in the constructor. That aside, you can pass all attributes you want in the constructor and Datastorm will treat them like Datastore fields automatically. 

Yes, even if you pass an attribute that doesn't exist.

Even though I've told you not to declare attributes on the fly, If you are going to do naughty things, at least do it in a proper way:

```python

strawberry.set('berry', True, field=fields.BooleanField())

```

### Entity deletion

Deleting an entity's instance is even easier than creating it:

```python
strawberry.delete()
```

And that's it.

### Entity sync

Imagine you create an entity's instance in your code. And you are pretty damn sure this particular instance also exists in Datastore.

Instead of making a query or a `get`, you could directly sync it and have it updated anytime you want:

```python
orange = FruitEntity("orange")
orange.sync()
print(orange.color) # "orange"
```

`sync()` will fetch your Datastore entity and will map everything in your Datastorm instance for you.

The only thing you must be careful with is that this will override all the properties your Datastorm entity instance shares with its Datastore counterpart.

### Base filters

Imagine that for some reason (my reason was comfort but each their own) you want to declare two Datastorm entities that refer to the same Datastore entity kind:

```python

class RedFruitEntity(datastorm.DSEntity):
	__kind__ = 'Fruit'
	
	is_strawberry = fields.BooleanField(default=False)

```

Following a little naming logic, you would expect your `RedFruitEntity` instances to have `color='red'`, but right now this isn't the case.

Worry no more, I have the solution!

```python
from datastorm.filter import Filter

class RedFruitEntity(datastorm.DSEntity):
	__kind__ = 'Fruit'
	__base_filters_ = [Filter('color', '=', 'red')]
	
	is_strawberry = fields.BooleanField(default=False)
```

In your entity definition you could add a list of filters that will be taken into consideration every time you perform a query against Datastore. In this example, every instance will have the `color` attribute to `red`.

### Getting the Datastore Entity object

There'll be times when this awesome ODM we call Datastorm could fall short for a certain usecase of yours. Maybe you felt kinky and tried excluding some attributes from the index?

Lucky for you, kinky programmer, there's a easy way to translate a Datastorm entity into a Datastore entity:

```python
strawberry.get_datastore_entity()
```

Huh, it was that easy. Who would've known!

