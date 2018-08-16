import unittest

import requests
from google.auth.credentials import Credentials

from datastorm import DataStorm


class EmulatorCreds(Credentials):
    """A mock credential object.
    Used to avoid unnecessary token refreshing or reliance on the network
    while an emulator is running.
    """

    def __init__(self):  # pylint: disable=super-init-not-called
        self.token = b'seekrit'
        self.expiry = None

    @property
    def valid(self):
        """Would-be validity check of the credentials.
        Always is :data:`True`.
        """
        return True

    def refresh(self, unused_request):  # pylint: disable=unused-argument
        """Off-limits implementation for abstract method."""
        raise RuntimeError('Should never be refreshed.')


class TestBase(unittest.TestCase):
    TEST_PROJECT_ID = "tests"
    DUMMY_CREDENTIALS = EmulatorCreds
    _HTTP = requests.Session

    def setUp(self):
        self.datastorm = DataStorm(TestBase.TEST_PROJECT_ID, credentials=TestBase.DUMMY_CREDENTIALS(),
                                   _http=TestBase._HTTP())

        class TestEntity1(self.datastorm.DSEntity):
            __kind__ = "TestEntity1"

            dict_field = dict()
            list_field = list()

        self.TestEntity1 = TestEntity1

    def tearDown(self):
        [entity.delete() for entity in self.TestEntity1.query.all()]
