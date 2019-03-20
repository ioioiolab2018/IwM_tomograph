from tomograph import InverseRadonTransform, RadonTransform, RayCalculator, Convolution
from skimage import color, io, img_as_float32, img_as_ubyte
import math


class God:
    tomograph = None
    sinogram_n = None
    iteration_no = None
    sinogram = None
    filtered_sinogram = None
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
        self.image = img_as_ubyte(color.rgb2gray(io.imread(filename)))

    def restart(self, n, alpha, arc_len):
        self.tomograph = RayCalculator(self.image.shape[0], self.image.shape[1], n, alpha, arc_len)
        self.iteration_no = math.floor(360 / alpha)
        self.result_n = -1
        self.sinogram_n = -1
        self.sinogram = []
        self.filtered_sinogram = None
        self.zeros = []
        for i in range(n):
            self.zeros.append(0)
        self.radon = RadonTransform()

    def restart_result(self):
        self.results = []
        self.result_n = 0

    def set_filtering(self, filtering: bool):
        print("###########", filtering)
        self.is_filtering = filtering
        self.restart_result()

    def get_sinogram(self, progress):
        if progress > self.sinogram_n:
            for i in range(self.sinogram_n, progress):
                self.sinogram.append(self.radon.get_singoram_vector(self.image, self.tomograph, i))
            self.sinogram_n = progress
        result = []
        for i in range(progress):
            result.append(self.sinogram[i])
        for i in range(progress, self.iteration_no - 1):
            result.append(self.zeros)
        return result

    def filterImage(self, sinogram, mask=None):
        return Convolution().transform(sinogram, mask)

    def get_inverse_result(self, progres: int):

        if self.sinogram_n < progres:
            self.get_sinogram(progres)

        sinogram_copy = None

        if self.is_filtering:
            if self.filtered_sinogram is None:
                self.filtered_sinogram = self.filterImage(self.sinogram.copy())
            sinogram_copy = self.filtered_sinogram
        else:
            sinogram_copy = self.sinogram.copy()

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
                image, counter = InverseRadonTransform().get_partial_result(sinogram_copy, self.tomograph,
                                                                            progres)
            else:
                image, counter = InverseRadonTransform().get_partial_result(sinogram_copy, self.tomograph,
                                                                            progres,
                                                                            partial_result[1].copy(),
                                                                            partial_result[2].copy(),
                                                                            partial_result[0])

            self.results.append([progres, image, counter])
            return InverseRadonTransform().normalize_image(image, counter)
