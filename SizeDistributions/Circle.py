import numpy
from random import uniform

import SizeDistributions

class Circle(SizeDistributions.SizeDistribution):
    def __init__(self):
        super(Circle, self).__init__()

    def get_values(self):
        values = []
        for item in self.distribution:
            values.append(item['radius'])

        return values


class Constant(Circle):
    """
    Generates a distribution of constant size
    """
    def __init__(self, size, num_inclusions):
        super(Constant, self).__init__()

        for x in range(num_inclusions):
            self.distribution.append(dict({'radius': size}))

class Random(Circle):
    """
    Generates a random distribution
    """
    def __init__(self, num_inclusions, lower=0.001, upper=0.999):
        super(Random, self).__init__()

        self.distribution = [uniform(lower, upper) for
                             x in range(num_inclusions)]

class Gaussian(Circle):
    """
    Generates a gaussian probability distribution, containing num_inclusions
    inclusions
    """
    def __init__(self, centre, stdev, num_inclusions):
        super(Gaussian, self).__init__()

        for size in numpy.random.normal(centre, stdev, num_inclusions).tolist():
            self.distribution.append(dict({'radius': size}))

class LogNormal(Circle):
    """
    Generates a log-normal probability distribution, containing num_inclusions
    inclusions
    """
    def __init__(self, centre, stdev, num_inclusions):
        super(LogNormal, self).__init__()

        for size in numpy.random.lognormal(centre, stdev, num_inclusions).tolist():
            self.distribution.append(dict({'radius': size}))

class Weibull(Circle):
    """
    Generates a weibulll probability distribution, containing num_inclusions
    inclusions
    """
    def __init__(self, shape, num_inclusions):
        super(Weibull, self).__init__()

        for size in numpy.random.weibull(shape, num_inclusions).tolist():
            self.distribution.append(dict({'radius': size}))


