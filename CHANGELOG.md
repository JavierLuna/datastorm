# Changelog

#### v0.0.0a3

* Add only() function to query. This adds [projection's support](https://cloud.google.com/datastore/docs/concepts/queries#projections).
* Add sync() to a DSEntity. It basically fetches the data from datastore to our entity. It comes handy when projection is used in a query and you don't want to delete other columns on the entity.
* Add force_sync parameter to all() query method. Forces a sync() before saving to datastore. A "safe save" if you will.