from django.test import TestCase
from client.factories import ActiveClientFactory
from employee.factories import FinancialAdviserFactory
from financial_planning.factories import FinancialPlanningFactory
from patrimony.factories import PatrimonyFactory
from dreamrich.utils import Relationship


class RelationshipTest(TestCase):

    def setUp(self):
        self.active_client = ActiveClientFactory()
        self.financial_planning = FinancialPlanningFactory()
        self.financial_adviser = FinancialAdviserFactory()
        self.patrimony = PatrimonyFactory()

    def test_make_relationship_many(self):
        self.assertNotIn(self.active_client,
                         self.financial_adviser.clients.all())

        Relationship(self.financial_adviser, self.active_client,
                     many=True, related_name='clients').make()

        self.assertIn(self.active_client,
                      self.financial_adviser.clients.all())

    def test_make_relationship_not_many(self):
        self.assertFalse(hasattr(self.active_client, 'financial_planning'))

        Relationship(self.active_client, self.financial_planning,
                     related_name='financial_planning', many=False).make()

        self.assertEqual(self.active_client.financial_planning.id,
                         self.financial_planning.id)

    def test_has_relationship_not_many(self):
        self.active_client.financial_planning = self.financial_planning

        relationship = Relationship(
            self.active_client, self.financial_planning,
            related_name='financial_planning', many=False
        )

        self.assertTrue(relationship.has_relationship())

    def test_hasnt_relationship_not_many(self):
        relationship = Relationship(
            self.active_client,
            self.financial_planning,
            related_name='financial_planning',
            many=False
        )
        self.assertFalse(relationship.has_relationship())

    def test_has_relationship_many(self):
        self.financial_adviser.clients.add(self.active_client)

        relationship = Relationship(
            self.active_client, self.financial_adviser,
            related_name='clients', many=True
        )

        self.assertTrue(relationship.has_relationship())

    def test_hasnt_relationship_many(self):
        relationship = Relationship(self.active_client, self.financial_adviser,
                                    related_name='clients', many=True)
        self.assertFalse(relationship.has_relationship())

    def test_str_many(self):
        relationship = Relationship(self.financial_planning, self.patrimony)
        self.assertEqual(str(relationship), 'FinancialPlanning has Patrimony')

    def test_str_not_many(self):
        relationship = Relationship(self.financial_planning, self.patrimony,
                                    many=True)
        self.assertEqual(str(relationship),
                         'FinancialPlanning has many Patrimony')

    def test_is_all_attributes_filled(self):
        relationship = Relationship(self.active_client,
                                    self.financial_planning)

        # pylint: disable=protected-access
        self.assertRaisesMessage(
            relationship._is_all_attributes_filled,
            'Not enough information, many is missing.'
        )
        relationship.many = False

        self.assertRaisesMessage(
            relationship._is_all_attributes_filled,
            'Not enough information, related_name is missing.'
        )
        relationship.related_name = 'any'

        relationship._is_all_attributes_filled()  # Fail if Error

    def test_check_relatedname(self):
        relationship = Relationship(
            self.active_client, self.financial_planning,
            related_name='financial_planning', many=False
        )
        # pylint: disable=protected-access
        relationship._check_relatedname()

    def test_check_relatedname_swapped(self):
        relationship = Relationship(
            self.financial_planning, self.active_client,
            related_name='financial_planning', many=False
        )
        # pylint: disable=protected-access
        relationship._check_relatedname()  # Fail if Error

    def test_hasnt_relatedname(self):
        relationship = Relationship(
            self.active_client, self.patrimony,
            related_name='invalid', many=False
        )
        # pylint: disable=protected-access
        self.assertRaisesMessage(relationship._check_relatedname,
                                 'related_name passed is not valid for any')

    def test_fill_missing_attributes(self):
        relationship = Relationship(self.active_client,
                                    self.financial_planning)
        self.assertEqual(relationship.primary, self.active_client)
        self.assertEqual(relationship.secondary, self.financial_planning)
        self.assertIsNone(relationship.many)
        self.assertIsNone(relationship.related_name)

        # pylint: disable=protected-access
        relationship._fill_missing_attributes(many=False)
        self.assertEqual(relationship.primary, self.active_client)
        self.assertEqual(relationship.secondary, self.financial_planning)
        self.assertFalse(relationship.many)
        self.assertIsNone(relationship.related_name)

        related_name = 'any'
        relationship._fill_missing_attributes(related_name=related_name)
        self.assertEqual(relationship.primary, self.active_client)
        self.assertEqual(relationship.secondary, self.financial_planning)
        self.assertFalse(relationship.many)
        self.assertEqual(relationship.related_name, related_name)

    def test_fill_missing_attributes_substituting(self):
        relationship = Relationship(self.active_client,
                                    self.financial_planning)

        primary = self.patrimony
        # pylint: disable=protected-access
        relationship._fill_missing_attributes(primary=primary)
        self.assertEqual(relationship.primary, primary)
