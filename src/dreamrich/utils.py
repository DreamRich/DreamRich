from django.core.exceptions import ObjectDoesNotExist


class Relationship:

    def __init__(self, primary, secondary, related_name=None, many=None):
        self.many, self.related_name = many, related_name
        self.primary, self.secondary = primary, secondary

    def make(self, primary=None, secondary=None, related_name=None, many=None):
        self._check_attributes_for_make()
        self._fill_missing_attributes(primary, secondary, many, related_name)
        self._check_relatedname()

        is_ok = True
        if self.many:
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

    def _check_relatedname(self):
        if not self.related_name:
            raise AttributeError('related_name was not provided.')

        swapped = False
        is_valid = True

        while True:
            try:
                getattr(self.primary, self.related_name)
            except ObjectDoesNotExist:
                break
            except AttributeError:
                self.primary, self.secondary = self.secondary, self.primary

                if swapped:
                    is_valid = False
                    break
                swapped = True
            break

        if not is_valid:
            raise AttributeError('related_name passed is not valid for any'
                                 ' of given objects.')

    def _check_attributes_for_make(self):
        missing = ''

        if self.many is None:
            missing = 'many'
        elif not self.related_name:
            missing = 'related_name'
        if missing:
            raise AttributeError('Not enough information, {} is missing.'
                                 .format(missing))

    def _fill_missing_attributes(self, primary=None, secondary=None,
                                 many=None, related_name=None):

        self.primary = primary or self.primary
        self.secondary = secondary or self.secondary
        self.many = many or self.many
        self.related_name = related_name or self.related_name

    def __str__(self):
        primary_name = self.primary.__class__.__name__
        secondary_name = self.secondary.__class__.__name__

        return "{} has{}{}".format(
            primary_name,
            " many " if self.many else " ",
            secondary_name
        )
