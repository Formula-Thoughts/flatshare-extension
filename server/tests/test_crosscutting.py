import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import get_args
from unittest import TestCase

from server.src.crosscutting import AutoFixture, ObjectMapper


class TestEnum(Enum):
    VALUE1 = "VALUE1"
    VALUE2 = "VALUE2"


@dataclass(unsafe_hash=True)
class InheritedDto:
    id: str = field(default_factory=lambda: "default_id")
    name: str = None


@dataclass(unsafe_hash=True)
class NestedTestOtherDto:
    id: str = None
    name: str = None


@dataclass(unsafe_hash=True)
class TestOtherDto:
    id: str = None
    name: str = None
    bool_: bool = None
    enum: TestEnum = None
    list_of_enums: list[TestEnum] = None
    list_of_strings: list[str] = None
    list_of_ints: list[int] = None
    list_of_floats: list[float] = None
    list_of_bools: list[bool] = None
    date: datetime.datetime = None
    list_of_dates: list[datetime.datetime] = None
    decimal_num: float = None
    nested: NestedTestOtherDto = None
    nested_list: list[NestedTestOtherDto] = None


@dataclass(unsafe_hash=True)
class NestedTestDto:
    id: str = None
    name: str = None


@dataclass(unsafe_hash=True)
class TestDto(InheritedDto):
    bool_: bool = None
    enum: TestEnum = None
    list_of_enums: list[TestEnum] = None
    list_of_strings: list[str] = None
    list_of_ints: list[int] = None
    list_of_floats: list[float] = None
    list_of_bools: list[bool] = None
    date: datetime.datetime = None
    list_of_dates: list[datetime.datetime] = None
    decimal_num: float = None
    nested: NestedTestDto = None
    nested_list: list[NestedTestDto] = None


class TestPinfluencerMapper(TestCase):

    def test_map(self):
        # arrange
        test_dto = AutoFixture().create(dto=TestDto,
                                        list_limit=5)

        # act
        test_other_dto: TestOtherDto = ObjectMapper().map(_from=test_dto, to=TestOtherDto)

        # assert
        with self.subTest(msg="id with default value matches"):
            assert test_other_dto.id == "default_id"

        # assert
        with self.subTest(msg="date field matches"):
            assert test_other_dto.date == test_dto.date

        # assert
        with self.subTest(msg="list of dates field matches"):
            assert test_other_dto.list_of_dates == test_dto.list_of_dates

        # assert
        with self.subTest(msg="name field matches"):
            assert test_other_dto.name == test_dto.name

        # assert
        with self.subTest(msg="nested list types match"):
            self.assertEqual(get_args(list[NestedTestDto])[0], type(test_dto.nested_list[0]))

        # assert
        with self.subTest(msg="nested list types match"):
            self.assertEqual(get_args(list[NestedTestOtherDto])[0], type(test_other_dto.nested_list[0]))

        # assert
        with self.subTest(msg="nested list lengths match"):
            self.assertEqual(len(test_dto.nested_list), len(test_other_dto.nested_list))

        # assert
        with self.subTest(msg="nested list field matches"):
            for i in range(0, len(test_other_dto.nested_list)):
                self.assertEqual(test_other_dto.nested_list[i].__dict__, test_dto.nested_list[i].__dict__)

        # assert
        with self.subTest(msg="nested id field matches"):
            assert test_other_dto.nested.id == test_dto.nested.id

        # assert
        with self.subTest(msg="nested name field matches"):
            assert test_other_dto.nested.name == test_dto.nested.name

        # assert
        with self.subTest(msg="list of dates field matches"):
            assert test_other_dto.list_of_dates == test_dto.list_of_dates

        # assert
        with self.subTest(msg="list of bools field matches"):
            assert test_other_dto.list_of_bools == test_dto.list_of_bools

        # assert
        with self.subTest(msg="list of ints field matches"):
            assert test_other_dto.list_of_ints == test_dto.list_of_ints

        # assert
        with self.subTest(msg="bool field matches"):
            assert test_other_dto.bool_ == test_dto.bool_

        # assert
        with self.subTest(msg="list of strings field matches"):
            assert test_other_dto.list_of_strings == test_dto.list_of_strings

        # assert
        with self.subTest(msg="list of enums field matches"):
            assert test_other_dto.list_of_enums == test_dto.list_of_enums

        # assert
        with self.subTest(msg="enum field matches"):
            assert test_other_dto.enum == test_dto.enum

        # assert
        with self.subTest(msg="decimal field matches"):
            assert test_other_dto.decimal_num == test_dto.decimal_num

        # assert
        with self.subTest(msg="list of floats field matches"):
            assert test_other_dto.list_of_floats == test_dto.list_of_floats


class TestAutoFixture(TestCase):

    def test_create(self):
        # arrange
        autofixture = AutoFixture()

        # act
        dto: TestDto = autofixture.create(dto=TestDto,
                                          seed="1234",
                                          num=2)

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(dto.id, "default_id")

        with self.subTest(msg="names match"):
            self.assertEqual(dto.name, "name1234")

        with self.subTest(msg="bools match"):
            self.assertTrue(dto.bool_)

        with self.subTest(msg="enums match"):
            self.assertEqual(dto.enum, TestEnum.VALUE1)

        with self.subTest(msg="enum lists match"):
            self.assertEqual(dto.list_of_enums, [TestEnum.VALUE1, TestEnum.VALUE1])

        with self.subTest(msg="string lists match"):
            self.assertEqual(dto.list_of_strings, ["list_of_strings12340", "list_of_strings12341"])

        with self.subTest(msg="int lists match"):
            self.assertEqual(dto.list_of_ints, [2, 3])

        with self.subTest(msg="bool lists match"):
            self.assertEqual(dto.list_of_bools, [True, True])

        with self.subTest(msg="dates match"):
            self.assertEqual(dto.date.year, 2)
            self.assertEqual(dto.date.month, 2)
            self.assertEqual(dto.date.day, 2)
            self.assertEqual(dto.date.hour, 2)
            self.assertEqual(dto.date.minute, 2)
            self.assertEqual(dto.date.second, 2)

        with self.subTest(msg="date lists match"):
            self.assertEqual(dto.list_of_dates[0].year, 2)
            self.assertEqual(dto.list_of_dates[0].month, 2)
            self.assertEqual(dto.list_of_dates[0].day, 2)
            self.assertEqual(dto.list_of_dates[0].hour, 2)
            self.assertEqual(dto.list_of_dates[0].minute, 2)
            self.assertEqual(dto.list_of_dates[0].second, 2)

            self.assertEqual(dto.list_of_dates[1].year, 2)
            self.assertEqual(dto.list_of_dates[1].month, 2)
            self.assertEqual(dto.list_of_dates[1].day, 2)
            self.assertEqual(dto.list_of_dates[1].hour, 2)
            self.assertEqual(dto.list_of_dates[1].minute, 2)
            self.assertEqual(dto.list_of_dates[1].second, 2)

        with self.subTest(msg="nested objects match"):
            self.assertEqual(dto.decimal_num, 2.22)
            self.assertEqual(dto.nested.id, "id1234")
            self.assertEqual(dto.nested.name, "name1234")

        with self.subTest(msg="nested objects list match"):
            self.assertEqual(dto.nested_list[0].id, "id1234")
            self.assertEqual(dto.nested_list[0].name, "name1234")
            self.assertEqual(dto.nested_list[1].id, "id1234")
            self.assertEqual(dto.nested_list[1].name, "name1234")