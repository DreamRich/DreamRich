from django.db import models
from django.core.exceptions import ValidationError
from dr_auth.models_permissions import GENERAL_MODEL_PERMISSIONS


class BaseModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        try:
            self.full_clean()
        except ValidationError:
            raise ValidationError('Error while saving model "{}"'
                                  .format(self.__class__.__name__))

        super(BaseModel, self).save(*args, **kwargs)


# Abstract model for classes which have "general" level of permissions
# Children classes won't get any permissions from here, inheriterance is just
# to satisfy modeling aspects
class GeneralModel(BaseModel):
    class Meta:
        # Can't set abstract here because permissions wouldn't get generated
        permissions = GENERAL_MODEL_PERMISSIONS

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        this_class_name = 'GeneralModel'

        # Prevent this class from being instantiated
        if self.__class__.__name__ == this_class_name:
            raise Exception("Can't save object of class GeneralModel"
                            " it's an abstract model.")

        super(GeneralModel, self).save(*args, **kwargs)
