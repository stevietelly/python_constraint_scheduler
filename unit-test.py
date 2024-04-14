"""Pytest Compatible Tests"""
import os
from types import NoneType
from typing import List
from Data.Validators.Formation import DataValidator
from cli import generate_instructors, generate_rooms, generate_students, generate_units, write_data_file


def test_generate_instructors():
    """Test generate Instructors"""
    assert generate_instructors(3) == [
        {"id": 1, "preferences": None},
        {"id": 2, "preferences": None},
        {"id": 3, "preferences": None},
    ]

def test_generate_rooms():
    """Test Generate Rooms"""
    assert DataValidator(
        {"id": int, "capacity": int, "preferences": (NoneType, str)}, generate_rooms(1)
    ).Validate()

def test_generate_students():
    """Test Generate STudents"""
    assert DataValidator(
        {"id": int, "units": List[int], "total": int, "preferences": (NoneType, str)},
        generate_students(5, 5),
    )

def test_generate_units():
    assert DataValidator({'id': int, 'preferences': (str, NoneType),
                          'instructors': List[int]}, generate_units(5, 5)
                          )

def test_write_data_file():
    write_data_file("abcde.json")
    assert os.path.exists("abcde.json")
    os.remove("abcde.json")

