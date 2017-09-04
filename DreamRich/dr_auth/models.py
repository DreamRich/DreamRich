from django.contrib.auth.models import User
from rolepermissions.permissions import available_perm_status


class BaseUser(User):

    @property
    def permissions(self):
        return available_perm_status(self)
