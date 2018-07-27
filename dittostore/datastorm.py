from typing import List

from google.cloud import datastore
from google.cloud.datastore import Key

from dittostore.objects import BaseEntity, AbstractDSEntity


class DittoStore:

    def __init__(self, project):
        self.project = project

    @property
    def DSEntity(self):
        return AbstractDSEntity("DSEntity", (BaseEntity,), {'__kind__': None, '__project__': self.project})

    def save_multi(self, entities : List[BaseEntity], exclude_from_indexes=()):
        client = datastore.Client(project=self.project)
        [entity._save_offline(exclude_from_indexes=exclude_from_indexes) for entity in entities]
        client.put_multi([entity.get_raw_entity() for entity in entities])

    def generate_key(self, kind: str, identifier: str, parent_key: Key = None):
        return datastore.Client(project=self.project).key(kind, identifier, parent=parent_key)
