import unittest
from src.calculator import add, divide, mean, power

class TestCalculatorUnit(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertAlmostEqual(add(2.5, 0.5), 3.0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_mean(self):
        self.assertEqual(mean([2, 4, 6]), 4)
        self.assertIsNone(mean([]))

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(9, 0.5), 3)

if __name__ == "__main__":
    unittest.main()