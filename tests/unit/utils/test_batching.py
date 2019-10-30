import pytest

from datastorm.utils.batching import split_batches


@pytest.mark.parametrize("n_entities, batch_size, n_expected_batches", [(2, 1, 2),
                                                                        (1, 2, 1),
                                                                        (1, 1, 1)])
def test_batching(n_entities, batch_size, n_expected_batches):
    entities = [None] * n_entities
    batches = split_batches(entities, batch_size=batch_size)
    assert len(batches) == n_expected_batches
