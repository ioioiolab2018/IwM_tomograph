from tomograph import Point


class Bresenham:
    __d = __dx = __dy = 0
    __x_direction = 0
    __y_direction = 0
    __result = []

    def get_image_points(self, start_point: Point, end_point: Point, image_width: int, image_height: int):
        self.__set_draw_direction(start_point, end_point)
        self.__result = []
        self.__append_point(Point(start_point.x, start_point.y), image_width, image_height)
        self.__run_algorithm(start_point, end_point, image_width, image_height)
        return self.__result

    def __set_draw_direction(self, point1: Point, point2: Point):
        self.__x_direction, self.__dx = self.__get_draw_direction(point1.x, point2.x)
        self.__y_direction, self.__dy = self.__get_draw_direction(point1.y, point2.y)

    def __run_algorithm(self, start_point: Point, end_point: Point, image_width: int, image_height: int):
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
                self.__append_point(Point(x, y), image_width, image_height)
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
                self.__append_point(Point(x, y), image_width, image_height)

    def __get_draw_direction(self, val1, val2):
        if val1 < val2:
            return 1, val2 - val1
        else:
            return -1, val1 - val2

    def __is_leading_axis(self, val1, val2):
        return val1 > val2

    def __get_parameters(self, d1, d2):
        ai = (d1 - d2) * 2
        bi = d1 * 2
        d = bi - d2
        return ai, bi, d

    def __append_point(self, point: Point, image_width, image_height):
        if self.__is_in_image(point, image_width, image_height):
            self.__result.append(point)

    def __is_in_image(self, point, image_width, image_height):
        return 0 <= point.x < image_width and 0 < point.y < image_height
