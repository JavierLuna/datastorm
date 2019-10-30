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

Datastorm will automatically batch your entity list to comply with  [Datastore's batch size limit](https://cloud.google.com/datastore/docs/concepts/limits).
You can specify the batch size using the `batch_size` parameter, which defaults to `500` (the maximum allowed by Datastore).

```python
datastorm.save_multi([orange, strawberry, blueberry], batch_size=2) # Will save in two batches
```


## Generate entity key

Having all the fuss about keys is exhausting, so Datastorm provides a way of generating Datastore keys easily:

```python
datastorm.generate_key("Fruit", identifier="orange")
```
