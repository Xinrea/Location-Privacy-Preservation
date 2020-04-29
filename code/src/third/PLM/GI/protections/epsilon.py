# encoding=utf-8
class Epsilon:
    """
    Privacy budget management.
    """

    def __init__(self, epsilon, strategy):
        assert isinstance(epsilon, float)
        assert issubclass(strategy, EpsilonAllocationStrategy)

        self.epsilon = epsilon
        self.strategy = strategy


class EpsilonAllocationStrategy:
    """
    A strategy to divide total epsilon into slots, where each slot is used for a perturbation.
    """

    total_eps = 1.0

    @classmethod
    def divide(cls, total_eps, data, **kwargs):
        """
        Divide the total epsilon into some slots.
        :param total_eps: float
        :param data: list, trajectories or check-ins
        :return: list, a list of floating numbers
        """

        pass


class UniformAllocation(EpsilonAllocationStrategy):
    """
    Divide the total epsilon into uniform slots.
    """

    @classmethod
    def divide(cls, total_eps, data, **kwargs):
        return [total_eps / len(data), ] * len(data)


class ExponentialAllocation(EpsilonAllocationStrategy):
    """
    Divide the total epsilon into geometric series {total_eps / 2^i}, i = 1, ... since sum(total_eps / 2^i) = total_eps.
    0-th,  1-th, ...,   i-th, ...,  (n-1)-th :
    x   , x/2^1, ...,  x/2^i, ...,  x/2^(n-1) ---> sum to total_eps
    Then, x, i.e., the first_eps, = total_eps / (2 - 2 ^ (1 - n))
    """

    @classmethod
    def divide(cls, total_eps, data, **kwargs):
        first_eps = total_eps / (2 - 2 ** (1 - len(data)))
        return [first_eps / (2 ** i) for i in range(len(data))]
