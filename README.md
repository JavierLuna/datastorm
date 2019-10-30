# Datastorm
![Python versions](https://img.shields.io/badge/Python-3.6%2C%203.7-green.svg) [![PyPI version](https://badge.fury.io/py/datastorm.svg)](https://badge.fury.io/py/datastorm) [![Documentation Status](https://readthedocs.org/projects/datastorm/badge/?version=latest)](https://datastorm.readthedocs.io/en/latest/?badge=latest) [![CircleCI](https://circleci.com/gh/JavierLuna/datastorm/tree/master.svg?style=svg)](https://circleci.com/gh/JavierLuna/datastorm/tree/master)

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
from datastorm import fields
class EntityName(datastorm.DSEntity): 
    __kind__ = "EntityName"
    foo = fields.StringField(default="Default values rules!")
```

### Query for a field 

```python
results = EntityName.query.filter(EntityName.foo == "bar").all()

for result in results:
    do_stuff(result) # type(result) is EntityName
```

### Query several filters
```python
from datastorm.filter import Filter
results = EntityName.query.filter(EntityName.foo == "bar").filter(Filter('numeric_foo', '<', 2)).all()

for result in results:
    do_stuff(result) # type(result) is EntityName
```

### Create or update entity
```python
e = EntityName()
e.foo = "bar"
e.save()
e.foo = "rab"
e.set('bar', True)
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

## Test
To be able to run the tests, you'll need [Docker](https://www.docker.com/) installed.
Then:
```
make docker-test
```
To be able to run the tests without Docker, please visit the documentation.

## Disclaimer

Fork from [OrbitalAds/dittostore](https://github.com/OrbitalAds/dittostore), which I also created.
