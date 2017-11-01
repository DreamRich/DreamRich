from django.test import TestCase
from lib.rates.rate import Rate


class RatesTest(TestCase):

    real_rates = [[0.06, 0.049, 0.01],
                  [0.06, 0.0, 0.06],
                  [0.01, 1, -0.495]
                  ]
    effectiveness_rate = [[0.011, 0.140],
                          [0.00, 0.00],
                          [0.001, 0.012],
                          [0.99, 3855.887]
                          ]
    difference_rates = [[0.1, 0.1, 0],
                        [0.1, 0.2, -0.5],
                        [0.2, 0.1, 1.0],
                        [0.5, 0.4, 0.25]
                        ]

    def test_real_rate_basic(self):
        for rates in self.real_rates:
            real_rate = Rate.real_rate(rates[0], rates[1])
            self.assertAlmostEqual(rates[2], real_rate, 3)

    def test_effective_rate(self):
        # Check from monthly to anual
        for rate in self.effectiveness_rate:
            new_rate = Rate.monthly_to_anual(rate[0])
            self.assertAlmostEqual(rate[1], new_rate, 3)

        # Check from anual to monthly
        for rate in self.effectiveness_rate:
            new_rate = Rate.anual_to_monthly(rate[1])
            self.assertAlmostEqual(rate[0], new_rate, 3)

    def test_difference_rate(self):
        for rates in self.difference_rates:
            difference = Rate.difference(rates[0], rates[1])
            self.assertAlmostEqual(rates[2], difference, 3)


class RatesZeroTest(TestCase):

    def test_real_rate_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            Rate.real_rate(1, -1)
        self.assertTrue(Rate.difference(1, 1 + 1e-15) < 0)

    def test_difference_zero_rate(self):
        with self.assertRaises(ZeroDivisionError):
            Rate.difference(1, 0)
        self.assertTrue(Rate.difference(1, 1e-16) > 0)
