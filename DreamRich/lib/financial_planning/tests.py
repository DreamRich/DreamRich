from django.test import TestCase
from lib.financial_planning.flow import create_array_change_annual
from financial_planning.models import FlowUnitChange


class FlowTest(TestCase):
    changes = []
    change1 = FlowUnitChange(year=2018, annual_value=2000)
    changes.append(change1)
    change2 = FlowUnitChange(year=2020, annual_value=-5000)
    changes.append(change2)

    def test_create_array_change_annual(self):
        array_compare = [0, 2000, 0, -5000, 0, 0, 0, 0, 0, 0]
        self.assertEqual(array_compare, create_array_change_annual(
            self.changes, 10, 2017))
