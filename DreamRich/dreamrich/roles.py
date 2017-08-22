from rolepermissions.roles import AbstractUserRole

class ComumEmployee(AbstractUserRole):
    available_permissions = {
        'see_all_basic_client_data': True,
    }

class FinancialAdviser(AbstractUserRole):
    available_permissions = {
        'see_all_basic_client_data': True,
        'change_own_client_data': True,
        'see_own_client_data': True,
    }

class Client(AbstractUserRole):
    available_permissions = {
        'see_own_client_data': True,
    }
