from django.contrib.auth.models import User


class BaseUser(User):

    @property
    def permissions(self):
        permissions = self.get_permissions()
        permissions = sorted(permissions.items())

        permissions = [permission[0] for permission in permissions
                       if permission[1]]  # permission is like ('p1', True))
        permissions = ', '.join(permissions)

        return permissions

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if not self.pk:  # not registered
            self.username = self.cpf  # user can't change password

            self.password = 'default123' if not self.password else \
                self.password  # must generate random, not ok yet
            self.set_password(self.password)

        self.full_clean()
        super(BaseUser, self).save(*args, **kwargs)
