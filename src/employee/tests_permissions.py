from http import HTTPStatus
from dr_auth.permissions_tests_utils import (
    EmployeeToModel,
    FinancialAdviserToModel,
    UserToClient,
    UserToEmployee,
    UserToFinancialAdviser,
    UserToGeneral,
    PermissionsTests
)
from dr_auth.common_tests_permissions import (
    AuthenticatedTests,
    NotAuthenticatedTests
)


class EmployeeToItself(EmployeeToModel, UserToEmployee, PermissionsTests,
                       AuthenticatedTests, NotAuthenticatedTests):

    to_itself = True
    expected_status_codes = (
        ('retrieve', HTTPStatus.OK),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.OK),
        ('partial_update', HTTPStatus.OK),
    )


class EmployeeToEmployee(EmployeeToModel, UserToEmployee, PermissionsTests,
                         AuthenticatedTests, NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class EmployeeToClient(EmployeeToModel, UserToClient, PermissionsTests,
                       AuthenticatedTests, NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.OK),
        ('retrieve', HTTPStatus.OK),
        ('create', HTTPStatus.CREATED),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class EmployeeToFinancialAdviser(EmployeeToModel, UserToFinancialAdviser,
                                 PermissionsTests,
                                 AuthenticatedTests,
                                 NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.FORBIDDEN),
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class EmployeeToGeneral(EmployeeToModel, UserToGeneral, PermissionsTests,
                        AuthenticatedTests, NotAuthenticatedTests):

    expected_status_codes = (
        ('retrieve', HTTPStatus.FORBIDDEN),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
        ('create', HTTPStatus.FORBIDDEN),
    )


class FinanicalAdviserToItself(FinancialAdviserToModel, UserToFinancialAdviser,
                               PermissionsTests, AuthenticatedTests,
                               NotAuthenticatedTests):

    expected_status_codes = (
        ('retrieve', HTTPStatus.OK),
        ('destroy', HTTPStatus.NO_CONTENT),
        ('update', HTTPStatus.OK),
        ('partial_update', HTTPStatus.OK),
    )


class FinanicalAdviserToFinanicalAdviser(FinancialAdviserToModel,
                                         UserToFinancialAdviser,
                                         PermissionsTests,
                                         AuthenticatedTests,
                                         NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.OK),
        ('retrieve', HTTPStatus.OK),
        ('create', HTTPStatus.CREATED),
        ('destroy', HTTPStatus.NO_CONTENT),
        ('update', HTTPStatus.OK),
        ('partial_update', HTTPStatus.OK),
    )


class FinancialAdviserToRelatedClient(FinancialAdviserToModel, UserToClient,
                                      PermissionsTests,
                                      AuthenticatedTests,
                                      NotAuthenticatedTests):

    related_name = 'clients'
    expected_status_codes = (
        ('list', HTTPStatus.OK),
        ('retrieve', HTTPStatus.OK),
        ('destroy', HTTPStatus.NO_CONTENT),
        ('update', HTTPStatus.OK),
        ('partial_update', HTTPStatus.OK),
    )


class FinancialAdviserToClient(FinancialAdviserToModel, UserToClient,
                               PermissionsTests, AuthenticatedTests,
                               NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.OK),
        ('retrieve', HTTPStatus.OK),
        ('create', HTTPStatus.CREATED),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class FinancialAdviserToEmployee(FinancialAdviserToModel, UserToEmployee,
                                 PermissionsTests, NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.OK),
        ('retrieve', HTTPStatus.OK),
        ('create', HTTPStatus.CREATED),
        ('destroy', HTTPStatus.NO_CONTENT),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )


class FinancialAdviserToRelatedGeneral(FinancialAdviserToModel, UserToGeneral,
                                       PermissionsTests,
                                       NotAuthenticatedTests):

    related_names = ('clients', 'financial_planning')
    expected_status_codes = (
        ('list', HTTPStatus.OK),
        ('retrieve', HTTPStatus.OK),
        ('destroy', HTTPStatus.NO_CONTENT),
        ('update', HTTPStatus.OK),
        ('partial_update', HTTPStatus.OK),
    )


class FinancialAdviserToGeneral(FinancialAdviserToModel, UserToGeneral,
                                PermissionsTests, AuthenticatedTests,
                                NotAuthenticatedTests):

    expected_status_codes = (
        ('list', HTTPStatus.OK),
        ('retrieve', HTTPStatus.OK),
        ('create', HTTPStatus.CREATED),
        ('destroy', HTTPStatus.FORBIDDEN),
        ('update', HTTPStatus.FORBIDDEN),
        ('partial_update', HTTPStatus.FORBIDDEN),
    )
