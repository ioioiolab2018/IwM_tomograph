from point import Point
from bresenham import Bresenham
from section import Section

class RadonTransform:
    def transform(self, image, emiter_position, detector_positions):
        image_points = []
        sections = self.__get_section(emiter_position, detector_positions)
        for section in sections:
            image_points = Bresenham().get_points(section.start_point, section.end_point)
            image_points = self.__filter_image_points()
        return image_points

    def __get_sections(self, emiter_position, detector_positions):
        sections = []
        for position in detector_positions:
            sections.append(Section(emiter_position, position))
        return sections
    
    def __filter_image_points(image_height, image_width, points):
        return points
    
    def inverse_transform(self):
        print('InverseTransform')

    def __init__(self):
        print('init')
