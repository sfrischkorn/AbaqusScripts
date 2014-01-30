import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import Shapes
import SizeDistributions
import Locations
import Materials

from math import sqrt

class ShapesTests(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(Shapes.shapes.CIRCLE, 'Circle')

    def test_CircleDef_perimiter_location(self):
        centre = 0.25, 0.25
        radius = 0.31

        circle = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre, radius=radius)

        distance = sqrt((circle.centre[0] - circle.perimeter_location()[0])**2 + (circle.centre[1] - circle.perimeter_location()[1])**2)
        self.assertEqual(round(distance, 5), radius)

    def test_location_in_square(self):
        circle = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=(0.5, 0.5), radius=0.5)
        result = circle.is_location_inside_square()
        self.assertTrue(result)

    def test_location_not_in_square(self):
        circle = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=(0.5, 0.5), radius=0.6)
        result = circle.is_location_inside_square()
        self.assertFalse(result)

    def test_do_circles_intersect_true(self):
        centre1 = 0.25, 0.25
        centre2 = 0.25, 0.75
        centre3 = 0.75, 0.25
        circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre1, radius=0.3)
        circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre2, radius=0.3)
        #circle 3 does not intersect, but because 1 and 2 do it should still return true
        circle3 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre3, radius=0.15)
        result = circle1.check_intersect([circle2, circle3])
        self.assertTrue(result)

    def test_circles_intersect(self):
        centre1 = 0.25, 0.25
        centre2 = 0.35, 0.35
        circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre1, radius=0.2)
        circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre2, radius=0.2)
        result = circle1.check_intersect([circle2])
        self.assertTrue(result)

    def test_circles_intersect2(self):
        centre1 = 0.575, 0.658
        centre2 = 0.576, 0.658
        centre3 = 0.844, 0.247
        centre4 = 0.095, 0.489
        circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre1, radius=0.16)
        circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre2, radius=0.196)
        circle3 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre3, radius=0.118)
        circle4 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre4, radius=0.086)

        circles = []
        result = circle1.check_intersect(circles)
        self.assertFalse(result)

        circles.append(circle1)
        result = circle2.check_intersect(circles)
        self.assertTrue(result)

    def test_circles_intersect3(self):
        centre1 = 0.25, 0.25
        centre2 = 0.25, 0.25
        circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre1, radius=0.2)
        circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre2, radius=0.1)
        result = circle1.check_intersect([circle2])
        self.assertTrue(result)

        result2 = circle2.check_intersect([circle1])

    def test_circles_intersect4(self):
            centre1 = 0.25, 0.75
            centre2 = 0.75, 0.25
            centre3 = 0.5, 0.5
            circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre1, radius=0.16)
            circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre2, radius=0.196)
            circle3 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre3, radius=0.5)

            circles = [circle2, circle3]
            result = circle1.check_intersect(circles)
            self.assertTrue(result)

    def test_do_circles_intersect_false(self):
        centre1 = 0.25, 0.25
        centre2 = 0.25, 0.75
        centre3 = 0.75, 0.25
        circle1 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre1, radius=0.2)
        circle2 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre2, radius=0.299)
        circle3 = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre3, radius=0.299)
        result = circle1.check_intersect([circle2, circle3])
        self.assertFalse(result)

    def test_circle_max_radius_1(self):
        result = Shapes.Circle.determine_max_radius(0, 1, 1)
        self.assertEqual(0.5, result)

    def test_circle_max_radius_2(self):
        result = Shapes.Circle.determine_max_radius(0, 2, 1)
        self.assertEqual(0.25, result)

    def test_generate_ellipse_commands(self):
        INCLUSION_SIZE = 0.25
        LOCATION = (0.5, 0.5)

        circle = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=LOCATION, radius=INCLUSION_SIZE)

        commands = circle.GenerateSketch()

        self.assertEqual(4, len(commands))
        self.assertEqual("t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.5, 0.5, 0.0))", commands[0])
        self.assertEqual("s.EllipseByCenterPerimeter(center=(0.0, 0.0), axisPoint1=(0.25, 0.0), axisPoint2=(0.0, 0.25))", commands[3])

    def test_ellipses_intersect_true(self):
        LOCATION = (0.5, 0.5)
        LOCATION2 = (1, 1)
        ellipse1 = Shapes.ShapeFactory.createShape(Shapes.shapes.ELLIPSE, material=None, centre=LOCATION, short_axis=1, long_axis=2)
        ellipse2 = Shapes.ShapeFactory.createShape(Shapes.shapes.ELLIPSE, material=None, centre=LOCATION2, short_axis=1, long_axis=2)

        result = ellipse1.check_intersect(ellipse2)
        self.assertTrue(result)

    def test_ellipses_intersect_false(self):
        LOCATION = (0.5, 0.5)
        LOCATION2 = (10.5, 10.5)
        ellipse1 = Shapes.ShapeFactory.createShape(Shapes.shapes.ELLIPSE, material=None, centre=LOCATION, short_axis=1, long_axis=2)
        ellipse2 = Shapes.ShapeFactory.createShape(Shapes.shapes.ELLIPSE, material=None, centre=LOCATION2, short_axis=1, long_axis=2)

        result = ellipse1.check_intersect(ellipse2)
        self.assertFalse(result)

    def test_ellipses_intersect_contains_true(self):
        LOCATION = (0.0, 0.0)
        LOCATION2 = (0.0, 0.0)
        ellipse1 = Shapes.ShapeFactory.createShape(Shapes.shapes.ELLIPSE, material=None, centre=LOCATION, short_axis=10, long_axis=20)
        ellipse2 = Shapes.ShapeFactory.createShape(Shapes.shapes.ELLIPSE, material=None, centre=LOCATION2, short_axis=1, long_axis=2)

        result = ellipse1.check_intersect(ellipse2)
        self.assertTrue(result)

    def test_export(self):
        NUM_INCLUSIONS = 4
        INCLUSION_SIZE = 0.2

        #Define a material for the inclusions
        inclusion_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Inclusion', youngs_modulus=2000, poissons_ratio=0.3)
        inclusion_material2 = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Inclusion2', youngs_modulus=2500, poissons_ratio=0.2)
        inclusion_materials = [inclusion_material, inclusion_material, inclusion_material2, inclusion_material]

        matrix_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Matrix', youngs_modulus=3000, poissons_ratio=0.25)

        #Create the distribution and location to use, and generate the inclusions
        dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
        loc = Locations.FixedLocation(generate_lattice=True, num_locations=4)
        circles = Locations.Location.GenerateInclusions(NUM_INCLUSIONS, dist, loc, inclusion_materials)

        output = Shapes.Shape.ExportInclusions(circles, matrix_material)
        print output

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ShapesTests)
    unittest.TextTestRunner(verbosity=2).run(suite)