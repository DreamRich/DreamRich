CLIENT_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_related_clients', 'change_related_clients',
    'see_related_general'
]

EMPLOYEE_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_all_clients', 'add_clients', 'list_clients',
    'see_related_employees', 'change_related_employees'
]

# fa = financial adviser
FINANCIAL_ADVISER_DEFAULT_CODENAMES_PERMISSIONS = [
    'see_all_clients', 'delete_related_clients', 'change_related_clients',
    'list_clients',

    'see_all_employees', 'add_employees', 'delete_all_employees',
    'list_employees',

    'see_all_fa', 'add_employees', 'delete_all_fa', 'change_all_fa',
    'see_fa_list',

    'see_all_general', 'list_general', 'add_generals',
    'delete_related_general', 'change_related_general',
]

CLIENT_MODEL_PERMISSIONS = (
    ('see_all_clients', 'See all clients from database'),
    ('see_related_clients', 'See related clients (or itself, if clients)'),
    ('see_clients_from_others', 'See clients which others related'),
    ('list_clients', 'See list of clients itself'),

    ('add_clients', 'Create a clients'),

    ('change_all_clients', 'Change all clients from database'),
    ('change_related_clients', 'Change related clients (itself, if client)'),
    ('change_clients_from_others', 'See clients which others related'),

    ('delete_all_clients', 'Delete all clients from database'),
    ('delete_related_clients', 'Delete related clients (itself, if clients)'),
    ('delete_clients_from_others', 'Delete clients which others related'),
)

EMPLOYEE_MODEL_PERMISSIONS = (
    ('see_all_employees', 'See all employees from database'),
    ('see_related_employees', 'See related employeess (itself, if employees)'),
    ('see_employees_from_others', 'See employeess which others related'),
    ('list_employees', 'See list of employeess itself'),

    ('add_employees', 'Create an employees'),

    ('change_all_employees', 'Change all employees from database'),
    ('change_related_employees', 'Change related employeess (or itself)'),
    ('change_employees_from_others', 'See employeess which others related'),

    ('delete_all_employees', 'Change all employees from database'),
    ('delete_employees_from_others', 'Delete employeess which others related'),
)

FINANCIAL_ADVISER_MODEL_PERMISSIONS = (
    ('see_all_fa', 'See all fa, relateds and others'),
    ('see_related_fa', 'See related fa (or itself, if fa)'),
    ('see_fa_from_others', 'See fa which others related'),
    ('see_fa_list', 'See list of fa itself'),

    ('add_fa', 'Create an fa'),

    ('change_all_fa', 'Change all fa from database'),
    ('change_related_fa', 'Change related fa (itself, if fa)'),
    ('change_fa_from_others', 'See fa which others related'),

    ('delete_all_fa', 'Change all fa from database'),
    ('delete_related_fa', 'Delete related fa (itself, if fa))'),
    ('delete_fa_from_others', 'Delete fa which others related'),
)

GENERAL_MODEL_PERMISSIONS = (
    ('see_all_general', 'See all general from database'),
    ('see_related_general', 'See related generals)'),
    ('see_general_from_others', 'See others generals)'),
    ('list_general', 'See list of generals itself'),

    ('add_generals', 'Create a general'),

    ('change_all_general', 'Change all general from database'),
    ('change_related_general', 'Change related generals (itself, if general)'),
    ('change_general_from_others', 'See general which others related'),

    ('delete_all_general', 'Delete all general from database'),
    ('delete_related_general', 'Delete related generals)'),
    ('delete_general_from_others', 'Delete generals which others related'),
)
