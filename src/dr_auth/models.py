from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from dreamrich.models import BaseModel


class BaseUser(User, BaseModel):

    # Children can set this attribute for setting user permissions
    default_permissions_codenames = []

    @property
    def permissions(self):
        return self.get_all_permissions()

    # To facilitate getting default permissions in others places, permissions,
    # not codenames
    @property
    def default_permissions(self):
        permissions = []

        try:
            for permission_codename in self.default_permissions_codenames:
                permissions += \
                    [Permission.objects.get(codename=permission_codename)]
        except Permission.DoesNotExist:
            raise Permission.DoesNotExist("Couldn't find permission"
                                          " with codename {}"
                                          .format(permission_codename))
        except Permission.MultipleObjectsReturned:
            permissions_codenames = \
                ', '.join([permission.codename for permission in permissions])
            raise Permission.MultipleObjectsReturned(
                "Found multiple permissions with same code_name."
                " Permissions gotten until moment for this object: {}"
                .format(permissions_codenames)
            )

        return permissions

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.pk is None:  # not registered
            self.username = self.cpf

            self.password = 'default123' if not self.password else \
                self.password  # must generate random, not ok yet
            self.set_password(self.password)

        super(BaseUser, self).save(*args, **kwargs)

        self.user_permissions.set(self.default_permissions)
