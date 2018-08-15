# Datastorm

## What is it?

**Datastorm** is an attempt to make your datastore experience painless.

How am I going to do that? I'll show you!


## How to

### Connect to DataStore

```python
from datastorm.datastorm import DataStorm

datastorm = DataStorm("example-gcloud-project")
```

### Define an entity

```python
class EntityName(datastorm.DSEntity): 
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
datastorm.save_multi(entity_list)
```

## Install
```bash
pip install datastorm
```

## Disclaimer

Proper tests and a decent documentation will roll in a few days.

Fork from [OrbitalAds/dittostore](https://github.com/OrbitalAds/dittostore), which I also created.