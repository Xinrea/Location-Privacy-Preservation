# encoding=utf-8
import unittest

from GI.protections.noise import UniformAllocation, ExponentialAllocation


class TestUniformAllocation(unittest.TestCase):
    def test_divide(self):
        total_eps = 1.0
        data = [1, ] * 10
        expected_slot = total_eps / len(data)
        found_slots = UniformAllocation.divide(total_eps, data)
        # check whether found slots sum to total_eps
        self.assertAlmostEqual(total_eps, sum(found_slots), delta=0.001)
        # checkin whether each slot equals to expected_slot
        for found_slot in found_slots:
            self.assertAlmostEqual(expected_slot, found_slot, delta=0.001)


class TestExponentialAllocation(unittest.TestCase):
    def test_divide(self):
        total_eps = 1.0
        data = [1, ] * 10
        found_slots = ExponentialAllocation.divide(total_eps, data)
        # check whether found slots sum to total_eps
        self.assertAlmostEqual(total_eps, sum(found_slots), delta=0.001)
        # check whether the i-th slot is half of the (i - 1)-th slot
        for i in range(1, len(data)):
            self.assertAlmostEqual(found_slots[i - 1] / 2, found_slots[i], delta=0.001)


if __name__ == '__main__':
    unittest.main()
