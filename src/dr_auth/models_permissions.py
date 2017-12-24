from rest_framework.permissions import DjangoModelPermissions

CLIENT_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_client', 'see_own_client',
    'change_client', 'change_own_client',

    'see_general', 'see_own_general'
]

EMPLOYEE_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_client', 'delete_client',
    'see_other_client', 'add_client',

    'see_employee', 'change_employee',
    'see_own_employee', 'change_own_employee'
]

# fa = financial adviser
FINANCIAL_ADVISER_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_client', 'delete_client', 'change_client',
    'see_own_client', 'delete_own_client', 'change_own_client',
    'see_other_client', 'add_client',

    'see_employee', 'delete_employee', 'change_employee',
    'see_other_employee', 'delete_other_employee', 'add_employee',

    'see_fa', 'delete_fa', 'change_fa',
    'see_own_fa', 'delete_own_fa', 'change_own_fa',
    'see_other_fa', 'delete_other_fa', 'add_fa',

    'see_general', 'delete_general', 'change_general', 'add_general',
    'see_own_general', 'delete_own_general', 'change_own_general',
    'see_other_general'
]

CLIENT_MODEL_PERMISSIONS = (
    ('see_client', 'Obrigatory for user can see any client'),
    ('see_own_client', 'See own clients (or itself, if client)'),
    ('see_other_client', 'See other clients (or not yours)'),
    ('see_client_list', 'See list of clients itself'),

    ('add_client', 'Create a client'),

    ('change_client', 'Obrigatory for user can change any client'),
    ('change_own_client', 'Change own clients (or itself)'),
    ('change_other_client', 'See other clients (or not yours)'),

    ('delete_client', 'Obrigatory for user can delete any client'),
    ('delete_own_client', 'Delete own clients (or itself, if client)'),
    ('delete_other_client', 'Delete other clients (or not yours)'),
)

EMPLOYEE_MODEL_PERMISSIONS = (
    ('see_employee', 'Obrigatory for user can see any employee'),
    ('see_own_employee', 'See own employees (or itself, if employee)'),
    ('see_other_employee', 'See other employees (or not yours)'),
    ('see_employee_list', 'See list of employees itself'),

    ('add_employee', 'Create an employee'),

    ('change_employee', 'Obrigatory for user can change any employee'),
    ('change_own_employee', 'Change own employees (or itself)'),
    ('change_other_employee', 'See other employees (or not yours)'),

    ('delete_employee', 'Obrigatory for user can change any employee'),
    ('delete_other_employee', 'Delete other employees (or not yours)'),
)

FINANCIAL_ADVISER_MODEL_PERMISSIONS = (
    ('see_fa', 'Obrigatory for user can see any fa'),
    ('see_own_fa', 'See own fas (or itself, if fa)'),
    ('see_other_fa', 'See other fa (or not yours)'),
    ('see_fa_list', 'See list of fa itself'),

    ('add_fa', 'Create an fa'),

    ('change_fa', 'Obrigatory for user can change any fa'),
    ('change_own_fa', 'Change own fa (or itself)'),
    ('change_other_fa', 'See other fa (or not yours)'),

    ('delete_fa', 'Obrigatory for user can change any fa'),
    ('delete_other_fa', 'Delete other fa (or not yours)'),
)


class ClientsModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['client.see_client'],
        'POST': ['client.add_client'],
        'PUT': ['client.change_client'],
        'PATCH': ['client.change_client'],
        'DELETE': ['client.delete_client'],
    }


class EmployeesModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['employee.see_employee'],
        'POST': ['employee.add_employee'],
        'PUT': ['employee.change_employee'],
        'PATCH': ['employee.change_employee'],
        'DELETE': ['employee.delete_employee'],
    }


class FinancialAdvisersModelPermissions(DjangoModelPermissions):
    # fa = financial adviser
    perms_map = {
        'GET': ['fa.see_fa'],
        'POST': ['fa.add_fa'],
        'PUT': ['fa.change_fa'],
        'PATCH': ['fa.change_fa'],
        'DELETE': ['fa.delete_fa'],
    }


class GeneralModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['general.see_general'],
        'POST': ['general.add_general'],
        'PUT': ['general.change_general'],
        'PATCH': ['general.change_general'],
        'DELETE': ['general.delete_general'],
    }
