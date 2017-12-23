from django.contrib.auth.models import User


class BaseUser(User):

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if not self.pk:  # not registered
            self.username = self.cpf  # user can't change password

            self.password = 'default123' if not self.password else \
                self.password  # must generate random, not ok yet
            self.set_password(self.password)

        self.full_clean()
        super(BaseUser, self).save(*args, **kwargs)

        # pylint: disable=no-member
        self.user_permissions.set(self.default_permissions)
