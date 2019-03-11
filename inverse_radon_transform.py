from bresenham import Bresenham
from tomograph import Tomograph
from point import Point
import numpy as np


class InverseRadonTransform:
    def transform(self, sinogram, tomograph: Tomograph):
        image_size = (tomograph.width, tomograph.height)
        image = np.zeros(image_size)
        lines_quantity_per_pixel = np.zeros(image_size)

        rays_quantity = len(sinogram)
        detectors_quantity = len(sinogram[0])
        for vector_number in range(0, rays_quantity):
            self.__transform_vector(image, lines_quantity_per_pixel, detectors_quantity, sinogram, tomograph,
                                    vector_number)
        self.normalize_image(image, lines_quantity_per_pixel)
        return image

    def __transform_vector(self, image: [[float]], lines_quantity_per_pixel: [[int]], detectors_quantity: int, sinogram,
                           tomograph: Tomograph, vector_number: int):
        for detector_number in range(0, detectors_quantity):
            section = tomograph.get_ray(vector_number, detector_number)
            image_points = Bresenham().get_image_points(section.start_point, section.end_point, tomograph.width,
                                                        tomograph.height)
            self.__transform_value(image, lines_quantity_per_pixel, image_points,
                                   sinogram[vector_number][detector_number])

    def normalize_image(self, image: [[float]], lines_quantity_per_pixel: [[int]]):
        for i in range(0, len(lines_quantity_per_pixel)):
            for j in range(0, len(lines_quantity_per_pixel[0])):
                if lines_quantity_per_pixel[i][j] > 0:
                    image[i][j] = image[i][j] / lines_quantity_per_pixel[i][j]

    def __transform_value(self, image: [[float]], lines_quantity_per_pixel: [[int]], image_points: [Point],
                          sinogram_value: float):
        for point in image_points:
            image[point.x][point.y] += sinogram_value
            lines_quantity_per_pixel[point.x][point.y] += 1
