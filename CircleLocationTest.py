import unittest
import CircleLocation
from random import randint
from math import sqrt

class CircleLocationTests(unittest.TestCase):
    def test_generate_circles_one_circle(self):
        buffersize = 0.1
        result = CircleLocation.generate_circles(buffersize=buffersize, scalefactor=0.9)
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].radius + 2 * buffersize <= 1)

    def test_generate_circles_too_many_exception(self):
        self.assertRaises(ArithmeticError, CircleLocation.generate_circles, numcircles=100, buffersize=.5)

    def test_generate_circles_multiple_circle(self):
        numcircles = randint(1, 50)
        buffersize = 0
        result = CircleLocation.generate_circles(numcircles=numcircles, buffersize=buffersize, scalefactor=0.9)
        self.assertEqual(len(result), numcircles)

        #ensure that all of the circles fit in the unit square
        total_radius = sum(circle.radius for circle in result)
        self.assertTrue(total_radius + 2 * buffersize + buffersize * (len(result) - 1) <= 1)

        #Ensure that all of the radii are the same
        self.assertEqual(len(set(circle.radius for circle in result)), 1)

    def test_generate_circles_different_radii(self):
        equalsize = False
        numcircles = 5
        buffersize = 0.1
        scalefactor = 0.9

        result = CircleLocation.generate_circles(equalsize=equalsize, numcircles=numcircles, buffersize=buffersize, scalefactor=scalefactor)
        max_radius = CircleLocation._determine_max_radius(buffersize, numcircles, scalefactor)
        self.assertEqual(len(result), numcircles)
        self.assertTrue(0.01 <= circle.radius <= max_radius for circle in result)
        #Ensure that all of the radii are unique. Note that there is a extremely small chance that this test could fail, due to
        #radii being the same random number. But given that they are random floats, the chance is extremely small
        self.assertEqual(len(result), len(set(circle.radius for circle in result)))

    def test_location_in_square(self):
        result = CircleLocation._is_location_inside_square(0, 0.5, 0.5, 0.5)
        self.assertTrue(result)
    
    def test_location_not_in_square(self):
        result = CircleLocation._is_location_inside_square(0, 0.6, 0.5, 0.5)
        self.assertFalse(result)
        
    def test_do_circles_intersect_true(self):
        centre1 = 0.25, 0.25
        centre2 = 0.25, 0.75
        centre3 = 0.75, 0.25
        circle1 = CircleLocation.CircleDef(centre1, 0.3)
        circle2 = CircleLocation.CircleDef(centre2, 0.3)
        #circle 3 does not intersect, but because 1 and 2 do it should still return true
        circle3 = CircleLocation.CircleDef(centre3, 0.15)
        result = CircleLocation._do_circles_intersect(circle1, [circle2, circle3])
        self.assertTrue(result)
        
    def test_do_circles_intersect_false(self):
        centre1 = 0.25, 0.25
        centre2 = 0.25, 0.75
        centre3 = 0.75, 0.25
        circle1 = CircleLocation.CircleDef(centre1, 0.2)
        circle2 = CircleLocation.CircleDef(centre2, 0.2)
        circle3 = CircleLocation.CircleDef(centre3, 0.299)
        result = CircleLocation._do_circles_intersect(circle1, [circle2, circle3])
        self.assertFalse(result)
    
    def test_CircleDef_perimiter_location(self):
        centre = 0.25, 0.25
        radius = 0.31
        circle = CircleLocation.CircleDef(centre, radius)
        
        distance = sqrt((circle.centre[0] - circle.perimiter_location()[0])**2 + (circle.centre[1] - circle.perimiter_location()[1])**2)
        self.assertEqual(round(distance, 5), radius)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CircleLocationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)