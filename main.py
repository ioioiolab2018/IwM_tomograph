from tomograph import *
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
import numpy as np
from skimage.transform import resize
from skimage.util import img_as_int, img_as_ubyte, img_as_float, img_as_uint

# img = color.rgb2gray(io.imread('images/Sin.png'))
img = color.rgb2gray(io.imread('images/picbrain.jpg'))
print('image: ', max([max(sublist) for sublist in img]))
img = img_as_ubyte(img)
print('image_as_ubyte: ', max([max(sublist) for sublist in img]))
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

n = 50
alpha = 2
tomograph = RayCalculator(arr.shape[0], arr.shape[1], n, alpha, 300)

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
sinogram = Convolution().transform(sinogram)

arr2 = np.asarray(sinogram)
print('arr2: ', max([max(sublist) for sublist in arr2]))
arr2 = np.transpose(arr2)
image = resize(arr2, (100, 200), mode='constant', anti_aliasing=False)
plt.imshow(image, cmap='gray')
plt.show()

print('sinogram: ', max([max(sublist) for sublist in sinogram]))
result = InverseRadonTransform().transform(sinogram, tomograph)
print('result: ', max([max(sublist) for sublist in result]))
plt.imshow(result, cmap='gray')
plt.show()
# print(result)
DICOMSaver().save(img_as_uint(np.asarray(result, dtype=np.uint8)), 'pretty', PatientInformation())
DICOMSaver().save_test(img_as_uint(np.asarray(result, dtype=np.uint8)), 'pretty1')
# DICOMSaver().save_test(img_as_ubyte(np.asarray(result, dtype=np.uint8)), 'pretty2')
# DICOMSaver().save_test(img_as_uint(img_as_float(np.asarray(result, dtype=np.uint8))), 'pretty3')
# DICOMSaver().save_test(img_as_uint(np.asarray(result, dtype=np.uint8)), 'pretty4')
# try:
#     DICOMSaver().save_test(((sinogram)), 'pretty')
#     print('test1')
# except:
#     DICOMSaver().save_test(img_as_int(img_as_float(np.asarray(img))), 'pretty')
# DICOMSaver().save(result, 'pretty')
