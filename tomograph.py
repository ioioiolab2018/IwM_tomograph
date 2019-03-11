from section import Section
from point import Point
from math import *


class Tomograph:
    image_height = None
    image_width = None
    detectors_quantity = None
    shifting_angle = None
    spread = None

    def get_ray(self, shift_number, detector_number):
        radius = self.__calculate_radius()
        emitter_position = self.__calculate_emitter_position_relative_to_coordinate_system_center(radius, shift_number)
        displacement_angle = self.__calculate_the_detectors_shift_angle(detector_number)
        detector = self.__calculate_detector_position(emitter_position, displacement_angle)
        self.__shift_emitter_to_right_position(emitter_position)
        return Section(emitter_position, detector)

    def __calculate_radius(self):
        return sqrt(self.image_height ** 2 + self.image_width ** 2) / 2

    def __calculate_emitter_position_relative_to_coordinate_system_center(self, radius: float, shift_number: int):
        x = radius * sin(radians(shift_number * self.shifting_angle))
        y = radius * cos(radians(shift_number * self.shifting_angle))
        return Point(x, y)

    def __calculate_the_detectors_shift_angle(self, detector_number):
        return radians(self.spread) / 2 - detector_number * (radians(self.spread) / (self.detectors_quantity - 1))

    def __calculate_detector_position(self, emitter_position, displacement_angle):
        x = (-emitter_position.x) * cos(displacement_angle) + emitter_position.y * sin(displacement_angle)
        y = (-emitter_position.x) * sin(displacement_angle) - emitter_position.y * cos(displacement_angle)
        return Point(floor(x + self.image_width / 2), floor(y + self.image_height / 2))

    def __shift_emitter_to_right_position(self, emitter_position):
        emitter_position.x = floor(emitter_position.x + self.image_width / 2)
        emitter_position.y = floor(emitter_position.y + self.image_height / 2)

    def __init__(self, height, width, detectors_quantity, shifting_angle, system_spread):
        self.image_height = height
        self.image_width = width
        self.detectors_quantity = detectors_quantity
        self.shifting_angle = shifting_angle
        self.spread = system_spread
