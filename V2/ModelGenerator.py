import Locations
import SizeDistributions
import Shapes

def GenerateCircles(num_inclusions, distribution, locations, max_attempts=10000):
    if type(locations) == Locations.FixedLocation:
        if num_inclusions <> len(locations.locations) <> len(distribution.distribution):
                raise IndexError("The number of inclusions and length of the locations must be equal")    
    
    circles = []

    # loop through num inclusions
    for i in range(num_inclusions):
        inclusion = locations.GenerateInclusion(distribution, circles)
        if inclusion:
            circles.append(inclusion)

    return circles

NUM_INCLUSIONS = 1
INCLUSION_SIZE = 0.25
LOCATION = [(0.5, 0.5)] 

dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
loc = Locations.FixedLocation(LOCATION)

#GenerateCircles(NUM_INCLUSIONS, dist, loc)



NUM_INCLUSIONS = 2
INCLUSION_SIZE = 0.2
LOCATION = [(0.25, 0.25), (0.35, 0.35)] 

dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
loc = Locations.FixedLocation(LOCATION)

circles = GenerateCircles(NUM_INCLUSIONS, dist, loc)



NUM_INCLUSIONS = 2
BUFFER = 0.01 
SCALE = 0.8
INCLUSION_SIZE = 0.2

dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
loc = Locations.RandomLocation(NUM_INCLUSIONS)

#GenerateCircles(NUM_INCLUSIONS, dist, loc)


NUM_INCLUSIONS = 4
BUFFER = 0.01 
SCALE = 0.8
INCLUSION_SIZE = 0.2

dist = SizeDistributions.Random(NUM_INCLUSIONS, upper=0.2)
loc = Locations.RandomLocation(NUM_INCLUSIONS)

#circles = GenerateCircles(NUM_INCLUSIONS, dist, loc)

for circle in circles:
    print circle