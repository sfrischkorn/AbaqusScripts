"""
This module contains code to generate non-intersecting circles within a unit square. generate_circles() will generate the 
location and radius of circles based on the input parameters. The other methods should not generally be used in normal circumstances.
"""

from __future__ import division
from random import random, uniform
from math import fabs, sqrt


class CircleDef(object):
    """
    Class to hold the information about a circle
    """

    def __init__(self, centre=(), radius = 0.0):
        self.centre = centre
        self.radius = radius

    def perimiter_location(self):
        """
        Get a coordinate that lies on the perimiter of the circle
        """

        return self.centre[0] + self.radius, self.centre[0]

    def __str__(self):
        return 'Centre: {}, radius: {}.'.format(self.centre, self.radius)


def _determine_max_radius(buffersize, numcircles, scalefactor):
    """
    Determines the Maximum radius of circles to fit into a unit square. The fit is based on all fitting across in a row,
    so that they will always be able to fit.
    buffersize is the buffer space to leave between circles and the edge of the container, as well as between circles.
    numcircles is the number of circles to fit into the container
    scalefactor is a factor to multiply the final radius by. It is provided to allow for easier fitting of circles, since
    if the maximum radius is used, it can be difficult to fit all the circles in if the first is in a bad location. 0.5 will halve
    the radius, 2 will double it.
    """
    
    if buffersize*2 + (numcircles-1)*buffersize > 1:
        raise ArithmeticError('Cannot fit {} circles with {} buffer size'.format(numcircles, buffersize))
    
    return (((1 - buffersize - buffersize*numcircles) / numcircles)/2) * scalefactor


def _is_location_inside_square(buffersize, radius, x, y):
    """
    Ensure that the circle will sit completely within the buffer zone of the container
    """

    if x - radius < buffersize or x + radius > (1 - buffersize):
        return False
    if y - radius < buffersize or y + radius > (1 - buffersize):
        return False

    return True


def _do_circles_intersect(newcircle, circles):
    """
    The circles intesect if the distance between the centrepoints is less than the sum of the radii. Also check to make sure one
    circle isn't wholly within another circle. It is squared to remove the need for a square root, and absolute value on the
    """

    for circle in circles:
        centre_distance = sqrt((newcircle.centre[0] - circle.centre[0])**2 + (newcircle.centre[1] - circle.centre[1])**2)

        if fabs(newcircle.radius - circle.radius) <= centre_distance <= (newcircle.radius + circle.radius):
            return True

    return False
    
def _determine_radius(max_radius, equalsize):
    if equalsize:
        return max_radius
    else:
        return uniform(0.01, max_radius)


def generate_circles(numcircles=1, buffersize=0.05, scalefactor=1, maxattempts=1000, equalsize=True):
    """
    Generate a list of non-intersecting circles that lie within a unit square container.
    numcircles - The number of circles to attempt to create. It is not guaranteed to generate this number. If it tries maxattempts times unsuccessfully, it will return the current successfully generated circles.
    buffersize - The distance to leave between both the edge of the container and circles, and between circles.
    scalefactor - The factor to multiply the maximum determined radius by. This can make it easier to fit circles. 0.5 halves the radius, 2 doubles it.
    maxattempts - The number of times to attempt to find a fitting circle before giving up.
    equalsize - Whether the size of the circles should be equal. If True, the maximum radius for the number of circles will be determined 
    and that will be used for all of the circles. If False, a random size between the maximum determined size and 0.01 will be used.
    """
    
    try:
        max_radius = _determine_max_radius(buffersize, numcircles, scalefactor)
    except ArithmeticError: 
        #There is nothing to do with the exception here, so send it back to the caller
        raise
    
    generated_circles = []

    for i in range(numcircles):
        attempts = 0
        
        while True:
            if attempts == maxattempts:
                # Could not find a location to fit the circle, so give up
                return generated_circles
                
            radius = _determine_radius(max_radius, equalsize)

            x = random()
            y = random()

            centre = x, y
            newcircle = CircleDef(centre, radius)

            location_ok = _is_location_inside_square(buffersize, radius, x, y) and not _do_circles_intersect(newcircle, generated_circles)
            attempts += 1

            if location_ok:
                generated_circles.append(newcircle)
                break

    return generated_circles
