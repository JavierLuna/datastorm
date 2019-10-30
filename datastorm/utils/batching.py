from typing import List, TypeVar
import math

T = TypeVar('T')


def split_batches(entities: List[T], batch_size: int) -> List[List[T]]:
    batches = []
    n_batches = math.ceil(len(entities) / batch_size)
    for batch_number in range(n_batches):
        batches.append(entities[batch_size * batch_number: min(batch_size * (batch_number + 1), len(entities))])
    return batches
