from abc import ABC, abstractmethod


class Bike:
    def __init__(self):
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)

    def show(self):
        return ", ".join(self.parts)


class Builder(ABC):
    @abstractmethod
    def add_frame(self):
        pass

    @abstractmethod
    def add_wheels(self):
        pass

    @abstractmethod
    def add_motor(self):
        pass

    @abstractmethod
    def get_bike(self):
        pass


class RegularBikeBuilder(Builder):
    def __init__(self):
        self.bike = Bike()

    def add_frame(self):
        self.bike.add_part("Regular Frame")

    def add_wheels(self):
        self.bike.add_part("Standard Wheels")

    def add_motor(self):
        pass

    def get_bike(self):
        return self.bike


class ElectricBikeBuilder(Builder):
    def __init__(self):
        self.bike = Bike()

    def add_frame(self):
        self.bike.add_part("Electric Frame")

    def add_wheels(self):
        self.bike.add_part("Electric Wheels")

    def add_motor(self):
        self.bike.add_part("Motor")

    def get_bike(self):
        return self.bike


class Director:
    def __init__(self, builder: Builder):
        self.builder = builder

    def build_bike(self):
        self.builder.add_frame()
        self.builder.add_wheels()
        self.builder.add_motor()
        return self.builder.get_bike()
