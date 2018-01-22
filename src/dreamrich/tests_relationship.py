from django.test import TestCase
from client.factories import ActiveClientFactory
from employee.factories import FinancialAdviserFactory
from financial_planning.factories import FinancialPlanningFactory
from patrimony.factories import PatrimonyFactory
from dreamrich.utils import Relationship


class RelationshiTest(TestCase):

    def setUp(self):
        self.active_client = ActiveClientFactory()
        self.financial_planning = FinancialPlanningFactory()
        self.financial_adviser = FinancialAdviserFactory()
        self.patrimony = PatrimonyFactory()

    def test_check_relatedname(self):
        relationship = Relationship(
            self.active_client,
            self.financial_planning,
            'financial_planning',
            many=False
        )
        # pylint: disable=protected-access
        self.assertTrue(relationship._check_relatedname())

    def test_check_relatedname_swapped(self):
        relationship = Relationship(
            self.financial_planning,
            self.active_client,
            'financial_planning',
            many=False
        )
        # pylint: disable=protected-access
        self.assertTrue(relationship._check_relatedname())

    def test_hasnt_relatedname(self):
        relationship = Relationship(
            self.active_client,
            self.patrimony,
            'invalid',
            many=False
        )
        # pylint: disable=protected-access
        self.assertFalse(relationship._check_relatedname())
