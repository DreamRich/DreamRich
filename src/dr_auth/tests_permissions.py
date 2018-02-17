from collections import namedtuple
from django.test import TestCase
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
                ('destroy_all_anymodels', 'Can destroy all anymodels'),
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

    # def test_has_any_permission(self):
    # def test_has_any_permission_fail(self):
    # def test_has_passed_related_checks(self):
    # def test_has_passed_related_checks_fail(self):
    # def test_get_checker_method_have_attr(self):
    # def test_get_checker_method_havent_attr(self):
    # def test_get_user_from_project(self):
    # def test_get_user_from_project_fail(self):
    # def test_check_children_params(self):
    # def test_check_children_params_fail(self):
    # def test_fill_consulted_attr(self):
    # def test_fill_consulted_attr_fail(self):
