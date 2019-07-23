## Datastorm "main" object

All your Datastorm entities and stuff are built arround this object.

This object holds the information about how to connect with Datastore. See credentials, host, project id...

## Initialize a project

You must have seen this in every page of this documentation, but here it is:

```python
from datastorm import Datastorm

datastorm = Datastorm("test-project")
```

Signature is:

`Datastorm(project=None, namespace=None, credentials=None)`

All variables refer to the Datastore client initialization, so you better check their documentation.

The only tweak is that if `project` is left to `None`, Datastorm will attempt to get the project id from the environmental variable `DATASTORE_PROJECT_ID`.

## Client

As the `Datastorm` object is a thin wrapper arround Datastore client, you can get the original client:

```python
datastorm.client # Datastore client
```


## Save bulk

There'll be times when you'd need to save a batch of Datastorm instances:

```python
datastorm.save_multi([orange, strawberry, blueberry])
```

And that's it!


## Generate entity key

Having all the fuss about keys is exhausting, so Datastorm provides a way of generating Datastore keys easily:

```python
datastorm.generate_key("Fruit", identifier="orange")
```