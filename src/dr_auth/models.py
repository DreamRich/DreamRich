from django.contrib.auth.models import User
from rolepermissions.permissions import available_perm_status


class BaseUser(User):

    def get_permissions(self):
        return available_perm_status(self)

    @property
    def permissions(self):
        permissions = self.get_permissions()
        permissions = sorted(permissions.items())

        permissions = [permission[0] for permission in permissions
                       if permission[1]]  # permission is like ('p1', True))
        permissions = ', '.join(permissions)

        return permissions

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if not self.pk:
            if not self.password:
                self.password = 'default123'
            self.set_password(self.password)

        self.username = self.cpf
        self.full_clean()

        super(BaseUser, self).save(*args, **kwargs)
