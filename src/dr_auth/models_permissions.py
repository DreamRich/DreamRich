CLIENT_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_own_clients', 'change_own_clients',
    'see_own_general'
]

EMPLOYEE_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_all_clients', 'add_clients', 'list_clients',
    'see_own_employees', 'change_own_employees'
]

# fa = financial adviser
FINANCIAL_ADVISER_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_all_clients', 'delete_own_clients', 'change_own_clients',
    'list_clients',

    'see_all_employees', 'add_employees', 'delete_all_employees',
    'list_employees',

    'see_all_fa', 'add_employees', 'delete_all_fa', 'change_all_fa',
    'see_fa_list',

    'see_all_general', 'list_general', 'add_generals',
    'delete_own_general', 'change_own_general',
]

CLIENT_MODEL_PERMISSIONS = (
    ('see_all_clients', 'See all clients from database'),
    ('see_own_clients', 'See own clients (or itself, if clients)'),
    ('see_clients_from_others', 'See clients which others own'),
    ('list_clients', 'See list of clients itself'),

    ('add_clients', 'Create a clients'),

    ('change_all_clients', 'Change all clients from database'),
    ('change_own_clients', 'Change own clients (or itself, if client)'),
    ('change_clients_from_others', 'See clients which others own'),

    ('delete_all_clients', 'Delete all clients from database'),
    ('delete_own_clients', 'Delete own clients (or itself, if clients)'),
    ('delete_clients_from_others', 'Delete clients which others own'),
)

EMPLOYEE_MODEL_PERMISSIONS = (
    ('see_all_employees', 'See all employees from database'),
    ('see_own_employees', 'See own employeess (or itself, if employees)'),
    ('see_employees_from_others', 'See employeess which others own'),
    ('list_employees', 'See list of employeess itself'),

    ('add_employees', 'Create an employees'),

    ('change_all_employees', 'Change all employees from database'),
    ('change_own_employees', 'Change own employeess (or itself)'),
    ('change_employees_from_others', 'See employeess which others own'),

    ('delete_all_employees', 'Change all employees from database'),
    ('delete_employees_from_others', 'Delete employeess which others own'),
)

FINANCIAL_ADVISER_MODEL_PERMISSIONS = (
    ('see_all_fa', 'See all fa, owns and others'),
    ('see_own_fa', 'See own fa (or itself, if fa)'),
    ('see_fa_from_others', 'See fa which others own'),
    ('see_fa_list', 'See list of fa itself'),

    ('add_fa', 'Create an fa'),

    ('change_all_fa', 'Change all fa from database'),
    ('change_own_fa', 'Change own fa (or itself)'),
    ('change_fa_from_others', 'See fa which others own'),

    ('delete_all_fa', 'Change all fa from database'),
    ('delete_own_fa', 'Delete own fa (or itself, if fa))'),
    ('delete_fa_from_others', 'Delete fa which others own'),
)

GENERAL_MODEL_PERMISSIONS = (
    ('see_all_general', 'See all general from database'),
    ('see_own_general', 'See own generals)'),
    ('see_general_from_others', 'See others generals)'),
    ('list_general', 'See list of generals itself'),

    ('add_generals', 'Create a general'),

    ('change_all_general', 'Change all general from database'),
    ('change_own_general', 'Change own generals (or itself)'),
    ('change_general_from_others', 'See general which others own'),

    ('delete_all_general', 'Delete all general from database'),
    ('delete_own_general', 'Delete own generals)'),
    ('delete_general_from_others', 'Delete generals which others own'),
)
