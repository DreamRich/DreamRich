from django.db import models
from django.contrib.auth.models import Permission


class BaseModel(models.Model):
    class Meta:
        abstract = True

    # To facilitate getting default permissions in others places
    @property
    def default_permissions(self):
        permissions = []
        for permission_codename in self.default_permissions_codenames:
            permissions += \
                [Permission.objects.get(codename=permission_codename)]

        return permissions

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        self.full_clean()

        super(BaseModel, self).save(*args, **kwargs)
