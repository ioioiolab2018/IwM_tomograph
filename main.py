from bresenham import Bresenham
from point import Point
from radon_transform import RadonTransform
from inverse_radon_transform import InverseRadonTransform
from convolution import Convolution
from tomograph import Tomograph
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
import numpy as np
from skimage.transform import resize

img = color.rgb2gray(io.imread('image.png'))
arr = np.asarray(img)
plt.imshow(arr, cmap='gray')
plt.show()
print(arr.shape)

# x = Bresenham()
# start_point = Point(1, 0)
# end_point = Point(2, 3)
# result = x.get_points(start_point, end_point)

# for point in result:
#     print('X: ' + str(point.x) + '  Y: ' + str(point.y))
#

# n = 400
# alpha = 0.7
# tomograph = Tomograph(alpha, n, 90, arr.shape[0], arr.shape[1])

n = 300
alpha = 0.5
tomograph = Tomograph(arr.shape[0], arr.shape[1], n, alpha, 300)

# x = []
# y = []
# for i in range(0, 360):
#     for d in range(0, 3):
#         wynik = tomograph.get_ray(i, d)
#         x.append(wynik.end_point.x)
#         y.append(wynik.end_point.y)
#
# plt.plot(x, y, 'ro')
# plt.show()

sinogram = RadonTransform().transform(arr, tomograph)
sinogram = Convolution().transform(sinogram, [-1, 3, -1])

arr2 = np.asarray(sinogram)
arr2 = np.transpose(arr2)
image = resize(arr2, (100, 200), mode='constant', anti_aliasing=False)
plt.imshow(image, cmap='gray')
plt.show()

result = InverseRadonTransform().transform(sinogram, tomograph)
plt.imshow(result, cmap='gray')
plt.show()
