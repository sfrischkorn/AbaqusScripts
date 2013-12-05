import numpy
from random import randint, uniform

class SizeDistribution(object):
    distribution = []

    def retrieve_sample(self):
        """
        Retrieve a random item from the distribution and remove it from the list. This ensures once it is used it will no be used again
        """
        index = randint(0, len(self.distribution) - 1)
        sample = self.distribution[index]
        del self.distribution[index]
        return sample

class Constant(SizeDistribution):
    """
    Generates a distribution of constant size
    """
    def __init__(self, size, num_inclusions):
        self.distribution = [size for x in range(num_inclusions)]

    
class Random(SizeDistribution):
    """
    Generates a random distribution
    """
    def __init__(self, num_inclusions, lower = 0.001, upper = 0.999):
        self.distribution = [uniform(lower, upper) for x in range(num_inclusions)]

    
class Gaussian(SizeDistribution):
    """
    Generates a gaussian probability distribution, containing num_inclusions inclusions
    """
    def __init__(self, centre, stdev, num_inclusions):
        self.distribution = numpy.random.normal(centre, stdev, num_inclusions).tolist()

    
class LogNormal(SizeDistribution):
    """
    Generates a log-normal probability distribution, containing num_inclusions inclusions
    """
    def __init__(self, centre, stdev, num_inclusions):
        self.distribution = numpy.random.lognormal(centre, stdev, num_inclusions).tolist()
    
    
class Weibull(SizeDistribution):
    """
    Generates a weibulll probability distribution, containing num_inclusions inclusions
    """
    def __init__(self, shape, num_inclusions):
        self.distribution = numpy.random.weibull(shape, num_inclusions).tolist()