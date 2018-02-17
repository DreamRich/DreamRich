from collections import namedtuple
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Permission
from django.db import models
from dr_auth.permissions import BasePermissions
from dreamrich.utils import Relationship


class BaseCustomPermissionsTests(TestCase):

    class AnyModel(models.Model):

        class Meta:
            default_permissions = ()
            permissions = (
                ('retrieve_all_anymodels', 'Can see all anymodels'),
                ('retrieve_any_anymodels', 'Can see any of anymodels'),
                ('update_related_anymodels', 'Can update all anymodels'),
            )

        user = models.ForeignKey(User, null=True)

    class AnyModelPermissions(BasePermissions):

        app_name = 'dr_auth'
        class_nick = 'anymodels'
        users_models = (User, )

    class ViewMock:

        def __init__(self, user, consulted, action):
            self.user = user
            self.action = action
            self.consulted = consulted

        def get_object(self):
            return self.consulted

    RequestMock = namedtuple('RequestMock', 'user')

    def setUp(self):
        self.user = User.objects.create(username='user')
        self.permission_class = self.AnyModelPermissions()
        self.permission_class.consulted = self.AnyModel.objects.create()

        # pylint: disable=protected-access
        self.permission_class._initialize_checking_attrs(
            self.ViewMock(self.user, self.permission_class.consulted,
                          'retrieve'),
            self.RequestMock(self.user)
        )
        # pylint: disable=protected-access

    def test_initialize_checking_attrs(self):
        '''
        Used on setUp() and too simple. Check only if attributes are filled.
        '''

        self.assertTrue(all((
            self.permission_class.view,
            self.permission_class.request,
            self.permission_class.user,
            self.permission_class.user_from_project
        )))

    def test_has_permission_to_retrieve_all(self):
        permission = Permission.objects.get(codename='retrieve_all_anymodels')
        self.user.user_permissions.add(permission)

        self.assertTrue(self.permission_class.has_permission_to('retrieve'))

    def test_hasnt_permission_to_retrieve(self):
        self.assertFalse(self.permission_class.has_permission_to('retrieve'))

    def test_has_permission_to_update_related(self):
        def related_user_checker(self=self.permission_class):
            relationship = Relationship(self.user, self.consulted,
                                        related_name='anymodel_set')

            return relationship.has_relationship()

        permission_codename = 'update_related_anymodels'
        permission = Permission.objects.get(codename=permission_codename)

        self.user.user_permissions.add(permission)
        self.user.anymodel_set.add(self.permission_class.consulted)

        # pylint: disable=attribute-defined-outside-init
        self.permission_class.related_user_checker = related_user_checker
        # pylint: disable=attribute-defined-outside-init

        self.assertTrue(self.permission_class.has_permission_to('update'))

    def test_hasnt_permission_to_update_related(self):
        self.user.anymodel_set.add(self.permission_class.consulted)

        self.assertFalse(self.permission_class.has_permission_to('update'))

    def test_has_permission_to_update_related_without_method(self):
        permission_codename = 'update_related_anymodels'
        permission = Permission.objects.get(codename=permission_codename)

        self.user.user_permissions.add(permission)
        self.user.anymodel_set.add(self.permission_class.consulted)

        self.assertFalse(self.permission_class.has_permission_to('update'))

    def test_has_any_permission(self):
        permission = Permission.objects.get(codename='retrieve_all_anymodels')
        self.user.user_permissions.add(permission)

        self.assertTrue(
            self.permission_class.has_any_permission(
                'dr_auth.retrieve_all_anymodels',
                'invalid'
            )
        )

    def test_has_any_permission_fail(self):
        self.assertFalse(
            self.permission_class.has_any_permission(
                'dr_auth.retrieve_all_anymodels',
                'invalid'
            )
        )

    def test_has_passed_related_checks(self):
        # pylint: disable=attribute-defined-outside-init
        self.permission_class.related_user_checker = lambda: True
        # pylint: disable=attribute-defined-outside-init

        self.assertTrue(self.permission_class.has_passed_related_checks())

    def test_hasnt_passed_related_checks(self):
        # pylint: disable=attribute-defined-outside-init
        self.permission_class.related_user_checker = lambda: False
        # pylint: disable=attribute-defined-outside-init

        self.assertFalse(self.permission_class.has_passed_related_checks())

    def test_get_checker_method_have_attr(self):
        # pylint: disable=attribute-defined-outside-init
        self.permission_class.related_user_checker = lambda: False
        # pylint: disable=attribute-defined-outside-init

        self.assertEqual(
            self.permission_class.related_user_checker,
            self.permission_class._get_checker_method()
        )

    def test_get_checker_method_havent_attr(self):
        checker_method = self.permission_class._get_checker_method()
        self.assertFalse(checker_method())

    def test_get_user_from_project(self):
        self.permission_class.users_models = (User,)
        user_from_project = self.permission_class._get_user_from_project()

        self.assertTrue(
            user_from_project.__class__ is User
        )

    def test_get_user_from_project_not_found(self):
        self.permission_class.users_models = tuple()

        with self.assertRaisesMessage(ObjectDoesNotExist,
                                      "Couldn't find user model"
                                      " for the user provided."):
            self.permission_class._get_user_from_project()

    def test_check_children_attrs(self):
        self.permission_class._check_children_attrs()

    def test_check_children_attrs_fail(self):
        self.permission_class.users_models = None

        with self.assertRaisesMessage(AttributeError,
                                      "Attribute 'users_models' was"
                                      " not filled at child class"):
            self.permission_class._check_children_attrs()

    def test_fill_consulted_attr_not_convenient_view_action(self):
        self.permission_class.view.action = 'list'
        self.permission_class._fill_consulted_attr()

        self.assertIsNone(self.permission_class.consulted)

    def test_fill_consulted_attr_convenient_view_action(self):
        expected_consulted = self.permission_class.consulted

        self.permission_class.view.action = 'retrieve'
        self.permission_class._fill_consulted_attr()

        self.assertEqual(
            expected_consulted,
            self.permission_class.consulted
        )
