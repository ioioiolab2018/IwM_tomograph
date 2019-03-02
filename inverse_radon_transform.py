from bresenham import Bresenham
from tomograph import Tomograph
import numpy as np


class InverseRadonTransform:
    def transform(self, sinogram, tomograph: Tomograph):
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
                image_points = Bresenham().get_image_points(section.start_point, section.end_point, tomograph.width,
                                                            tomograph.height)
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
