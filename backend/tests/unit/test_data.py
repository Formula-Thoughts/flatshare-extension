from unittest import TestCase

from attr import dataclass
from formula_thoughts_web.crosscutting import JsonSnakeToCamelSerializer, ObjectMapper

from src.data import ObjectHasher


@dataclass(unsafe_hash=True)
class TestModel:
    prop1: int = None
    prop2: str = None


class ObjectHasherTestCase(TestCase):

    def setUp(self):
        self.__sut = ObjectHasher(serializer=JsonSnakeToCamelSerializer(),
                                  object_mapper=ObjectMapper())

    def test_hash_should_hash_object(self):
        object = TestModel(prop1=123, prop2="test")
        hash = self.__sut.hash(object=object)

        with self.subTest(msg="hash should be md5 of object"):
            self.assertEqual("c9a4a0665a56e57b9d1a63ded7bcc8e0", hash)
