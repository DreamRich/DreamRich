CLIENT_PERMISSION_NAME = 'clients'
EMPLOYEE_PERMISSION_NAME = 'employees'
FINANCIAL_ADVISER_PERMISSION_NAME = 'fa'
GENERAL_PERMISSION_NAME = 'general'

CLIENT_DEFAULT_CODENAMES_PERMISSIONS = [
    'retrieve_related_clients',
    'update_related_clients',

    'retrieve_related_general'
]

EMPLOYEE_DEFAULT_CODENAMES_PERMISSIONS = [
    'create_clients',
    'list_all_clients',
    'retrieve_all_clients',

    'retrieve_related_employees',
    'update_related_employees',
]

# fa = financial adviser
FINANCIAL_ADVISER_DEFAULT_CODENAMES_PERMISSIONS = [
    'create_clients',
    'destroy_related_clients',
    'list_all_clients',
    'retrieve_all_clients',
    'update_related_clients',

    'create_employees',
    'destroy_all_employees',
    'list_all_employees',
    'retrieve_all_employees',

    'create_fa',
    'destroy_all_fa',
    'list_all_fa',
    'retrieve_all_fa',
    'update_all_fa',

    'create_general',
    'destroy_related_general',
    'list_all_general',
    'retrieve_all_general',
    'update_related_general',
]


def get_formatted_permissions(checked_name):
    ownership_types = ('all', 'related', 'not_related')

    # Format codenames with actions
    codenames = dict()
    for ownership in ownership_types:
        codenames[ownership] = '{}_{}_{}'.format('{}', ownership, '{}')

    # Define descriptions
    descriptions = dict()
    descriptions['all'] = \
        'To {} all {} from database'
    descriptions['related'] = \
        'To {} {} which has relationship with itself (or is itself)'
    descriptions['not_related'] = \
        "To {} only {} that don't have relationship with itself"

    # Maps actions to friendly names
    actions_with_ownership = dict(
        retrieve='Get',
        update='Update',
        destroy='Delete',
        list='List'
    )

    unformatted_template = [(codenames[ownership], descriptions[ownership])
                            for ownership in ownership_types]

    # Format codenames and descriptions with action and checked_name
    permissions = []
    for action, name_friendly in actions_with_ownership.items():
        for codename, description in unformatted_template:
            permissions += [
                (codename.format(action, checked_name),
                 description.format(name_friendly, checked_name))
            ]

    # Add specific cases
    permissions += [
        ('create_{}'.format(checked_name), 'To create {}'.format(checked_name))
    ]

    return tuple(permissions)
