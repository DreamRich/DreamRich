from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from dreamrich.models import BaseModel


class BaseUser(User, BaseModel):

    class Meta:
        abstract = True

    # Children can set this attribute for setting user permissions
    default_permissions_codenames = []

    @property
    def permissions(self):
        return self.get_all_permissions()

    # To facilitate getting default permissions in others places, permissions,
    # not codenames
    @property
    def default_permissions(self):
        permissions = Permission.objects.filter(
            codename__in=self.default_permissions_codenames
        )

        return permissions

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.pk is None:  # not registered
            self.username = self.cpf

            # must generate random, not ok yet
            self.password = ('default123' if not self.password
                             else self.password)
            self.set_password(self.password)

        super(BaseUser, self).save(*args, **kwargs)

        self.user_permissions.set(self.default_permissions)
