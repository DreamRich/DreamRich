from django.contrib.auth.models import User
from rolepermissions.permissions import available_perm_status
from functools import reduce


class BaseUser(User):

    def get_permissions(self):
        return available_perm_status(self)

    @property
    def permissions(self):
        permissions = self.get_permissions()

        def reducer(current, item):
            if not item[1]:
                return current
            elif current == '':
                return item[0]
            else:
                return '{}, {}'.format(current, *item)

        items = sorted(permissions.items())
        return reduce(reducer, items, '')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            # TODO: Generate random password
            if not self.password:
                self.password = 'default123'
            self.set_password(self.password)
        self.username = self.cpf
        self.full_clean()

        super(BaseUser, self).save(force_insert, force_update, using,
                                   update_fields)
