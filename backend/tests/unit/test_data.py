from decimal import Decimal
from unittest import TestCase

from attr import dataclass
from formula_thoughts_web.crosscutting import JsonSnakeToCamelSerializer, ObjectMapper

from src.infra import ObjectHasher


@dataclass(unsafe_hash=True)
class TestModel:
    prop1: int = None
    prop2: str = None
    prop3: Decimal = None


class ObjectHasherTestCase(TestCase):

    def setUp(self):
        self.__sut = ObjectHasher(serializer=JsonSnakeToCamelSerializer(),
                                  object_mapper=ObjectMapper())

    def test_hash_should_hash_object(self):
        object = TestModel(prop1=123, prop2="test", prop3=Decimal("123.2"))
        hash = self.__sut.hash(object=object)

        with self.subTest(msg="hash should be md5 of object"):
            self.assertEqual("36b84f7fd9583486019daf32a325204b", hash)
