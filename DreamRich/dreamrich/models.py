from django.db import models

class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()

        super(BaseModel, self).save(force_insert, force_update, using,
                                    update_fields)
