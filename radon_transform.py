from bresenham import Bresenham
from section import Section
from point import Point
from tomograph import Tomograph
import math
import time


class RadonTransform:
    def transform(self, image, tomograph: Tomograph):
        iteration_no = math.floor(360 / tomograph.dAlpha)
        sinogram = []
        for position_number in range(0, iteration_no):
            print(position_number)
            sinogram_vector = self.get_singoram_vector(image, tomograph, position_number)
            sinogram.append(sinogram_vector)
        return sinogram

    def get_singoram_vector(self, image, tomograph: Tomograph, position_number):
        sinogram_vector = []
        for j in range(0, tomograph.n):
            # start1 = time.clock()
            section = tomograph.get_ray(position_number, j)
            # end1 = time.clock()
            # start2 = time.clock()
            sinogram_vector.append(self.get_sinogram_value(image, section))
            # end2 = time.clock()
            # print('CALCULATE_RAY_TIME: ' + str(end1 - start1))
            # print('CALCULATE_VALUE_TIME: ' + str(end2 - start2))
        return sinogram_vector

    def get_sinogram_value(self, image, section: Section):
        image_height = len(image)
        image_width = len(image[0])
        # start1 = time.clock()
        image_points = Bresenham().get_image_points(section.start_point, section.end_point, image_width, image_height)
        # end1 = time.clock()
        # start2 = time.clock()
        value = self.__calculate_sinogram_value(image, image_points)
        # end2 = time.clock()
        # print('BRESENHAM_TIME: ' + str(end1 - start1))
        # print('CALCULATE_VALUE_TIME: ' + str(end2 - start2))
        return value

    def __calculate_sinogram_value(self, image, points: [Point]):
        points_sum = 0
        for point in points:
            points_sum += image[point.y][point.x]
        if len(points) > 0:
            return points_sum / len(points)
        return 0
