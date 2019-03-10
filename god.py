from tomograph import Tomograph
from radon_transform import RadonTransform
from skimage import color
from skimage import io
import math


class God:
    tomnograph = None
    sinogram_n = None
    result_n = None
    iteration_no = None
    sinogram = None
    image = None
    zeros = None
    radon = None

    def __init__(self, image_filename, n, alpha, arc_len):
        self.read_image(image_filename)
        self.restart(n, alpha, arc_len)

    def read_image(self, filename):
        self.image = color.rgb2gray(io.imread(filename))

    def restart(self, n, alpha, arc_len):
        self.tomograph = Tomograph(alpha, n, arc_len, self.image.shape[0], self.image.shape[1])
        self.iteration_no =  math.floor(360 / alpha)
        self.result_n = 0
        self.sinogram_n = -1
        self.sinogram = []
        self.zeros = []
        for i in range(n):
            self.zeros.append(0)
        self.radon = RadonTransform()

    def get_sinogram(self, progres):
        if progres > self.sinogram_n:
            for i in range(self.sinogram_n, progres):
                self.sinogram.append(self.radon.get_singoram_vector(self.image, self.tomograph, i))
            self.sinogram_n = progres
        result = []
        for i in range(progres):
            result.append(self.sinogram[i])
        for i in range(progres, self.iteration_no-1):
            result.append(self.zeros)
        return result
