import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import Locations

import Materials
import Shapes
import SizeDistributions

import turtle

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

    def test_LayoutLattice_1(self):
        result = Locations.FixedLocation._LayoutLatticeDimensions((1, 1), 1)
        self.assertEqual(1, result[0])

    def test_LayoutLattice_2(self):
        result = Locations.FixedLocation._LayoutLatticeDimensions((2, 2), 2)
        self.assertEqual(1, result[0])
        self.assertEqual(1, result[1])

    def test_LayoutLattice_4(self):
        result = Locations.FixedLocation._LayoutLatticeDimensions((2, 2), 4)
        self.assertEqual(2, result[0])
        self.assertEqual(2, result[1])

    def test_LayoutLattice_10(self):
        result = Locations.FixedLocation._LayoutLatticeDimensions((4, 4), 10)
        self.assertEqual(3, result[0])
        self.assertEqual(2, result[1])
        self.assertEqual(2, result[2])
        self.assertEqual(3, result[3])

    def test_LayoutLattice_11(self):
        result = Locations.FixedLocation._LayoutLatticeDimensions((4, 4), 11)
        self.assertEqual(3, result[0])
        self.assertEqual(3, result[1])
        self.assertEqual(2, result[2])
        self.assertEqual(3, result[3])

    def test_LayoutLattice_21(self):
        result = Locations.FixedLocation._LayoutLatticeDimensions((5, 5), 21)
        self.assertEqual(5, result[0])
        self.assertEqual(4, result[1])
        self.assertEqual(4, result[2])
        self.assertEqual(3, result[3])
        self.assertEqual(5, result[4])

    def test_LayoutLattice_93(self):
        result = Locations.FixedLocation._LayoutLatticeDimensions((10, 10), 93)
        self.assertEqual(10, result[0])
        self.assertEqual(10, result[1])
        self.assertEqual(9, result[2])
        self.assertEqual(9, result[3])
        self.assertEqual(9, result[4])
        self.assertEqual(9, result[5])
        self.assertEqual(9, result[6])
        self.assertEqual(9, result[7])
        self.assertEqual(9, result[8])
        self.assertEqual(10, result[9])

    def test_lattice_location_1(self):
        result = Locations.FixedLocation._DetermineLatticeLocations([1], 0, 1)
        self.assertEqual(1, len(result))
        self.assertTrue((0.5, 0.5) in result)

    def test_lattice_location_4(self):
        result = Locations.FixedLocation._DetermineLatticeLocations([2, 2], 0, 1)
        self.assertEqual(4, len(result))
        self.assertTrue((0.25, 0.25) in result)
        self.assertTrue((0.25, 0.75) in result)
        self.assertTrue((0.75, 0.25) in result)
        self.assertTrue((0.75, 0.75) in result)

    def test_lattice_location_3_buffer(self):
        result = Locations.FixedLocation._DetermineLatticeLocations([2, 1], 0.1, 1)
        self.assertEqual(3, len(result))
        self.assertTrue((0.275, 0.275) in result)
        self.assertTrue((0.725, 0.275) in result)
        self.assertTrue((0.5, 0.725) in result)

    def test_lattice_location_4_buffer(self):
        result = Locations.FixedLocation._DetermineLatticeLocations([2, 2], 0.1, 1)
        self.assertEqual(4, len(result))
        self.assertTrue((0.275, 0.275) in result)
        self.assertTrue((0.275, 0.725) in result)
        self.assertTrue((0.725, 0.275) in result)
        self.assertTrue((0.725, 0.725) in result)

    def test_lattice_constructor(self):
        loc = Locations.FixedLocation(generate_lattice=True, num_locations=4)
        self.assertEqual(4, len(loc.locations))
        self.assertTrue((0.25, 0.25) in loc.locations)
        self.assertTrue((0.25, 0.75) in loc.locations)
        self.assertTrue((0.75, 0.25) in loc.locations)
        self.assertTrue((0.75, 0.75) in loc.locations)

    def test_generate_circles(self):
        NUM_INCLUSIONS = 4
        INCLUSION_SIZE = 0.2

        #Define a material for the inclusions
        inclusion_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Inclusion', youngs_modulus=2000, poissons_ratio=0.3)
        #This is going to use the same material for all inclusions
        inclusion_materials = [inclusion_material] * NUM_INCLUSIONS

        #Create the distribution and location to use, and generate the inclusions
        dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
        loc = Locations.FixedLocation(generate_lattice=True, num_locations=4)
        circles = Locations.Location.GenerateInclusions(NUM_INCLUSIONS, dist, loc, inclusion_materials)

    @staticmethod
    def drawCircle (centerpoint, radius):
        (x,y) = centerpoint
        turtle.up()
        turtle.setpos(x*1000-500 + radius * 1000,y*1000-500)

        # turtle.right(3) this is kind of pointless
        turtle.setheading(90)
        turtle.down()
        turtle.circle(radius*1000)

    @staticmethod
    def setupboundingbox():
        turtle.reset()
        turtle.setup(1100, 1100)
        turtle.screensize(canvwidth=1100, canvheight=1100)
        turtle.up()
        turtle.goto(-500, -500)
        turtle.setheading(90)
        turtle.down()
        turtle.forward(1000)
        turtle.right(90)
        turtle.forward(1000)
        turtle.right(90)
        turtle.forward(1000)
        turtle.right(90)
        turtle.forward(1000)

    def test_generate_circles_50_visual(self):
        NUM_INCLUSIONS = 50

        #Define a material for the inclusions
        inclusion_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Inclusion', youngs_modulus=2000, poissons_ratio=0.3)
        #This is going to use the same material for all inclusions
        inclusion_materials = [inclusion_material] * NUM_INCLUSIONS

        #Create the distribution and location to use, and generate the inclusions
        dist = SizeDistributions.Random(NUM_INCLUSIONS)
        loc = Locations.RandomLocation(NUM_INCLUSIONS, buffersize=0, scale_factor=1)
        circles = Locations.Location.GenerateInclusions(NUM_INCLUSIONS, dist, loc, inclusion_materials, recurse_attempts=5, max_attempts=50)

        print 'Generated {0} circles'.format(len(circles))

        #LocationsTests.setupboundingbox()
        #for circle in circles:
        #    LocationsTests.drawCircle(circle.centre, circle.radius)

    def test_guassian_circles_visual(self):
        NUM_INCLUSIONS = 10

        #Define a material for the inclusions
        inclusion_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Inclusion', youngs_modulus=2000, poissons_ratio=0.3)
        #This is going to use the same material for all inclusions
        inclusion_materials = [inclusion_material] * NUM_INCLUSIONS

        max_radius = Shapes.Circle.determine_max_radius(0, 4, 1)

        #Create the distribution and location to use, and generate the inclusions
        dist = SizeDistributions.Gaussian(max_radius / 2, max_radius / 2, NUM_INCLUSIONS)
        loc = Locations.FixedLocation(generate_lattice=True, num_locations=NUM_INCLUSIONS, buffersize=0, scalefactor=1)
        circles = Locations.Location.GenerateInclusions(NUM_INCLUSIONS, dist, loc, inclusion_materials, recurse_attempts=5, max_attempts=50)

        LocationsTests.setupboundingbox()

        print 'Generated {0} circles'.format(len(circles))

        for circle in circles:
            LocationsTests.drawCircle(circle.centre, circle.radius)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LocationsTests)
    unittest.TextTestRunner(verbosity=2).run(suite)