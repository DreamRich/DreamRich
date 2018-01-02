from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from dreamrich.models import BaseModel


class BaseUser(User, BaseModel):

    # Children can set this attribute for setting user permissions
    default_permissions_codenames = []

    # To facilitate getting default permissions in others places, permissions,
    # not codenames
    @property
    def default_permissions(self):
        try:
            permissions = []
            for permission_codename in self.default_permissions_codenames:
                permissions += \
                    [Permission.objects.get(codename=permission_codename)]
        except Permission.DoesNotExist:
            raise Permission.DoesNotExist("Couldn't find permission"
                                          " with codename {}"
                                          .format(permission_codename))
        except Permission.MultipleObjectsReturned:
            raise Permission.MultipleObjectsReturned(
                "Found multiple permissions with same code_name."
                " Permissions gotten until moment for this object: {}"
                .format(', '.join(
                    [permission.codename for permission in permissions]
                ))
            )

        return permissions

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if not self.pk:  # not registered
            self.username = self.cpf  # user can't change password

            self.password = 'default123' if not self.password else \
                self.password  # must generate random, not ok yet
            self.set_password(self.password)

        super(BaseUser, self).save(*args, **kwargs)

        # pylint: disable=no-member
        self.user_permissions.set(self.default_permissions)
