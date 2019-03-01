from bresenham import Bresenham
from section import Section


class RadonTransform:
    def transform(self, image, section):
        image_points = Bresenham().get_points(section.start_point, section.end_point)
        image_points = self.__filter_image_points(len(image), len(image[0]), image_points)
        self.__calculate_sinogram_value(image, image_points)
        return image_points

    def __get_sections(self, emitter_position, detector_positions):
        sections = []
        for position in detector_positions:
            sections.append(Section(emitter_position, position))
        return sections

    def __filter_image_points(self, image_height, image_width, points):
        x = image_width / 2
        y = image_height / 2
        image_points = []
        for point in points:
            if abs(point.x) <= x and abs(point.y) <= y:
                image_points.append(point)
        return image_points

    def __calculate_sinogram_value(self, image, points):
        x = len(image[0])
        y = len(image)
        points_sum = 0
        for point in points:
            points_sum += image[abs(point.y - y)][abs(point.x - x)]
        return points_sum / len(points)
