from django.contrib.auth.models import User
from rolepermissions.permissions import available_perm_status


class BaseUser(User):

    @property
    def permissions(self):
        return available_perm_status(self)

    def save(self, *args, **kwargs):
        if not self.pk:
            # TODO: Generate random password
            self.set_password(self.password)
        self.username = self.cpf
        self.full_clean()

        super(BaseUser, self).save(*args, **kwargs)
