import unittest
import Shapes
from math import sqrt

class ShapesTests(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(Shapes.shapes.CIRCLE, 'Circle')

    def test_CircleDef_perimiter_location(self):
        centre = 0.25, 0.25
        radius = 0.31

        circle = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre, radius=radius)
        
        distance = sqrt((circle.centre[0] - circle.perimiter_location()[0])**2 + (circle.centre[1] - circle.perimiter_location()[1])**2)
        self.assertEqual(round(distance, 5), radius)

    def test_location_in_square(self):
        circle = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=(0.5, 0.5), radius=0.5)
        result = circle.is_location_inside_square()
        self.assertTrue(result)
    
    def test_location_not_in_square(self):
        circle = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=(0.5, 0.5), radius=0.6)
        result = circle.is_location_inside_square()
        self.assertFalse(result)

    def test_do_circles_intersect_true(self):
        centre1 = 0.25, 0.25
        centre2 = 0.25, 0.75
        centre3 = 0.75, 0.25
        circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre1, radius=0.3)
        circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre2, radius=0.3)
        #circle 3 does not intersect, but because 1 and 2 do it should still return true
        circle3 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre3, radius=0.15)
        result = circle1.check_intersect([circle2, circle3])
        self.assertTrue(result)

    def test_circles_intersect(self):
        centre1 = 0.25, 0.25
        centre2 = 0.35, 0.35
        circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre1, radius=0.2)
        circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre2, radius=0.2)
        result = circle1.check_intersect([circle2])
        self.assertTrue(result)

    def test_circles_intersect2(self):
        centre1 = 0.575, 0.658
        centre2 = 0.576, 0.658
        centre3 = 0.844, 0.247
        centre4 = 0.095, 0.489
        circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre1, radius=0.16)
        circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre2, radius=0.196)
        circle3 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre3, radius=0.118)
        circle4 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre4, radius=0.086)

        circles = []
        result = circle1.check_intersect(circles)
        self.assertFalse(result)

        circles.append(circle1)
        result = circle2.check_intersect(circles)
        self.assertTrue(result)

    def test_do_circles_intersect_false(self):
        centre1 = 0.25, 0.25
        centre2 = 0.25, 0.75
        centre3 = 0.75, 0.25
        circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre1, radius=0.2)
        circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre2, radius=0.299)
        circle3 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=centre3, radius=0.299)
        result = circle1.check_intersect([circle2, circle3])
        self.assertFalse(result)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ShapesTests)
    unittest.TextTestRunner(verbosity=2).run(suite)