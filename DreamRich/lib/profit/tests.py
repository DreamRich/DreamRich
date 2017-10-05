from django.test import TestCase
from lib.profit.profit import actual_rate


class ProfitTest(TestCase):

    NET_PROFITABILITY = 0.0879
    IPCA = 0.0750
    CDI = 0.1213
    WALLET_PROFITABILITY_TARGET = 1.1
    INCOME_TAX = 0.1750

    PROFIT_ANNUAL = 0.0431
    PROFIT_NET = 0.012
    PROFIT_NET_SUGGESTED = 0.0326

    def test_annual(self):
        profit_annual = actual_rate(self.CDI, self.IPCA)
        self.assertAlmostEqual(profit_annual, self.PROFIT_ANNUAL, 4)

    def test_net_annual(self):
        profit_net_annual = actual_rate(
            self.NET_PROFITABILITY, self.IPCA)
        self.assertAlmostEqual(profit_net_annual, self.PROFIT_NET, 4)

