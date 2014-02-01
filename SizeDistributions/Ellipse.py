import SizeDistributions

class Ellipse(SizeDistributions.SizeDistribution):
    def __init__(self):
        super(Ellipse, self).__init__()

class Constant(Ellipse):
    def __init__(self, horizontal_axis, vertical_axis, num_inclusions):
        super(Constant, self).__init__()

        for x in range(num_inclusions):
            self.distribution.append(dict({'long_axis':horizontal_axis, 'short_axis':vertical_axis}))

