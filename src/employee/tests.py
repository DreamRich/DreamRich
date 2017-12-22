from django.test import TestCase
from employee.factories import (
    EmployeeMainFactory, FinancialAdviserMainFactory
)
from employee.models import Employee, FinancialAdviser
from lib.tests import test_create_historic


class HistoricalEmployeeCreateTest(TestCase):

    def test_commum(self):
        test_create_historic(self, Employee, EmployeeMainFactory)

    def test_financial_adviser(self):
        test_create_historic(self, FinancialAdviser,
                             FinancialAdviserMainFactory)
