import unittest
import Locations
import Shapes

class LocationsTests(unittest.TestCase):
    def creation_helper(self):
        loc = [(0.5, 0.5)]
        return Locations.FixedLocation(loc)

    def test_fixed_loc_outside_square(self):
        loc = [(-0.5, 0.5)]
        self.assertRaises(AssertionError, Locations.FixedLocation, loc)

    def test_fixed_creation(self):
        fixed_loc = self.creation_helper()
        self.assertEqual(1, len(fixed_loc.locations))
    
    def test_retrieve_fixed_location(self):
        fixed_loc = self.creation_helper()
        val = fixed_loc.retrieve_location()

        self.assertEqual((0.5, 0.5), val)
        self.assertEqual(0, len(fixed_loc.locations))

    def test_retrieve_fixed_location_multiple(self):
        fixed_loc = self.creation_helper()
        fixed_loc.locations.append((0.2, 0.2))

        val = fixed_loc.retrieve_location()

        self.assertEqual((0.5, 0.5), val)
        self.assertEqual(1, len(fixed_loc.locations))

    def test_fixed_random_order(self):
        """
        Note that this test can technically fail. If the random function randomly puts the 10 objects back in the same 
        order, then it will fail. That should only happen 1 in 3.6 million times the test is run though, so it should be fine.
        """

        locs = [(0.1, 0.1), (0.2, 0.2), (0.3, 0.3), (0.4, 0.4), (0.5, 0.5), (0.6, 0.6), (0.7, 0.7), (0.8, 0.8), (0.9, 0.9)]
        fixed_loc = Locations.FixedLocation(locs, True)

        self.assertNotEqual(locs, fixed_loc.locations)



    def test_create_random_location_buffer_less_0(self):
        self.assertRaises(AssertionError, Locations.RandomLocation, 1, -0.3)

    def test_create_random_location_buffer_greater_1(self):
        self.assertRaises(AssertionError, Locations.RandomLocation, 1, 1.1)

    def test_create_random_location_numlocations_less_0(self):
        self.assertRaises(AssertionError, Locations.RandomLocation, 0)

    def test_create_random_location_scale_less_0(self):
        self.assertRaises(AssertionError, Locations.RandomLocation, 1, scale_factor=0)

    def test_create_random_location_toomanycircles(self):
        self.assertRaises(AssertionError, Locations.RandomLocation, 100, buffersize=.5)

    def test_create_random_location(self):
        loc = Locations.RandomLocation(1)
        self.assertIsNotNone(loc)

    def test_create_random_location_one_circle(self):
        buffersize = 0.1
        loc = Locations.RandomLocation(1, buffersize=buffersize, scale_factor=0.9)
        result = loc.retrieve_location(Shapes.shapes.CIRCLE)
        self.assertEqual(len(result), 2)
        self.assertTrue(0 <= result[0] <= 1)
        self.assertTrue(0 <= result[1] <= 1)

    def test_create_random_location_multiple_circles(self):
        buffersize = 0.1
        loc = Locations.RandomLocation(3, buffersize=buffersize, scale_factor=0.9)

        for i in range(3):
            result = loc.retrieve_location(Shapes.shapes.CIRCLE)
            self.assertTrue(0 <= result[0] <= 1)
            self.assertTrue(0 <= result[1] <= 1)


        


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LocationsTests)
    unittest.TextTestRunner(verbosity=2).run(suite)