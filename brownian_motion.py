import numpy as np

class BrownianMotion(object):

    class CurrentState(object):

        def __init__(self, initial_value):

            self._current_value = initial_value
            self._step = 0

        def increment(self, increment):
            self._current_value += increment
            self._step += 1

            return self.current_value

        @property
        def current_value(self):

            return self._current_value

    def __init__(self, mean, sigma, initial_value):

        self.mean = mean
        self.sigma = sigma
        self.initial_value = initial_value
        self.current_state = self.CurrentState(initial_value)

    def sample(self):

        increment = np.random.normal(self.mean, self.sigma, 1)[0]

        return self.increment(increment)

    @property
    def current_value(self):

        return self.current_state.current_value

    def increment(self, increment):

        return self.current_state.increment(increment)
