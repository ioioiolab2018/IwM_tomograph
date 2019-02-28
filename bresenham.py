from point import Point


class Bresenham:
    __d = __dx = __dy = 0
    __x_direction = 0
    __y_direction = 0
    __result = []

    def get_points(self, start_point, end_point):
        self.__set_draw_direction(start_point, end_point)
        self.__result.append(Point(start_point.x, start_point.y))
        self.__run_algorithm(start_point, end_point)
        return self.__result

    def __set_draw_direction(self, point1, point2):
        self.__x_direction, self.__dx = self.__get_draw_direction(point1.x, point2.x)
        self.__y_direction, self.__dy = self.__get_draw_direction(point1.y, point2.y)

    def __run_algorithm(self, start_point, end_point):
        x = start_point.x
        y = start_point.y

        if self.__is_leading_axis(self.__dx, self.__dy):
            ai, bi, d = self.__get_parameters(self.__dy, self.__dx)
            while x != end_point.x:
                if d >= 0:
                    x += self.__x_direction
                    y += self.__y_direction
                    d += ai
                else:
                    d += bi
                    x += self.__x_direction
                self.__result.append(Point(x, y))
        else:
            ai, bi, d = self.__get_parameters(self.__dx, self.__dy)
            while y != end_point.y:
                if d >= 0:
                    x += self.__x_direction
                    y += self.__y_direction
                    d += ai
                else:
                    d += bi
                    y += self.__y_direction
                self.__result.append(Point(x, y))

    def __get_draw_direction(self, val1, val2):
        if val1 < val2:
            return 1, val2 - val1
        else:
            return 1, val1 - val2

    def __is_leading_axis(self, val1, val2):
        return val1 > val2

    def __get_parameters(self, d1, d2):
        ai = (d1 - d2) * 2
        bi = d1 * 2
        d = bi - d2
        return ai, bi, d
