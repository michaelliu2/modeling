"""
returns population prediction based on stochastically
implementation of https://blog.kissmetrics.com/modeling-churn/
"""

import numpy as np

from brownian_motion import BrownianMotion

class PopulationPredictor(object):

    def __init__(
        self,
        population_0,
        growth_0,
        growth_diff_mean,
        growth_diff_sigma,
        decay_rate_0,
        decay_rate_diff_mean,
        decay_rate_diff_sigma
    ):

        self.population_0 = population_0
        self.growth_0 = growth_0
        self.growth_diff_mean = growth_diff_mean
        self.growth_diff_sigma = growth_diff_sigma
        self.decay_rate_0 = decay_rate_0
        self.decay_rate_diff_mean = decay_rate_diff_mean
        self.decay_rate_diff_sigma = decay_rate_diff_sigma

        # These are set each run
        self.growth = None
        self.decay_rate = None
        self.current_population = None

    def increment(self):

        growth = self.growth.sample()
        decay_rate = self.decay_rate.sample()
        loss = self.current_population * decay_rate
        gain = self.current_population - loss
        # NOTE if loss or gain is negative, this will break.
        # This may happen because the decay_rate params were too
        # extreme and decay_rate no longer is in [0,1]
        decay = np.random.beta(loss, gain)
        self.current_population += growth - decay

        return self.current_population

    def run(self, steps):

        if steps < 1:
            raise Exception("You cant have less than 1 step")

        self.growth = BrownianMotion(
            self.growth_diff_mean,
            self.growth_diff_sigma,
            self.growth_0
        )

        self.decay_rate = BrownianMotion(
            self.decay_rate_diff_mean,
            self.decay_rate_diff_sigma,
            self.decay_rate_0
        )

        self.current_population = self.population_0

        # NOTE: we output initial state, so there are steps + 1 points
        yield (0, self.population_0)

        for step in range(1, steps + 1):

            self.increment()

            yield (step, self.current_population)

if __name__ == '__main__':

    predictor = PopulationPredictor(
        population_0=5000,
        growth_0=50,
        growth_diff_mean=2,
        growth_diff_sigma=2,
        decay_rate_0=.15,
        decay_rate_diff_mean=.001,
        decay_rate_diff_sigma=.001
    )

    for values in predictor.run(steps=300):
        print values
