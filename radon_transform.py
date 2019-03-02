from numpy.core.multiarray import ndarray

from bresenham import Bresenham
from section import Section
from tomograph import Tomograph
import numpy as np
import math


class RadonTransform:
    def transform(self, image, tomograph: Tomograph):
        iteration_no = math.floor(360 / tomograph.dAlpha)
        sinogram = []
        for i in range(0, iteration_no):
            print(i)
            sinogram_vector = []
            for j in range(0, tomograph.n):
                section = tomograph.get_ray(i, j)
                image_points = Bresenham().get_points(section.start_point, section.end_point)
                # image_points = self.__filter_image_points(len(image), len(image[0]), image_points)
                sinogram_vector.append(self.__calculate_sinogram_value(image, image_points))
            sinogram.append(sinogram_vector)
        return sinogram

    def inverse_transform(self, sinogram, tomograph: Tomograph):
        size = (tomograph.width, tomograph.height)
        iteration = len(sinogram)
        detectors_no = len(sinogram[0])
        print(iteration)
        print("aaaaaaaaaa")
        print(detectors_no)
        image = np.zeros(size)
        counter = np.zeros(size)
        for i in range(0, iteration):
            for d in range(0, detectors_no):
                section = tomograph.get_ray(i, d)
                image_points = Bresenham().get_points(section.start_point, section.end_point)
                # image_points = self.__filter_image_points(size[1], size[0], image_points)
                for point in image_points:
                    if point.x < size[0] and point.y < size[1]:
                        image[point.x][point.y] += sinogram[i][d]
                        counter[point.x][point.y] += 1
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                if counter[i][j] > 0:
                    image[i][j] = image[i][j] / counter[i][j]

        return image

    def __get_sections(self, emitter_position, detector_positions):
        sections = []
        for position in detector_positions:
            sections.append(Section(emitter_position, position))
        return sections

    # def __filter_image_points(self, image_height, image_width, points):
    #     x = image_width
    #     y = image_height
    #     image_points = []
    #     for point in points:
    #         image_points.append(point)
    #     return image_points

    def __calculate_sinogram_value(self, image, points):
        points_sum = 0
        x = len(image[1])
        y = len(image)
        n = 0
        for point in points:
            if point.x < x and point.y < y:
                points_sum += image[point.y][point.x]
                n += 1
        if n > 0:
            return points_sum / n
        return 0
