from http import HTTPStatus
from dr_auth.permissions_tests_utils import (
    ClientToModel,
    UserToGeneral,
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser,
)
from dr_auth.permissions_tests_suites import (
    AuthenticatedTests,
    UnauthenticatedTests
)
from dr_auth.permissions_tests_utils import PermissionsTests


class ClientToItself(ClientToModel, UserToClient, PermissionsTests,
                     AuthenticatedTests, UnauthenticatedTests):

    to_itself = True
    expected_status_codes = (
        ('retrieve', HTTPStatus.OK),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.OK),
        ('partial_update', HTTPStatus.OK),
    )


class ClientToClient(ClientToModel, UserToClient, PermissionsTests,
                     AuthenticatedTests, UnauthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN)
    )


class ClientToEmployee(ClientToModel, UserToEmployee, PermissionsTests,
                       AuthenticatedTests, UnauthenticatedTests):

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
                               UnauthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class ClientToRelatedGeneral(ClientToModel, UserToGeneral, PermissionsTests,
                             AuthenticatedTests, UnauthenticatedTests):

    related_name = 'financial_planning'
    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.OK),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class ClientToGeneral(ClientToModel, UserToGeneral, PermissionsTests,
                      AuthenticatedTests, UnauthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )
