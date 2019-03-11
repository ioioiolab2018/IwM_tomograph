from section import Section
from point import Point
from math import *


class Tomograph:
    dAlpha = None
    n = None
    arcLenght = None
    height = None
    width = None

    def get_ray(self, iteration, detector_no):
        r = sqrt(self.height ** 2 + self.width ** 2) / 2
        # print('RADIUS: ' + str(r))
        emiter = Point(r * sin(radians(iteration*self.dAlpha)),
                       r * cos(radians(iteration*self.dAlpha)))
        # print('EMITER:' + '\n\tX: ' + str(emiter.x) + '\n\tY: ' + str(emiter.y))
        opposite_point = Point(-emiter.x, -emiter.y)
        # print('OPOSITE_POINT:' + '\n\tX: ' + str(opposite_point.x) + '\n\tY: ' + str(opposite_point.y))
        alpha = radians(self.arcLenght) / 2 - detector_no * (radians(self.arcLenght) / (self.n - 1))
        detector_x = opposite_point.x * cos(alpha) - opposite_point.y * sin(alpha)
        detector_y = opposite_point.x * sin(alpha) + opposite_point.y * cos(alpha)
        detector = Point(floor(detector_x+self.width/2), floor(detector_y+self.height/2))
        # print('DETECTOR:' + '\n\tX: ' + str(detector_x) + '\n\tY: ' + str(detector_y))
        emiter.x = floor(emiter.x+self.width/2)
        emiter.y = floor(emiter.y+self.height/2)
        return Section(emiter, detector)

    def __init__(self, d_alpha, n, arc_lenght, height, width):
        self.dAlpha = d_alpha
        self.n = n
        self.arcLenght = arc_lenght
        self.width = width
        self.height = height
