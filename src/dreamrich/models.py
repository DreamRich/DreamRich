from django.db import models
from dr_auth.models_permissions import GENERAL_MODEL_PERMISSIONS


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        self.full_clean()
        super(BaseModel, self).save(*args, **kwargs)


# Abstract model for classes which have "general" level of permissions
# Children classes won't get any permissions from here, inheriterance is just
# to satisfy modeling aspects
class GeneralModel(BaseModel):
    class Meta:
        # Can't set abstract here because permissions wouldn't get generated
        permissions = GENERAL_MODEL_PERMISSIONS

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if str(self.__class__()) == 'GeneralModel object':
            raise Exception("Can't save object of class GeneralModel"
                            " it's an abstract model.")

        super(GeneralModel, self).save(*args, **kwargs)
