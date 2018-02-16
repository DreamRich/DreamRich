from collections import namedtuple
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.db import models
from dr_auth.permissions import BasePermissions


class BaseCustomPermissionsTests(TestCase):

    class AnyModel(models.Model):

        class Meta:
            default_permissions = ()
            permissions = (
                ('retrieve_all_any_models', 'Can see all users1'),
                ('retrieve_any_any_models', 'Can see any of users1'),
                ('destroy_all_any_models', 'Can destroy all users1'),
            )

        user1 = models.ForeignKey(User)

    class AnyModelPermissions(BasePermissions):

        app_name = 'dr_auth'
        class_nick = 'any_models'
        users_models = (User, )

    class ViewMock:

        def __init__(self, user, action):
            self.user = user
            self.action = action

        def get_object(self):
            return self.user

    RequestMock = namedtuple('RequestMock', 'user')

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.permission_class = self.AnyModelPermissions()

        # pylint: disable=protected-access
        self.permission_class._initialize_checking_attrs(
            self.ViewMock(self.user1, 'retrieve'),
            self.RequestMock(self.user1)
        )
        # pylint: disable=protected-access

    def test_has_permission_to_retrieve_all(self):
        permission = Permission.objects.get(codename='retrieve_all_any_models')
        self.user1.user_permissions.add(permission)

        self.assertTrue(self.permission_class.has_permission_to('retrieve'))

    # def test_has_permission_to_retrieve_any(self):
    # def test_hasnt_permission_to_retrieve(self):
    # def test_has_permission_to_retrieve_related(self):
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
