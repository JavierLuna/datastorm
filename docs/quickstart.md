# Datastorm

A simple and intuitive Google Datastore ODM 

## Installation
`datastorm` is currently on [PyPi](https://pypi.org/project/datastorm/), so you can install it using `pip`:

```
pip install datastorm
```

## Quickstart

Let's say we want to use Datastore in a gcp project called `"example-gcloud-project"`. Why not? It's catchy!


### Initialize datastorm object

First, define your `datastorm` object, which will help us define entities along many other things:

```python
from datastorm import Datastorm

datastorm = DataStorm("example-gcloud-project")
``` 

### Define the entity

Then, you'll need to define the entity you want to work with. This is the same process other ORM's and ODM's use (like SQLAlchemy):

```python
from datastorm import fields

class EntityName(datastorm.DSEntity):
    __kind__ = "EntityName" # Datastore entity kind
    foo = fields.StringField(default="Default values rules!")
```

### Query for a field

```python
results = EntityName.query.filter(EntityName.foo == "bar").all() # Returns a generator.

for result in results:
    do_stuff(result) # type(result) -> EntityName
```

### Query several fields

You can also chain multiple filters and will treat them as `filter1 AND filter2`.

```python
from datastorm.filter import Filter

results = EntityName.query.filter(EntityName.foo == "bar").filter(Filter("numeric_foo", '<', 2)).all()

for result in results:
    do_stuff(result) # type(result) -> EntityName
```
You can also query for a filter that hasn't being defined in the entity using `Filter` like in the example above.

### Create or update entity

```python
e = EntityName("entity-key")
e.foo = "bar"
e.save() # Creates
e.set("bartolo", True) # New attribute, only for this specific entity.
e.save() # Updates
```

### Batch create/update entities
Obviously, you'll want to batch upsert entities sooner than later. You can do this with:

```python
datastorm.save_multy(entity_list)
```

