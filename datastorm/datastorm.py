import os
from typing import List

from google.cloud import datastore
from google.cloud.datastore import Key

from datastorm.objects import BaseEntity, AbstractDSEntity


class DataStorm:

    def __init__(self, project=None, namespace=None, credentials=None, _http=None, _use_grpc=None):
        self.project = project or os.getenv("DATASTORE_PROJECT_ID", None)
        self.credentials = credentials
        self.namespace = namespace
        self._http = _http
        self._use_grpc = _use_grpc

    @property
    def client(self):
        return datastore.Client(project=self.project, namespace=self.namespace, credentials=self.credentials,
                                _http=self._http, _use_grpc=self._use_grpc)

    @property
    def DSEntity(self):
        return AbstractDSEntity("DSEntity", (BaseEntity,), {'__kind__': None, '__datastorm_client__': self.client})

    def save_multi(self, entities: List[BaseEntity]):
        [entity._save_offline() for entity in entities]
        self.client.put_multi([entity.get_raw_entity() for entity in entities])

    def generate_key(self, kind: str, identifier: str, parent_key: Key = None):
        return self.client.key(kind, identifier, parent=parent_key)
