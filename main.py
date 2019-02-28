from bresenham import Bresenham
from point import Point

x = Bresenham()
start_point = Point(1, 0)
end_point = Point(2, 3)
result = x.get_points(start_point, end_point)
for point in result:
    print('X: ' + str(point.x) + '  Y: ' + str(point.y))
