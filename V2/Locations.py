from __future__ import division
import numpy
import logging
import sys
import random
import Shapes
import SizeDistributions
from math import ceil, sqrt
from types import IntType


class Location(object):
    locations = [()]

    def retrieve_location(self):
        return self.locations.pop(0)

    @staticmethod
    def GenerateInclusions(num_inclusions, distribution, locations, materials, inclusion_shape=Shapes.shapes.CIRCLE, max_attempts=1000, recurse_attempts=0, size=None):
        if type(locations) == FixedLocation:
            assert num_inclusions == len(locations.locations) == len(distribution.distribution) == len(materials), \
            "The number of inclusions, number of locations, number of sizes, and number of materials must be equal"

        inclusions = []

        #loop through the number of inclusions
        for i in range(num_inclusions):
            inclusion = locations.GenerateInclusion(distribution, materials[i], inclusions, inclusion_shape, max_attempts, recurse_attempts, size)
            if inclusion:
                print 'Generated {0} inclusions'.format(len(inclusions))
                inclusions.append(inclusion)

        return inclusions


class FixedLocation(Location):
    def __init__(self, locations=None, random_order=False,
                 generate_lattice=False, num_locations=None, buffersize=0, scalefactor=1):
        """
        Create a new fixed location collection. Note that if the locations
        are specified by the caller, it is the caller's responsibility to
        ensure that the shapes will fit correctly into those locations.
        locations - a list of tuples defining the coordinates of the location
                    in a unit square
        random_order - whether to use the list in the supplied order, or
                       randomise it
        generate_lattice - whether to generate a regular lattice of 
                           locations. Both locations and random_order will 
                           be ignored if this is set to True
        num_locations - the number of sites to generate in a random lattice. 
                        Only needs to be set if generate_lattice is True
        buffersize - The buffer space to leave between circles and the edge of
                     The container, as well as between circles. Only needs to
                     be set if generate_lattice is True
        scalefactor - a factor to multiply the final radius by. It is provided
                      to allow for easier fitting of circles, since if the
                      maximum radius is used, it can be difficult to fit all
                      the circles in if the first is in a bad location. 0.5
                      will halve the radius, 2 will double it. Only needs to
                      be set if generate_lattice is True.
        """
        if generate_lattice:
            assert num_locations is not None, 'The number of locations must be specified to generate a lattice'

            self.GenerateRegularLattice(num_locations, buffersize, scalefactor)

        else:
            # Assert that the locations provided are within a unit square
            for item in locations:
                assert(0.0 <= item[0] <= 1.0 and 0.0 <= item[1] <= 1.0)

            #this uses list() to create a copy of the list rather than a reference
            self.locations = list(locations)

            if random_order:
                random.shuffle(self.locations)


    @staticmethod
    def _DetermineRowLocations(num_locations_left, lattice, rows_to_fill):
        if len(rows_to_fill) == 1:
            lattice[rows_to_fill[0]] = num_locations_left
        else:
            res = num_locations_left / len(rows_to_fill)

            lattice[rows_to_fill[0]] = int(ceil(res))
            num_locations_left -= int(ceil(res))

            #Remove the first row from the list, since it has been filled now
            rows_to_fill.pop(0)

            lattice = FixedLocation._DetermineRowLocations(num_locations_left, lattice, rows_to_fill)

        return lattice

    @staticmethod
    def _LayoutLatticeDimensions(dimensions, num_inclusions):
        lattice = [0] * dimensions[0]
        #Layout the lattice
        if num_inclusions / dimensions[0] <= dimensions[0] - 1:
            lattice[0] = dimensions[0] - 1
        else:
            lattice[0] = dimensions[0]

        #if the rest fit into the last row, put them there and return
        remainder = num_inclusions - lattice[0]
        if remainder == 0:
            return lattice
        elif remainder <= dimensions[0]:
            lattice[len(lattice) - 1] = remainder
            return lattice
        else:
            lattice[len(lattice) - 1] = lattice[0]

        remainder = num_inclusions - (lattice[0] + lattice[len(lattice) - 1])
        res = remainder / (len(lattice) - 2)

        if res.is_integer():
            #They fit neatly into the other rows, so fill them in
            for i in range(1, len(lattice) - 1):
                lattice[i] = int(res)
        else:
            lattice = FixedLocation._DetermineRowLocations(remainder, lattice, range(1, len(lattice) - 1))

        return lattice

    @staticmethod
    def _DetermineLatticeCoordinates(buffersize, num_elements, position):
        space_to_use = 1 - 2 * buffersize
        space_to_use -= buffersize * (num_elements - 1)
        space_per_circle = space_to_use / num_elements
        centre_loc = space_per_circle / 2
        return round(buffersize + position * (space_per_circle + buffersize) + centre_loc, 4)

    @staticmethod
    def _DetermineLatticeLocations(lattice, buffersize, scalefactor):
        locations = []
        #The first row in the lattice always has the max number of elements,
        #so use that to determine the max size

        for i in range(len(lattice)):
            row_loc = FixedLocation._DetermineLatticeCoordinates(buffersize, len(lattice), i)

            for j in range(lattice[i]):
                col_loc = FixedLocation._DetermineLatticeCoordinates(buffersize, lattice[i], j)
                locations.append((col_loc, row_loc))

        return locations

    def GenerateRegularLattice(self, num_inclusions, buffersize, scalefactor):
        """
        Generate the locations of the inclusions by placing them in a regular
        lattice pattern. Any locations currently defined will be overwritten
        """
        assert type(num_inclusions) is IntType, "num_inclusions is not an integer: %r" % num_inclusions

        square_root = sqrt(num_inclusions)

        dimensions = ()

        if square_root.is_integer():
            #It is a whole number, so generate a square_root x square_root grid
            dimensions = (int(square_root), int(square_root))
        else:
            #Not a whole number, some some rows will not be full
            dimensions = (int(ceil(square_root)), int(ceil(square_root)))

        #This list contains the number of sites in each row
        lattice = FixedLocation._LayoutLatticeDimensions(dimensions, num_inclusions)

        self.locations = FixedLocation._DetermineLatticeLocations(lattice, buffersize, scalefactor)

    def GenerateInclusion(self, distribution, material, existing_circles, inclusion_shape=Shapes.shapes.CIRCLE, max_attempts=None, recurse_attempts=0, size=None):
        #Pick a size from the distribution
        args = distribution.retrieve_sample()

        #Find the location for it
        location = self.retrieve_location()

        args['material'] = material
        args['centre'] = location

        #Generate the shape object
        #inclusion = Shapes.ShapeFactory.createShape(inclusion_shape, material=material,centre=location, radius=size)
        inclusion = Shapes.ShapeFactory.createShape(inclusion_shape, **args)

        #Test that it fits there. If not, find a new location
        if (not inclusion.check_intersect(existing_circles)):
            return inclusion
        else:
            return None


class RandomLocation(Location):
    """
    This class does not actually contain a list of locations like
    FixedLocation does, but rather just returns a random location whenever
    requested. It determines a maximum size to be used for the number of
    desired inclusions, and determines the locations based on that size.
    """
    #logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    buffersize = 0.0
    num_locations = 0
    scale_factor = 1

    def __init__(self, num_locations, buffersize=0.0, scale_factor=1):
        """
        num_locations - the number of locations that will be generated
        buffersize - the gap to leave between inclusions, and also between
                     the edge of the matrix
        scale_factor - it is multipled by the determined maximum size. It
                       allows for easier placement of inclusions
        """

        assert 0 <= buffersize <= 1
        #Ensure that the specified number of inclusions can fit in a unit square with the desired buffer size
        assert buffersize * 2 + (num_locations - 1) * buffersize <= 1
        assert num_locations > 0
        assert scale_factor > 0

        self.buffersize = buffersize
        self.num_locations = num_locations
        self.scale_factor = scale_factor

    def retrieve_location(self, shape, max_attempts=1000, radius=None, equalsize=True):
        """
        Return a new location to fit an inclusion. The location will be
        within the unit square matrix, but there is no guarantee that it will
        not overlap with other existing inclusions. That should be checked
        elsewhere shape - a Shapes.shapes enum member defining the type of
        shape to retrieve a location for. The type of shape is important
        for identifying intersections
        maxattempts - the number of times to try to find a location before
                      giving up
        """

        if (shape != Shapes.shapes.CIRCLE):
            raise NotImplementedError("Only Circles have currently been implemented")

        attempts = 0

        if not radius:
            try:
                max_radius = Shapes.Circle.determine_max_radius(self.buffersize, self.num_locations, self.scale_factor)
            except ArithmeticError:
                #There is nothing to do with the exception here, so send it back to the caller
                raise

        while True:
            if attempts == max_attempts:
                # Could not find a location to fit the circle, so give up
                return None

            if not radius:
                radius = Shapes.Circle.determine_radius(max_radius, equalsize)

            x = random.random()
            y = random.random()

            centre = x, y
            newcircle = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, material=None, centre=centre, radius=radius)

            location_ok = newcircle.is_location_inside_square(self.buffersize)
            attempts += 1

            if location_ok:
                return centre
                break

            if (attempts / 1000).is_integer():
                logging.debug('{0} location attempts'.format(attempts))

        #Failed to find a location
        return None

    def GenerateInclusion(self, distribution, material, existing_inclusions, inclusion_shape=Shapes.shapes.CIRCLE, max_attempts=1000, recurse_attempts=0, size=None):
        """
        recurse_attempts is the number of times it will halve the size and try again if it cannot find a 
        solution in max_attempts
        """
        attempts = 0

        if not size:
            size = distribution.retrieve_sample()
        logging.debug('Recurse level {0}, size {1}'.format(recurse_attempts, size))
        while True:
            if attempts == max_attempts:
                if recurse_attempts > 0:
                    logging.debug('Attempts reached max attempts')
                    return self.GenerateInclusion(distribution, material, existing_inclusions, inclusion_shape, max_attempts, recurse_attempts - 1, size / 2)
                else:
                    # Could not find a location to fit the inclusion, so give up
                    logging.debug('Giving up')
                    return None

            #Find the location for it
            location = self.retrieve_location(inclusion_shape, radius=size)
            if not location:
                if recurse_attempts > 0:
                    logging.debug("Can't find location")
                    return self.GenerateInclusion(distribution, material, existing_inclusions, inclusion_shape, max_attempts, recurse_attempts - 1, size / 2)
                else:
                    #could not find a location to fit an object of this size, so skip it
                    logging.debug("Giving up, can't find location")
                    return None

            #Generate the shape object
            myCircle = Shapes.ShapeFactory.createShape(inclusion_shape, material=material, centre=location, radius=size)

            #Test that it fits there. If not, find a new location
            if (not myCircle.check_intersect(existing_inclusions)):
                logging.debug('Found a spot')
                return myCircle
            else:
                if (attempts / 1000).is_integer():
                    logging.debug('{0} attempts'.format(attempts))
                attempts += 1
