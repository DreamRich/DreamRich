class Relationship:
    def __init__(self, primary, secondary, many=None, relationship_attr=None):
        self.many, self.relationship_attr = many, relationship_attr
        self.primary, self.secondary = primary, secondary

        if many is not None and relationship_attr:  # If has enough info
            self.make()

    def make(self, primary=None, secondary=None,
             many=None, relationship_attr=None):

        self._fill_missing_attributes(primary, secondary, many,
                                      relationship_attr)

        if not self._has_relationship():
            raise AttributeError('There is no relationship between'
                                 ' user and consulted classes')

        # Avoid typing :)
        primary, secondary, many, attr = self.primary, self.secondary, \
            self.many, self.relationship_attr

        if many is None and not attr:
            raise Exception('Not enough information for making relationship')

        if many:
            attr = getattr(secondary, attr)
            attr.add(primary)  # Making relationship 1 or n to many
        else:
            secondary.delete()  # Avoid unique constraint problems
            setattr(secondary, attr, primary)  # Making relationship 1 to 1

            try:
                secondary.save()
            except ValueError:
                primary_name = primary.__class__.__name__
                secondary_name = secondary.__class__.__name__

                raise ValueError("Wasn't possible to create relashionship"
                                 " between {} and {} models"
                                 .format(primary_name, secondary_name))

    def get_info(self):
        return (self.many, self.relationship_attr,
                self.primary, self.secondary)

    def _has_relationship(self):

        # Primary will have primary key and secondary the foreign key
        # hasattr called twice to test A to B and B to A relationships
        if not hasattr(self.secondary, self.relationship_attr):
            self.primary, self.secondary = self.secondary, self.primary

        return hasattr(self.secondary, self.relationship_attr)

    # Can't use None because None will be used to check what params were passed
    def _fill_missing_attributes(self, primary=None, secondary=None,
                                 many=None, relationship_attr=None):

        self.primary = primary or self.primary
        self.secondary = secondary or self.secondary
        self.many = many or self.many
        self.relationship_attr = relationship_attr or self.relationship_attr

    def __str__(self):
        return str(self.get_info())
