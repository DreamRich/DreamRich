from http import HTTPStatus
from dr_auth.permissions_tests_utils import (
    ClientToModel,
    UserToGeneral,
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser,
)
from dr_auth.common_tests_permissions import (
    AuthenticatedTests,
    NotAuthenticatedTests
)
from dr_auth.permissions_tests_utils import PermissionsTests


class ClientToItself(ClientToModel, UserToClient, PermissionsTests,
                     AuthenticatedTests, NotAuthenticatedTests):

    to_itself = True
    expected_status_codes = (
        ('retrieve', HTTPStatus.OK),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.OK),
        ('partial_update', HTTPStatus.OK),
    )


class ClientToClient(ClientToModel, UserToClient,
                     AuthenticatedTests, PermissionsTests,
                     NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN)
    )


class ClientToEmployee(ClientToModel, UserToEmployee, PermissionsTests,
                       AuthenticatedTests, NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class ClientToFinancialAdviser(ClientToModel, UserToFinancialAdviser,
                               PermissionsTests, AuthenticatedTests,
                               NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class ClientToRelatedGeneral(ClientToModel, UserToGeneral, PermissionsTests,
                             AuthenticatedTests,
                             NotAuthenticatedTests):

    related_name = 'financial_planning'
    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.OK),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class ClientToGeneral(ClientToModel, UserToGeneral, PermissionsTests,
                      AuthenticatedTests, NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )
