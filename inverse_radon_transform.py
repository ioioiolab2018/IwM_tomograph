from bresenham import Bresenham
from tomograph import Tomograph
from point import Point
import numpy as np


class InverseRadonTransform:
    def transform(self, sinogram: [[float]], tomograph: Tomograph):
        image_size = (tomograph.image_width, tomograph.image_height)
        image = np.zeros(image_size)
        lines_quantity_per_pixel = np.zeros(image_size)

        rays_quantity = len(sinogram)
        detectors_quantity = len(sinogram[0])
        for sinogram_vector_number in range(0, rays_quantity):
            self.__transform_vector(image, lines_quantity_per_pixel, detectors_quantity, sinogram, tomograph,
                                    sinogram_vector_number)
        return self.normalize_image(image, lines_quantity_per_pixel)

    def __transform_vector(self, image: [[float]], lines_quantity_per_pixel: [[int]], detectors_quantity: int,
                           sinogram: [[float]], tomograph: Tomograph, vector_number: int):
        for detector_number in range(0, detectors_quantity):
            section = tomograph.get_ray(vector_number, detector_number)
            image_points = Bresenham().get_image_points(section.start_point, section.end_point, tomograph.image_width,
                                                        tomograph.image_height)
            self.__transform_value(image, lines_quantity_per_pixel, image_points,
                                   sinogram[vector_number][detector_number])

    def normalize_image(self, image: [[float]], lines_quantity_per_pixel: [[int]]):
        result = np.zeros(image.shape)
        for i in range(0, len(lines_quantity_per_pixel)):
            for j in range(0, len(lines_quantity_per_pixel[0])):
                if lines_quantity_per_pixel[i][j] > 0:
                    result[i][j] = (image[i][j] / lines_quantity_per_pixel[i][j])
        return result

    def __transform_value(self, image: [[float]], lines_quantity_per_pixel: [[int]], image_points: [Point],
                          sinogram_value: float):
        for point in image_points:
            image[point.x][point.y] += sinogram_value
            lines_quantity_per_pixel[point.x][point.y] += 1

    def get_partial_result(self, sinogram: [[float]], tomograph: Tomograph, progress: int, image: [[float]] = None,
                           lines_quantity_per_pixel: [[int]] = None, start: int = 0):
        image_size = (tomograph.image_width, tomograph.image_height)
        if image is None or lines_quantity_per_pixel is None:
            image = np.zeros(image_size)
            lines_quantity_per_pixel = np.zeros(image_size)
        detectors_quantity = len(sinogram[0])

        for iteration in range(start, progress):
            self.__transform_vector(image, lines_quantity_per_pixel, detectors_quantity, sinogram, tomograph, iteration)
        return image, lines_quantity_per_pixel
