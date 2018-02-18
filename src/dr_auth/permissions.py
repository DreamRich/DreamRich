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
        self._check_children_attrs()

        if request.user.is_authenticated():
            self._initialize_checking_attrs(view, request)

            return self.has_permission_to(self.view.action)
        return False

    def has_permission_to(self, permission_action):
        get_possible_permissions = self._get_possible_permissions

        possible_permissions = get_possible_permissions(permission_action)
        related_permission = possible_permissions.pop('related')

        has_related_permission = self.has_any_permission(related_permission)

        permissions_names = list(possible_permissions.values())

        return (self.has_any_permission(*permissions_names) or
                has_related_permission and self.has_passed_related_checks())

    def has_any_permission(self, *permissions_codenames):
        for permission in permissions_codenames:
            if self.user.has_perm(permission):
                return True
        return False

    def has_passed_related_checks(self):
        self._fill_consulted_attr()

        has_passed_on_checker = self._get_checker_method()

        return has_passed_on_checker()

    def _initialize_checking_attrs(self, view, request):
        '''
        Fills attrs generateds at checking time
        '''
        self.view = view
        self.request = request

        self.user = self.request.user
        self.user_from_project = self._get_user_from_project()

    def _get_possible_permissions(self, permission_action):
        ownerships_types = ('all', 'any', 'related', 'not_related')

        permission_template = '{}.{}_{}_{}'.format(
            self.app_name, permission_action, '{}', self.class_nick
        )

        possible_permissions = {
            ownership: permission_template.format(ownership)
            for ownership in ownerships_types
        }

        # Case with no ownership
        possible_permissions['no_owner'] = '{}.{}_{}'.format(
            self.app_name, permission_action, self.class_nick
        )

        return possible_permissions

    def _get_checker_method(self):
        class_name = self.user_from_project.__class__.__name__
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

    def _check_children_attrs(self):
        required_attrs_names = {
            self.app_name: 'app_name',
            self.class_nick: 'class_nick',
            self.users_models: 'users_models'
        }

        for attr, attr_name in required_attrs_names.items():
            if not attr:
                raise AttributeError(
                    "Attribute '{}' was not filled at child class"
                    .format(attr_name)
                )

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
