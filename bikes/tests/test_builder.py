import unittest
from bikes.builder import RegularBikeBuilder, ElectricBikeBuilder, Director

class TestBikeBuilder(unittest.TestCase):
    def test_regular_bike_builder_creates_correct_parts(self):
        builder = RegularBikeBuilder()
        director = Director(builder)
        bike = director.build_bike()
        self.assertIn("Regular Frame", bike.parts)
        self.assertIn("Standard Wheels", bike.parts)
        self.assertNotIn("Motor", bike.parts)

    def test_electric_bike_builder_creates_correct_parts(self):
        builder = ElectricBikeBuilder()
        director = Director(builder)
        bike = director.build_bike()
        self.assertIn("Electric Frame", bike.parts)
        self.assertIn("Electric Wheels", bike.parts)
        self.assertIn("Motor", bike.parts)

    def test_show_method_returns_string(self):
        builder = ElectricBikeBuilder()
        director = Director(builder)
        bike = director.build_bike()
        result = bike.show()
        self.assertIsInstance(result, str)
        self.assertIn("Electric Frame", result)

    def test_add_part_appends_to_list(self):
        from bikes.builder import Bike
        bike = Bike()
        bike.add_part("Test Part")
        self.assertIn("Test Part", bike.parts)
