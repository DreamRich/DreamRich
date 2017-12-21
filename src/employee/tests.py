from django.test import TestCase
from employee.factories import (
    EmployeeMainFactory, FinancialAdviserMainFactory
)
from employee.models import Employee, FinancialAdviser


class HistoricalEmployeeCreateTest(TestCase):

    def _test_create_historic(self, model, factory):
        self.assertEqual(model.history.count(), 0)
        factory()
        self.assertEqual(model.history.count(), 2)

    def test_commum(self):
        self._test_create_historic(Employee, EmployeeMainFactory)

    def test_financial_adviser(self):
        self._test_create_historic(FinancialAdviser,
            FinancialAdviserMainFactory)
