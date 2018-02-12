from functools import reduce
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from client.models import ActiveClient
from employee.models import Employee, FinancialAdviser
from dreamrich.utils import Relationship
from .models_permissions import USERS_PERMISSIONS_INFO


class BasePermissions(permissions.BasePermission):

    class Meta:
        abstract = True

    authorized = False
    view = None
    request = None
    user = None
    user_from_project = None
    consulted = None

    # Same used when defining models permissions
    app_name = ''
    class_nick = ''

    # Filled with models of users, users that can try to access views
    # protected by children of this permission class
    users_models = ()

    def has_permission(self, request, view):
        if request.user.is_authenticated():
            self._check_children_params()

            self.view = view
            self.request = request
            self.user = self.request.user
            self.user_from_project = self._get_user_from_project()

            return self.has_permission_to(self.view.action)
        return False

    def has_permission_to(self, permission_action):
        allowed_permissions = [
            '{}.{}_{}{}'.format(
                self.app_name, permission_action, ownership, self.class_nick
            ) for ownership in ('', 'all_', 'any_', 'related_')
        ]

        related_permission = allowed_permissions.pop()
        has_related_permission = self.has_any_permission(related_permission)

        return (self.has_any_permission(*allowed_permissions) or
                has_related_permission and self.has_passed_related_checks())

    def has_any_permission(self, *permissions_codenames):
        for permission in permissions_codenames:
            if self.user.has_perm(permission):
                return True
        return False

    def has_passed_related_checks(self):
        self._fill_consulted_attr()

        # users_class_names = [user.__name__ for user in self.users_models]

        # related_checkers = {
        #     class_name: get_checker_method(class_name)
        #     for class_name in users_class_names
        # }

        # user_class_name = self.user_from_project.__class__.__name__
        # try:
        #     checker_function = related_checkers[user_class_name]
        # except KeyError:
        #     raise AttributeError(
        #         "Model '{}' not listed at 'users_models' attribute."
        #         " All models from users must be listed on it."
        #         .format(user_class_name)
        #     )

        has_passed_on_checker = self._get_checker_method(
            self.user_from_project.__class__.__name__
        )

        return has_passed_on_checker()

    def _get_checker_method(self, class_name):
        method_name = 'related_' + class_name.lower() + '_checker'

        if not hasattr(self, method_name):
            setattr(self, method_name, lambda: False)

        return getattr(self, method_name)

    # We don't want an instance of django.contrib.auth.models.User
    def _get_user_from_project(self):
        for model in self.users_models:
            try:
                user_object = model.objects.get(username=self.user.username)
                break
            except ObjectDoesNotExist:
                pass
        else:
            raise ObjectDoesNotExist("Couldn't find user model"
                                     " for the user provided.")
        return user_object

    def _check_children_params(self):
        required_params = {self.app_name: 'app_name',
                           self.class_nick: 'class_nick'}

        if not all(required_params.keys()):
            raise AttributeError('Attribute {} was not filled at child class')

    # To be used for children classes
    def _fill_consulted_attr(self):
        self.consulted = None

        # Http methods which are not directed to specific instances would raise
        # exception
        if self.view.action not in ('list', 'post'):
            self.consulted = self.view.get_object()


class ProjectBasePermissions(BasePermissions):

    users_models = (ActiveClient, FinancialAdviser, Employee)


class ClientsPermissions(ProjectBasePermissions):

    app_name = 'client'
    class_nick = USERS_PERMISSIONS_INFO.client.nick

    def related_activeclient_checker(self):
        return self.user_from_project.pk == self.consulted.pk

    def related_financialadviser_checker(self):
        relationship = Relationship(self.consulted,
                                    self.user_from_project,
                                    related_name='clients')

        return relationship.has_relationship()


class EmployeesPermissions(ProjectBasePermissions):

    app_name = 'employee'
    class_nick = USERS_PERMISSIONS_INFO.employee.nick

    def related_employee_checker(self):
        return (self.consulted.pk == self.user_from_project.pk and
                self.view.action in ('update', 'partial_update', 'retrieve'))


class FinancialAdvisersPermissions(ProjectBasePermissions):

    app_name = 'employee'
    class_nick = USERS_PERMISSIONS_INFO.financial_adviser.nick

    def related_financialadviser_checker(self):
        return self.consulted.pk == self.user_from_project.pk


class GeneralPermissions(ProjectBasePermissions):

    app_name = 'dreamrich'
    class_nick = 'general'

    def related_activeclient_checker(self):
        relationship = Relationship(self.user_from_project,
                                    self.consulted,
                                    related_name='financial_planning')

        return relationship.has_relationship()

    def related_financialadviser_checker(self):
        relationship = Relationship(self.user_from_project,
                                    related_name='clients')

        related_client_pk = self._get_active_client_pk()
        related_meta_class = Relationship.RelatedMeta

        return relationship.has_nested_relationship(
            related_meta_class('clients', related_client_pk),
            related_meta_class('financial_planning', None)
        )

    def _get_active_client_pk(self):
        '''
        Covers the types of relationships that self.consulted can have
        with the class which represents General
        '''

        # The more towards the end, the deeper
        prefixes_depths = [
            '.active_client.pk',
            '.financial_planning',
            '.patrimony'
        ]

        paths_to_client_pk = ['']
        paths_to_client_pk = [prefixe + paths_to_client_pk[-1] for prefixe in
                              prefixes_depths]

        for possible_path in paths_to_client_pk:
            iterable = [self.consulted] + possible_path.split('.')[1:]
            try:
                active_client_pk = reduce(getattr, iterable)
                break
            except AttributeError:
                pass
        else:
            raise AttributeError(
                'The type of relationship that {} has with the class'
                ' representing General is not listed in possibilities'
                ' for getting ActiveClient pk'.format(self.consulted)
            )

        return active_client_pk
