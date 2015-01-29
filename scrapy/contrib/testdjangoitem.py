import  os, sys
sys.path.insert(0, r"D:\Projects\peeweeitem\scrapy\contrib\testdjangoitem")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdjangoitem.settings")
from django.conf import settings


#Defining a basic DjangoItem:
from scrapy.contrib.djangoitem import DjangoItem
from djitem.models import Person


class PersonItem(DjangoItem):
    django_model = Person


#PeeweeItem work just like Item:

p = PersonItem()
p['name'] = 'John'
p['age'] = '22'

print p
#p.save()