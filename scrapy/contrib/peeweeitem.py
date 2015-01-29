from scrapy.item import Field, Item, ItemMeta
from scrapy import optional_features
if 'peewee' in optional_features:
    from django.core.exceptions import ValidationError

from peewee import ProgrammingError, IntegrityError

class PeeweeItemMeta(ItemMeta):

    def  __new__(mcs, class_name, bases, attrs):
        cls = super(PeeweeItemMeta, mcs).__new__(mcs, class_name, bases, attrs)
        cls.fields = cls.fields.copy()
        print 'class fields ',type(cls.fields), cls.fields

        if cls.peewee_model:
            cls._model_fields = []
            cls._model_meta = cls.peewee_model._meta
            # cls._model_meta.fields is a dict, donot like in django which is a list
            print 'peewee_model fields:', type(cls._model_meta.fields), cls._model_meta.fields.keys()
            for name, model_field in cls._model_meta.fields.iteritems():
                print name, model_field.name, type(model_field), model_field
                #print 'dir(model_field)', dir(model_field)
                print 'model_field.primary_key', model_field.primary_key, model_field.constraints,
                print model_field.default
                if not model_field.primary_key:
                    if model_field.name not in cls.fields:
                        cls.fields[model_field.name] = Field()
                    cls._model_fields.append(model_field.name)
        print 'cls.fields',cls.fields
        return cls


class PeeweeItem(Item):

    __metaclass__ = PeeweeItemMeta

    peewee_model = None

    def __init__(self, *args, **kwargs):
        print '*args, **kwargs', args, kwargs
        super(PeeweeItem, self).__init__(*args, **kwargs)

        print 'self init, now is:', self
        self._instance = None
        self._errors = None

    def save(self, commit=True):
        if commit:
            self.instance.save()
        return self.instance

    def is_valid(self, exclude=None):
        self._get_errors(exclude)
        return not bool(self._errors)

    def _get_errors(self, exclude=None):
        if self._errors is not None:
            return self._errors

        self._errors = {}
        if exclude is None:
            exclude = []

        try:
            self.instance.clean_fields(exclude=exclude)
        except ValidationError as e:
            self._errors = e.update_error_dict(self._errors)

        try:
            self.instance.clean()
        except ValidationError as e:
            self._errors = e.update_error_dict(self._errors)

        # uniqueness is not checked, because it is faster to check it when
        # saving object to database. Just beware, that failed save()
        # raises IntegrityError instead of ValidationError.

        return self._errors
    errors = property(_get_errors)

    @property
    def instance(self):
        if self._instance is None:
            modelargs = dict((k, self.get(k)) for k in self._values
                             if k in self._model_fields)
            print 'modelargs', modelargs
            self._instance = self.peewee_model(**modelargs)
        return self._instance
