CLIENT_DEFAULT_CODENAMES_PERMISSIONS = [
    'retrieve_related_clients', 'update_related_clients',
    'retrieve_related_general'
]

EMPLOYEE_DEFAULT_CODENAMES_PERMISSIONS = [
    'retrieve_all_clients', 'add_clients', 'list_clients',
    'retrieve_related_employees', 'update_related_employees'
]

# fa = financial adviser
FINANCIAL_ADVISER_DEFAULT_CODENAMES_PERMISSIONS = [
    'retrieve_all_clients', 'destroy_related_clients', 'update_related_clients',
    'list_clients',

    'retrieve_all_employees', 'add_employees', 'destroy_all_employees',
    'list_employees',

    'retrieve_all_fa', 'add_employees', 'destroy_all_fa', 'update_all_fa',
    'retrieve_fa_list',

    'retrieve_all_general', 'list_general', 'add_generals',
    'destroy_related_general', 'update_related_general',
]

CLIENT_MODEL_PERMISSIONS = (
    ('retrieve_all_clients', 'retrieve all clients from database'),
    ('retrieve_related_clients', 'retrieve related clients (or itself, if clients)'),
    ('retrieve_clients_from_others', 'retrieve clients which others related'),
    ('list_clients', 'retrieve list of clients itself'),

    ('add_clients', 'Create a clients'),

    ('update_all_clients', 'update all clients from database'),
    ('update_related_clients', 'update related clients (itself, if client)'),
    ('update_clients_from_others', 'retrieve clients which others related'),

    ('destroy_all_clients', 'destroy all clients from database'),
    ('destroy_related_clients', 'destroy related clients (itself, if clients)'),
    ('destroy_clients_from_others', 'destroy clients which others related'),
)

EMPLOYEE_MODEL_PERMISSIONS = (
    ('retrieve_all_employees', 'retrieve all employees from database'),
    ('retrieve_related_employees', 'retrieve related employeess (itself, if employees)'),
    ('retrieve_employees_from_others', 'retrieve employeess which others related'),
    ('list_employees', 'retrieve list of employeess itself'),

    ('add_employees', 'Create an employees'),

    ('update_all_employees', 'update all employees from database'),
    ('update_related_employees', 'update related employeess (or itself)'),
    ('update_employees_from_others', 'retrieve employeess which others related'),

    ('destroy_all_employees', 'update all employees from database'),
    ('destroy_employees_from_others', 'destroy employeess which others related'),
)

FINANCIAL_ADVISER_MODEL_PERMISSIONS = (
    ('retrieve_all_fa', 'retrieve all fa, relateds and others'),
    ('retrieve_related_fa', 'retrieve related fa (or itself, if fa)'),
    ('retrieve_fa_from_others', 'retrieve fa which others related'),
    ('retrieve_fa_list', 'retrieve list of fa itself'),

    ('add_fa', 'Create an fa'),

    ('update_all_fa', 'update all fa from database'),
    ('update_related_fa', 'update related fa (itself, if fa)'),
    ('update_fa_from_others', 'retrieve fa which others related'),

    ('destroy_all_fa', 'update all fa from database'),
    ('destroy_related_fa', 'destroy related fa (itself, if fa))'),
    ('destroy_fa_from_others', 'destroy fa which others related'),
)

GENERAL_MODEL_PERMISSIONS = (
    ('retrieve_all_general', 'retrieve all general from database'),
    ('retrieve_related_general', 'retrieve related generals)'),
    ('retrieve_general_from_others', 'retrieve others generals)'),
    ('list_general', 'retrieve list of generals itself'),

    ('add_generals', 'Create a general'),

    ('update_all_general', 'update all general from database'),
    ('update_related_general', 'update related generals (itself, if general)'),
    ('update_general_from_others', 'retrieve general which others related'),

    ('destroy_all_general', 'destroy all general from database'),
    ('destroy_related_general', 'destroy related generals)'),
    ('destroy_general_from_others', 'destroy generals which others related'),
)
