import SizeDistributions
import Shapes

def GenerateCircles(num_inclusions, distribution, location):
    if num_inclusions <> len(location):
        raise IndexError("The number of inclusions and length of the locations must be equal")        

    # loop through num inclusions
    for i in range(num_inclusions):
        #Pick a size from the distribution
        size = distribution.retrieve_sample()

        #Find the location for it

        #Generate the shape object
        myCircle = Shapes.ShapeFactory.createShape(Shapes.shapes.CIRCLE, centre=location[i], radius=size)
        myCircle.centre = location[i]
        myCircle.radius = size

        #Test that it fits there. If not, find a new location


        print myCircle

NUM_INCLUSIONS = 1
INCLUSION_SIZE = 0.25
SHAPE = 'Circle'
LOCATION = [(0.5, 0.5)]  # this needs a location generator similar to the distribution one. either pre-define locations, or have it randomly pick them

dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)

GenerateCircles(NUM_INCLUSIONS, dist, LOCATION)