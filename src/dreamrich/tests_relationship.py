from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
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
                     related_name='clients').make()

        self.assertIn(self.active_client,
                      self.financial_adviser.clients.all())

    def test_make_relationship_not_many(self):
        self.assertFalse(hasattr(self.active_client, 'financial_planning'))

        Relationship(self.active_client, self.financial_planning,
                     related_name='financial_planning').make()

        self.assertTrue(hasattr(self.active_client, 'financial_planning'))
        self.assertEqual(self.active_client.financial_planning.id,
                         self.financial_planning.id)

    def test_passing_attributes_to_make(self):
        relationship = Relationship(self.active_client,
                                    self.financial_planning)

        relationship.make(related_name='financial_planning')

        self.assertEqual(self.active_client.financial_planning,
                         self.financial_planning)

    def test_has_relationship_not_many(self):
        self.active_client.financial_planning = self.financial_planning

        relationship = Relationship(
            self.active_client, self.financial_planning,
            related_name='financial_planning'
        )

        self.assertTrue(relationship.has_relationship())

    def test_hasnt_relationship_not_many(self):
        relationship = Relationship(
            self.active_client, self.financial_planning,
            related_name='financial_planning'
        )
        self.assertFalse(relationship.has_relationship())

    def test_has_relationship_many(self):
        self.financial_adviser.clients.add(self.active_client)

        relationship = Relationship(
            self.active_client, self.financial_adviser,
            related_name='clients'
        )

        self.assertTrue(relationship.has_relationship())

    def test_hasnt_relationship_many(self):
        relationship = Relationship(self.active_client, self.financial_adviser,
                                    related_name='clients')
        self.assertFalse(relationship.has_relationship())

    def test_has_nested_relationsihp(self):
        self.financial_adviser.clients.add(self.active_client)
        self.active_client.financial_planning = self.financial_planning

        relationship = Relationship(self.financial_adviser,
                                    related_name='clients')

        self.assertTrue(
            relationship.has_nested_relationship(
                Relationship.RelatedMeta('clients', self.active_client.pk),
                Relationship.RelatedMeta('financial_planning', None)
            )
        )

    def test_hasnt_nested_relationship(self):
        relationship = Relationship(self.financial_adviser,
                                    related_name='clients')

        self.assertFalse(
            relationship.has_nested_relationship(
                Relationship.RelatedMeta('clients', self.active_client.pk),
                Relationship.RelatedMeta('financial_planning', None)
            )
        )

    def test_is_many(self):
        relationship = Relationship(self.financial_adviser,
                                    related_name='clients')

        self.assertTrue(relationship.is_many())

    def test_isnt_many(self):
        relationship = Relationship(self.active_client,
                                    related_name='financial_planning')

        self.assertFalse(relationship.is_many())

    def test_isnt_many_related(self):
        self.active_client.financial_planning = self.financial_planning
        relationship = Relationship(self.active_client,
                                    related_name='financial_planning')

        self.assertFalse(relationship.is_many())

    def test_get_related_not_many(self):
        self.active_client.financial_planning = self.financial_planning

        relationship = Relationship(self.active_client,
                                    related_name='financial_planning')

        related = relationship.get_related()

        self.assertEqual(related, self.financial_planning)

    def test_get_related_many(self):
        second_client = ActiveClientFactory()

        self.financial_adviser.clients.add(self.active_client, second_client)

        relationship = Relationship(self.financial_adviser,
                                    related_name='clients')

        related = relationship.get_related()

        self.assertEqual(related, second_client)

    def test_get_related_many_wrong_pk(self):
        second_client = ActiveClientFactory()

        self.financial_adviser.clients.add(self.active_client, second_client)

        wrong_pk = 12312312
        relationship = Relationship(self.financial_adviser,
                                    related_name='clients', pk=wrong_pk)

        with self.assertRaisesMessage(ObjectDoesNotExist,
                                      "Was not possible to get the object"
                                      " indicated by the information passed."
                                      " 'pk' not found."):
            relationship.get_related()

    def test_get_related_not_many_none(self):
        self.assertFalse(hasattr(self.active_client, 'financial_planning'))

        relationship = Relationship(self.active_client,
                                    related_name='financial_planning')

        related = relationship.get_related()

        self.assertIsNone(related)

    def test_get_related_many_none(self):
        self.assertIsNone(self.financial_adviser.clients.last())

        relationship = Relationship(self.financial_adviser,
                                    related_name='clients')

        related = relationship.get_related()

        self.assertIsNone(related)

    def test_get_related_return_manager(self):
        relationship = Relationship(self.financial_adviser,
                                    related_name='clients')
        related_manager = relationship.get_related(return_manager=True)

        self.assertEqual(related_manager, self.financial_adviser.clients)

    def test_get_related_return_manager_fail_one_to_one(self):
        self.active_client.financial_planning = self.financial_planning
        relationship = Relationship(self.active_client,
                                    related_name='financial_planning')

        with self.assertRaisesMessage(AttributeError,
                                      "'return_manager' is valid only for"
                                      " \"to many\" relationships"):
            relationship.get_related(return_manager=True)

    def test_get_related_return_manager_fail_no_related(self):
        relationship = Relationship(self.active_client,
                                    related_name='financial_planning')

        with self.assertRaisesMessage(AttributeError,
                                      "'return_manager' is valid only for"
                                      " \"to many\" relationships"):
            relationship.get_related(return_manager=True)

    def test_get_nested_related(self):
        self.active_client.financial_planning = self.financial_planning
        self.financial_planning.patrimony = self.patrimony

        relationship = Relationship(self.active_client,
                                    related_name='financial_planning')

        last_related = relationship.get_nested_related(
            Relationship.RelatedMeta('financial_planning', None),
            Relationship.RelatedMeta('patrimony', None)
        )

        self.assertEqual(last_related, self.patrimony)

    def test_get_nested_related_none_related(self):
        self.financial_planning.patrimony = self.patrimony

        relationship = Relationship(self.active_client,
                                    related_name='financial_planning')

        with self.assertRaisesMessage(AttributeError,
                                      "Not possible getting nested related."
                                      " 'financial_planning' related name got"
                                      " a None object."):
            relationship.get_nested_related(
                Relationship.RelatedMeta('financial_planning', None),
                Relationship.RelatedMeta('patrimony', None)
            )

    def test_str_many(self):
        relationship = Relationship(self.financial_planning, self.patrimony)
        self.assertEqual(str(relationship), '(FinancialPlanning : Patrimony)')

    def test_str_not_many(self):
        relationship = Relationship(self.financial_planning, self.patrimony)
        self.assertEqual(str(relationship), '(FinancialPlanning : Patrimony)')

    def test_check_all_core_attributes_filled(self):
        relationship = Relationship(self.active_client)

        # pylint: disable=protected-access
        with self.assertRaisesMessage(AttributeError,
                                      "Not enough information, 'secondary'"
                                      " is missing or None."):
            relationship._check_all_core_attributes_filled()

        relationship.secondary = self.financial_planning

        with self.assertRaisesMessage(AttributeError,
                                      "Not enough information, 'related_name'"
                                      " is missing or None."):
            relationship._check_all_core_attributes_filled()
        relationship.related_name = 'any'

        relationship._check_all_core_attributes_filled()  # Fail if Error

    def test_check_relatedname(self):
        relationship = Relationship(
            self.active_client, self.financial_planning,
            related_name='financial_planning'
        )
        # pylint: disable=protected-access
        relationship._check_relatedname()

    def test_check_relatedname_swapped(self):
        relationship = Relationship(
            self.financial_planning, self.active_client,
            related_name='financial_planning'
        )
        # pylint: disable=protected-access
        relationship._check_relatedname()  # Fail if Error

    def test_invalid_relatedname(self):
        relationship = Relationship(self.active_client, self.patrimony,
                                    related_name='invalid')

        # pylint: disable=protected-access
        with self.assertRaisesMessage(AttributeError,
                                      "'invalid' is not a valid related_name"
                                      " for 'ActiveClient' nor for"
                                      " 'Patrimony'."):
            relationship._check_relatedname()

    def test_fill_attributes(self):
        relationship = Relationship(self.active_client,
                                    self.financial_planning)
        self.assertEqual(relationship.primary, self.active_client)
        self.assertEqual(relationship.secondary, self.financial_planning)
        self.assertIsNone(relationship.related_name)

        # pylint: disable=protected-access
        related_name = 'any'
        relationship._fill_attributes(related_name=related_name)
        self.assertEqual(relationship.primary, self.active_client)
        self.assertEqual(relationship.secondary, self.financial_planning)
        self.assertEqual(relationship.related_name, related_name)

    def test_fill_attributes_substituting(self):
        relationship = Relationship(self.active_client,
                                    self.financial_planning)

        primary = self.patrimony
        # pylint: disable=protected-access
        relationship._fill_attributes(primary=primary)
        self.assertEqual(relationship.primary, primary)
