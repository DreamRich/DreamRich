from rest_framework.permissions import DjangoModelPermissions

CLIENT_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_any_client', 'see_own_client',
    'change_any_client', 'change_own_client',

    'see_any_general', 'see_own_general'
]

EMPLOYEE_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_any_client', 'delete_any_client',
    'see_other_client', 'add_any_client',

    'see_any_employee', 'change_any_employee',
    'see_own_employee', 'change_own_employee'
]

# fa = financial adviser
FINANCIAL_ADVISER_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_any_client', 'delete_any_client', 'change_any_client',
    'see_own_client', 'delete_own_client', 'change_own_client',
    'see_other_client', 'add_any_client',

    'see_any_employee', 'delete_any_employee', 'change_any_employee',
    'see_other_employee', 'delete_other_employee', 'add_any_employee',

    'see_any_fa', 'delete_any_fa', 'change_any_fa',
    'see_own_fa', 'delete_own_fa', 'change_own_fa',
    'see_other_fa', 'delete_other_fa', 'add_any_fa',

    'see_any_general', 'delete_any_general', 'change_any_general',
    'see_own_general', 'delete_own_general', 'change_own_general',
    'see_other_general',
    'add_any_general'
]

CLIENT_MODEL_PERMISSIONS = (
    ('see_any_client', 'Obrigatory for user can see any client'),
    ('see_own_client', 'See own clients (or itself, if client)'),
    ('see_other_client', 'See other clients (or not yours)'),
    ('see_any_client_list', 'See list of clients itself'),

    ('add_any_client', 'Create a client'),

    ('change_any_client', 'Obrigatory for user can change any client'),
    ('change_own_client', 'Change own clients (or itself)'),
    ('change_other_client', 'See other clients (or not yours)'),

    ('delete_any_client', 'Obrigatory for user can delete any client'),
    ('delete_own_client', 'Delete own clients (or itself, if client)'),
    ('delete_other_client', 'Delete other clients (or not yours)'),
)

EMPLOYEE_MODEL_PERMISSIONS = (
    ('see_any_employee', 'Obrigatory for user can see any employee'),
    ('see_own_employee', 'See own employees (or itself, if employee)'),
    ('see_other_employee', 'See other employees (or not yours)'),
    ('see_any_employee_list', 'See list of employees itself'),

    ('add_any_employee', 'Create an employee'),

    ('change_any_employee', 'Obrigatory for user can change any employee'),
    ('change_own_employee', 'Change own employees (or itself)'),
    ('change_other_employee', 'See other employees (or not yours)'),

    ('delete_any_employee', 'Obrigatory for user can change any employee'),
    ('delete_other_employee', 'Delete other employees (or not yours)'),
)

FINANCIAL_ADVISER_MODEL_PERMISSIONS = (
    ('see_any_fa', 'Obrigatory for user can see any fa'),
    ('see_own_fa', 'See own fas (or itself, if fa)'),
    ('see_other_fa', 'See other fa (or not yours)'),
    ('see_any_fa_list', 'See list of fa itself'),

    ('add_any_fa', 'Create an fa'),

    ('change_any_fa', 'Obrigatory for user can change any fa'),
    ('change_own_fa', 'Change own fa (or itself)'),
    ('change_other_fa', 'See other fa (or not yours)'),

    ('delete_any_fa', 'Obrigatory for user can change any fa'),
    ('delete_own_fa', 'Delete own fa (or itself, if fa))'),
    ('delete_other_fa', 'Delete other fa (or not yours)'),
)

GENERAL_MODEL_PERMISSIONS = (
    ('see_any_general', 'Obrigatory for user can see any general'),
    ('see_own_general', 'See own generals)'),
    ('see_other_general', 'See other generals)'),
    ('see_any_general_list', 'See list of generals itself'),

    ('add_any_general', 'Create a general'),

    ('change_any_general', 'Obrigatory for user can change any general'),
    ('change_own_general', 'Change own generals (or itself)'),
    ('change_other_general', 'See other generals (or not yours)'),

    ('delete_any_general', 'Obrigatory for user can delete any general'),
    ('delete_own_general', 'Delete own generals)'),
    ('delete_other_general', 'Delete other generals (or not yours)'),
)


class ClientsModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['client.see_any_client'],
        'POST': ['client.add_any_client'],
        'PUT': ['client.change_any_client'],
        'PATCH': ['client.change_any_client'],
        'DELETE': ['client.delete_any_client'],
    }


class EmployeesModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['employee.see_any_employee'],
        'POST': ['employee.add_any_employee'],
        'PUT': ['employee.change_any_employee'],
        'PATCH': ['employee.change_any_employee'],
        'DELETE': ['employee.delete_any_employee'],
    }


class FinancialAdvisersModelPermissions(DjangoModelPermissions):
    # fa = financial adviser
    perms_map = {
        'GET': ['fa.see_any_fa'],
        'POST': ['fa.add_any_fa'],
        'PUT': ['fa.change_any_fa'],
        'PATCH': ['fa.change_any_fa'],
        'DELETE': ['fa.delete_any_fa'],
    }


class GeneralModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['general.see_any_general'],
        'POST': ['general.add_any_general'],
        'PUT': ['general.change_any_general'],
        'PATCH': ['general.change_any_general'],
        'DELETE': ['general.delete_any_general'],
    }
