from django.test import TestCase
from lib.patrimony.patrimony import Patrimony

class PatrimonyTest(TestCase):

  assets = [1000, 2000, 3000, 4000]
  debts = [500, 700]
  sources_of_income = [3000, 1000, 1500, 7500]
  vacation_bonus = 6000
  thirteenth_salary = 7000
  current_investment_net = 8800
  current_investment_immobilized = 10000
  monthly_income = 13000
  monthly_income_bonus = 14083.33

  def test_current_investment_net(self):
    current_net = Patrimony.current_investment_net(self.assets, self.debts)
    self.assertEqual(current_net, self.current_investment_net)

  def test_current_investment_immobilized(self):
    current_immobilized = Patrimony.current_investment_immobilized(self.assets)
    self.assertEqual(current_immobilized, self.current_investment_immobilized)

  def test_monthly_income(self):
    income = Patrimony.monthly_income(self.sources_of_income)
    self.assertEqual(income, self.monthly_income)

  def test_monthly_income_bonus(self):
    income = Patrimony.monthly_income_bonus(self.sources_of_income, self.vacation_bonus, self.thirteenth_salary)
    self.assertAlmostEqual(income, self.monthly_income_bonus, 2)
