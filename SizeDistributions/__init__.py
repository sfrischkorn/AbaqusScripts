from random import randint


class SizeDistribution(object):
    distribution = []

    def __init__(self):
        self.distribution = []

    def retrieve_sample(self):
        """
        Retrieve a random item from the distribution and remove it from the
        list. This ensures once it is used it will no be used again
        """
        index = randint(0, len(self.distribution) - 1)
        sample = self.distribution[index]
        del self.distribution[index]

        return sample
