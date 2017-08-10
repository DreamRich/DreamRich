from django.test import TestCase
from lib.patrimony.patrimony import Patrimony

class PatrimonyTest(TestCase):

  assets = [1000, 2000, 3000, 4000]
  debts = [500, 700]
  current_investment_net = 8800
  current_investment_immobilized = 10000

  def test_current_investment_net(self):
    current_net = Patrimony.current_investment_net(self.assets, self.debts)
    self.assertEqual(current_net, self.current_investment_net)

  def test_current_investment_immobilized(self):
    current_immobilized = Patrimony.current_investment_immobilized(self.assets)
    self.assertEqual(current_immobilized, self.current_investment_immobilized)