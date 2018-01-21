from django.core.exceptions import ObjectDoesNotExist


class Relationship:

    def __init__(self, primary, secondary, related_name=None, many=None):
        self.many, self.related_name = many, related_name
        self.primary, self.secondary = primary, secondary

    def make(self, primary=None, secondary=None, related_name=None, many=None):

        self._fill_missing_attributes(primary, secondary, many, related_name)

        if not self.has_relationship():
            raise AttributeError('There is no relationship between classes'
                                 ' or related_name is wrong')

        if self.many:
            related_manager = getattr(self.primary, self.related_name)
            related_manager.add(self.secondary)
        else:
            setattr(self.primary, self.related_name, self.secondary)

    def has_relationship(self):
        # Check relationship between classes, not objects

        if self.many is None or not self.related_name:
            raise Exception('Not enough information. All attributes must be'
                            ' filled for making a relationship.')

        swapped = False

        while True:
            try:
                getattr(self.primary, self.related_name)
            except ObjectDoesNotExist:
                pass
            except AttributeError:
                self.primary, self.secondary = self.secondary, self.primary

                if swapped:
                    return False
                swapped = True
            break

        return True

    def get(self):
        return (self.primary, self.secondary, self.many, self.related_name)

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
