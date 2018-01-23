from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import related_descriptors


class Relationship:

    def __init__(self, primary, secondary=None, related_name=None):
        self.primary, self.secondary = primary, secondary
        self.related_name = related_name

        self._check_objects_are_saved()

    def make(self, related_name=None):
        self._fill_attributes(related_name=related_name)
        self._check_all_attributes_filled()
        self._check_relatedname()

        is_ok = True
        if self.is_many():
            related_manager = getattr(self.primary, self.related_name)
            try:
                related_manager.add(self.secondary)
            except TypeError:
                is_ok = False
        else:
            try:
                setattr(self.primary, self.related_name, self.secondary)
            except ValueError:
                is_ok = False

        if not is_ok:
            raise TypeError("Can't create relationship between these classes."
                            " Probably they don't have a relationship or"
                            " tried the wrong related_name.")

    def is_many(self):
        self._check_relatedname()

        try:
            related_attr = getattr(self.primary, self.related_name)

            if related_attr.__module__ == related_descriptors.__name__:
                return True
        except ObjectDoesNotExist:
            pass

        return False

    def has_relationship(self):
        self._check_relatedname()
        self._check_all_attributes_filled()

        has_relationship_bool = False
        if hasattr(self.primary, self.related_name):
            if self.is_many():
                related_manager = getattr(self.primary, self.related_name)
                has_relationship_bool = self.secondary in related_manager.all()
            else:
                related_attribute = getattr(self.primary, self.related_name)
                has_relationship_bool = related_attribute == self.secondary

        return has_relationship_bool

    def get_related(self):
        '''
        Returns last related if many else returns related.
        '''
        self._check_relatedname()

        related = None
        if hasattr(self.primary, self.related_name):
            if self.is_many():
                related_manager = getattr(self.primary, self.related_name)
                related = related_manager.last()
            else:
                related = getattr(self.primary, self.related_name)

        return related

    def _check_relatedname(self):
        swapped = False
        is_valid = True

        while True:
            try:
                getattr(self.primary, str(self.related_name))
                break
            except ObjectDoesNotExist:
                break
            except AttributeError:
                self.primary, self.secondary = self.secondary, self.primary

                if swapped:
                    is_valid = False
                    break
                swapped = True

        if not is_valid:
            raise AttributeError("'related_name' passed is not valid for any"
                                 " of related objects.")

    def _check_objects_are_saved(self):
        if (self.primary.id is None or
                (self.secondary and self.secondary.id is None)):
            raise AttributeError('Objects passed to this class must be on'
                                 ' database.')

    def _check_all_attributes_filled(self):
        missing = ''

        if not self.secondary:
            missing = 'secondary'
        elif not self.related_name:
            missing = 'related_name'

        if missing:
            raise AttributeError("Not enough information, '{}' is missing."
                                 .format(missing))

    def _fill_attributes(self, primary=None, secondary=None,
                         related_name=None):

        self.primary = primary or self.primary
        self.secondary = secondary or self.secondary
        self.related_name = related_name or self.related_name

    def __str__(self):
        primary_name = self.primary.__class__.__name__

        if self.secondary:
            secondary_name = self.secondary.__class__.__name__
        else:
            secondary_name = ''

        return '({} : {})'.format(primary_name,
                                  secondary_name if secondary_name else "")
