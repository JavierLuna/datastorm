import os
from typing import List

from google.cloud import datastore
from google.cloud.datastore import Key

from datastorm.entity import BaseEntity, AbstractDSEntity
from datastorm.exceptions.datastore import BatchSizeLimitExceeded
from datastorm.limits.batching import MAX_BATCH_SIZE
from datastorm.utils.batching import split_batches


class DataStorm:

    def __init__(self, project=None, namespace=None, credentials=None, _http=None):
        self.project = project or os.getenv("DATASTORE_PROJECT_ID", None)
        self.credentials = credentials
        self.namespace = namespace
        self._http = _http

    @property
    def client(self):
        return datastore.Client(project=self.project, namespace=self.namespace, credentials=self.credentials,
                                _http=self._http)

    @property
    def DSEntity(self):
        return AbstractDSEntity("DSEntity", (BaseEntity,), {'__kind__': None, '_datastore_client': self.client})

    def save_multi(self, entities: List[BaseEntity], batch_size: int = MAX_BATCH_SIZE):
        if batch_size < 1:
            raise ValueError("Batch size must be greater than 0")
        if MAX_BATCH_SIZE < batch_size:
            raise BatchSizeLimitExceeded(batch_size)

        for entity_batch in split_batches(entities, batch_size):
            self.client.put_multi([entity.get_datastore_entity() for entity in entity_batch])

    def generate_key(self, kind: str, identifier: str, parent_key: Key = None):
        return self.client.key(kind, identifier, parent=parent_key)
