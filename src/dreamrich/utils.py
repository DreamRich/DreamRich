from collections import namedtuple
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import related_descriptors


class Relationship:

    RelatedMeta = namedtuple('RelatedMeta', 'related_name pk')

    def __init__(self, primary, secondary=None, *,
                 related_name=None, pk=None):  # pylint: disable=invalid-name
        # pylint: disable=invalid-name
        self.primary, self.secondary = primary, secondary
        self.related_name, self.pk = related_name, pk
        # pylint: disable=invalid-name

        if secondary and pk:
            raise AttributeError('Both classes were provided and pk. This'
                                 ' can cause inconsistencies')

    def make(self, related_name=None):
        self._fill_attributes(related_name=related_name)
        self._check_all_core_attributes_filled()
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
        self._check_all_core_attributes_filled()

        try:
            related = self.get_related(return_manager=True)
        except AttributeError:
            related = self.get_related()

        if self.is_many():
            return related.filter(pk=self.secondary.pk).exists()
        return related == self.secondary

    def has_nested_relationship(self, *relateds_metas, return_manager=False):
        try:
            self.get_nested_related(return_manager=return_manager,
                                    *relateds_metas)
            return True
        except ObjectDoesNotExist:
            return False

    def get_related(self, *, return_manager=False):
        self._check_relatedname()

        related = None
        if self.is_many():
            related_manager = getattr(self.primary, self.related_name)

            related = related_manager
            if not return_manager:
                if self.pk:
                    related = related_manager.filter(pk=self.pk)

                    if related.exists():
                        related, = related
                    else:
                        raise ObjectDoesNotExist(
                            'Was not possible to get the object indicated by'
                            ' the information passed. pk not found.'
                        )
                else:
                    related = related_manager.last()
        else:
            if not return_manager:
                try:
                    related = getattr(self.primary, self.related_name)
                except AttributeError:
                    related = None
            else:
                raise AttributeError('return_manager is valid only for'
                                     ' "to many" relationships')

        return related

    def get_nested_related(self, *relateds_metas, return_manager=False):
        related = self.primary

        for related_meta in relateds_metas:
            relationship = Relationship(
                related,
                related_name=related_meta.related_name, pk=related_meta.pk
            )
            if related_meta is not relateds_metas[-1]:
                related = relationship.get_related()

                if related is None:
                    raise AttributeError(
                        "Not possible getting nested related."
                        " '{}' related_name got a None object.".format(
                            relationship.related_name
                        )
                    )

            else:
                try:
                    related = relationship.get_related(
                        return_manager=return_manager
                    )
                except AttributeError:
                    related = relationship.get_related()

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
            primary__class_name = self.primary.__class__.__name__
            secondary__class_name = self.secondary.__class__.__name__

            raise AttributeError(
                "'{}' is not a valid related_name for {}{}".format(
                    self.related_name,
                    primary__class_name,
                    " nor for {}.".format(secondary__class_name) if
                    self.secondary else "."
                )
            )

    def _check_all_core_attributes_filled(self):
        missing = ''

        if not self.secondary:
            missing = 'secondary'
        elif not self.related_name:
            missing = 'related_name'

        if missing:
            raise AttributeError("Not enough information, '{}' is missing."
                                 .format(missing))

    def _fill_attributes(self, primary=None,  # pylint: disable=invalid-name
                         secondary=None, related_name=None, pk=None):

        self.primary = primary or self.primary
        self.secondary = secondary or self.secondary
        self.related_name = related_name or self.related_name
        self.pk = pk or self.pk

    def __str__(self):
        primary_name = self.primary.__class__.__name__

        if self.secondary:
            secondary_name = self.secondary.__class__.__name__
        else:
            secondary_name = ''

        return '({} : {})'.format(primary_name,
                                  secondary_name if secondary_name else "")
