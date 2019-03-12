from tomograph.utils.point import Point
class Section:
    start_point = None
    end_point = None
    
    def __init__(self, start: Point, end: Point):
        self.start_point = start
        self.end_point = end
