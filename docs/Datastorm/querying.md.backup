# Datastorm Query

What would be an ODM without query support.

I'd be trash. Like, complete and utterly trashy trash.

That's why Datastorm queries are so pleasant to use. They are simple and straight to the point, and provides us pagination with no BS.

```python
class FruitEntity(datastorm.DSEntity):
	__kind__ = 'Fruit'
	
	color = fields.StringField()
	weight = fields.IntField()

```

All query methods are under the `query` class property.

## Get

`get(key)` allows you to get an instance by its... key! Surprise!

```python
orange = FruitEntity.query.get("orange")
print(orange.color) # "orange"
```

## All

`all(page_size:int=500, parent_key: Key=None)`

This methods returns a generator which yields instances of your entity that matches the query.

* page_size: How many instances per page are requested to Datastore. Defaults to `500`.
* parent_key: Whether your instances have a parent key.

## First

Returns the first instance resulting from the query. `None` if there's no result.

## Order

`order(field: Union[BaseField, str], inverted: bool = False)`

Orders the results by a field.

```python
ordered_entities = FruitEntity.query.order("weight").all()
```

You can stack and order by different fields:

```python
ordered_entities = FruitEntity.query.order("weight").order("color", inverted=True).all()
```

## Filter

Alright!! Let's filter some stuff!!!

Syntax is pretty straigthforward:

```python
not_berries = FruitEntity.query.filter(FruitEntity.weight > 2).all()
```

You can stack them filters in an `and` way:

```python
blueberries = FruitEntity.query.filter(FruitEntity.weight == 1).filter(FruitEntity.color == "blue").all()
```

Cool huh?

If you don't have access to the Entity and you want to filter by an attribute, or lets say filter by a yet-to-be-defined attribute that some instances have:

```python
from datastorm.filter import Filter

seedless_fruits = FruitEntity.query.filter(Filter('has_seeds', '=', False)).all()
```


## Projection

Sometimes, you'd only want a subset of your instances' attributes. For example, If we only cared about `color`:

```python
only_colors = FruitEntity.query.only("color").all()
```

This will fetch only the color of the instances. 
**WARNING: Queries that makes use of only() will return Datastore instances, not Datastorm's!!!**

