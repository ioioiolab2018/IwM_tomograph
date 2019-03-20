from tomograph import Tomograph
from radon_transform import RadonTransform
from inverse_radon_transform import InverseRadonTransform
from skimage import color
from skimage import io
import math
import numpy as np


class God:
    tomograph = None
    sinogram_n = None
    iteration_no = None
    sinogram = None
    image = None
    zeros = None
    radon = None
    is_filtering = None
    result_n = None
    results = None

    def __init__(self, image_filename, n, alpha, arc_len):
        self.read_image(image_filename)
        self.restart(n, alpha, arc_len)
        self.restart_result()

    def read_image(self, filename):
        self.image = color.rgb2gray(io.imread(filename))

    def restart(self, n, alpha, arc_len):
        self.tomograph = Tomograph(self.image.shape[0], self.image.shape[1], n, alpha, arc_len)
        self.iteration_no = math.floor(360 / alpha)
        self.result_n = -1
        self.sinogram_n = -1
        self.sinogram = []
        self.zeros = []
        for i in range(n):
            self.zeros.append(0)
        self.radon = RadonTransform()

    def restart_result(self):
        self.results = []
        self.result_n = 0

    def set_filtering(self, filtering: bool):
        self.is_filtering = filtering
        self.restart_result()

    def get_sinogram(self, progres):
        if progres > self.sinogram_n:
            for i in range(self.sinogram_n, progres):
                self.sinogram.append(self.radon.get_singoram_vector(self.image, self.tomograph, i))
            self.sinogram_n = progres
        result = []
        for i in range(progres):
            result.append(self.sinogram[i])
        for i in range(progres, self.iteration_no - 1):
            result.append(self.zeros)
        return result

    def get_inverse_result(self, progres: int):
        if self.sinogram_n < progres:
            self.get_sinogram(progres)
        partial_result = None
        is_done = False
        for result in self.results:
            if result[0] <= progres and (partial_result is None or partial_result[0] < result[0]):
                partial_result = result
                if result[0] == progres:
                    is_done = True
                    break
        if is_done:
            return InverseRadonTransform().normalize_image(partial_result[1], partial_result[2])
        else:
            if partial_result is None:
                image, counter = InverseRadonTransform().get_partial_result(self.sinogram, self.tomograph,
                                                                            progres)
            else:
                image, counter = InverseRadonTransform().get_partial_result(self.sinogram, self.tomograph,
                                                                            progres,
                                                                            partial_result[1].copy(),
                                                                            partial_result[2].copy(),
                                                                            partial_result[0])

            self.results.append([progres, image, counter])
            return InverseRadonTransform().normalize_image(image, counter)
