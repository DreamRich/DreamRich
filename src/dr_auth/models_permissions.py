from collections import namedtuple

PermissionInfo = namedtuple('PermissionInfo', 'nick default_codenames')

UsersPermissionsInfo = namedtuple('UsersPermissionsInfo',
                                  'client employee financial_adviser')

# Nicks are the ones used on permissions codenames
USERS_PERMISSIONS_INFO = UsersPermissionsInfo(
    client=PermissionInfo(
        nick='clients',
        default_codenames=(
            'retrieve_related_clients',
            'update_related_clients', 'partial_update_related_clients',

            'retrieve_related_general'
        )
    ),
    employee=PermissionInfo(
        nick='employees',
        default_codenames=(
            'create_clients',
            'list_all_clients',
            'retrieve_all_clients',

            'retrieve_related_employees',
            'update_related_employees', 'partial_update_related_employees',
        )
    ),
    financial_adviser=PermissionInfo(
        nick='fa',
        default_codenames=(
            'create_clients',
            'destroy_related_clients',
            'list_all_clients',
            'retrieve_all_clients',
            'update_related_clients', 'partial_update_related_clients',

            'create_employees',
            'destroy_all_employees',
            'list_all_employees',
            'retrieve_all_employees',

            'create_fa',
            'destroy_all_fa',
            'list_all_fa',
            'retrieve_all_fa',
            'update_all_fa', 'partial_update_all_fa',

            'create_general',
            'destroy_related_general',
            'list_all_general',
            'retrieve_all_general',
            'update_related_general', 'partial_update_related_general',
        )
    )
)


def get_formatted_permissions(checked_name):
    ownership_types = ('all', 'related', 'not_related')

    # Format codenames with actions
    codenames = {ownership: '{}_{}_{}'.format('{}', ownership, '{}')
                 for ownership in ownership_types}

    # Define descriptions
    descriptions = dict()
    descriptions['all'] = \
        'To {} all {} from database'
    descriptions['related'] = \
        'To {} {} which have relationship with, or is, itself'
    descriptions['not_related'] = \
        "To {} only {} that don't have relationship with itself"

    # Maps actions to friendly names
    actions_with_ownership = dict(
        retrieve='get',
        update='change',
        partial_update='partially change',
        destroy='delete',
        list='list'
    )

    # Assembling permissions tuples
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

    # Add case with no ownership
    permissions += [
        ('create_{}'.format(checked_name), 'To create {}'.format(checked_name))
    ]

    return tuple(permissions)
