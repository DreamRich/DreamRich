from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        self.full_clean()

        super(BaseModel, self).save(*args, **kwargs)
