# Dittostore

## What is it?

**Dittostore** is an attempt to make your datastore experience painless.

How am I going to do that? I'll show you!


## How to

### Connect to DataStore

```python
from dittostore.dittostore import DittoStore

dittostore = DittoStore("example-gcloud-project")
```

### Define an entity

```python
class EntityName(dittostore.DSEntity): 
    __kind__ = "EntityName"
```

### Query for a field 

```python
results = EntityName.query.filter(EntityName.foo == "bar").all()

for result in results:
    do_stuff(result) # type(result) is EntityName
```

### Query several filters
```python
results = EntityName.query.filter(EntityName.foo == "bar").filter(EntityName.numeric_foo < 2).all()

for result in results:
    do_stuff(result) # type(result) is EntityName
```

### Create or update entity
```python
e = EntityName()
e.foo = "bar"
e.save()
e.foo = "rab"
e.bar = True
e.save()
```

### Batch create/update entities
```python
dittostore.save_multi(entity_list)
```

## Install
```bash
pip install dittostore
```

## Disclaimer

Proper tests and a decent documentation will roll in a few days.