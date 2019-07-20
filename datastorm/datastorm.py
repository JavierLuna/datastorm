import os
from typing import List

from google.cloud import datastore
from google.cloud.datastore import Key

from datastorm.entity import BaseEntity, AbstractDSEntity


class DataStorm:

    def __init__(self, project=None, namespace=None, credentials=None):
        self.project = project or os.getenv("DATASTORE_PROJECT_ID", None)
        self.credentials = credentials
        self.namespace = namespace

    @property
    def client(self):
        return datastore.Client(project=self.project, namespace=self.namespace, credentials=self.credentials)

    @property
    def DSEntity(self):
        return AbstractDSEntity("DSEntity", (BaseEntity,), {'__kind__': None, '_datastore_client': self.client})

    def save_multi(self, entities: List[BaseEntity]):
        [entity._save_offline() for entity in entities]
        self.client.put_multi([entity.get_raw_entity() for entity in entities])

    def generate_key(self, kind: str, identifier: str, parent_key: Key = None):
        return self.client.key(kind, identifier, parent=parent_key)
