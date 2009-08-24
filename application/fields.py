from django.db import models

class IntegerListField(models.Field):
    """
    IntegerListField keeps a list of int as a comma-separated string.

    >>> g = IntegerListField()
    >>> g.get_db_prep_value([1,2,-1,20,30,40,-100])
    '1,2,-1,20,30,40,-100'

    >>> g.to_python('1,2,-10,3,4,-100,7')
    [1,2,-10,3,4,-100,7]
    """
    __metaclass__ = models.SubfieldBase

    def db_type(self):
        return 'text'

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if value==None or value=='':
            return []
        else:
            return [ int(r) for r in value.split(',') ]

    def get_db_prep_value(self, value):
        return ','.join([str(r) for r in value])

