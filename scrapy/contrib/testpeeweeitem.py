
import os
import scrapy

from peewee import *
db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField(max_length=255)
    nickname = CharField(max_length=255)
    birthday = DateField(null=True)
    age = IntegerField(null=True)
    is_relative = BooleanField(default=True)

    class Meta:
        database = db # This model uses the "people.db" database.

if not os.path.exists('people.db'):
    db.connect()
    #We'll begin by creating the tables in the database that will store our data.
    #This will create the tables with the appropriate columns, indexes, sequences,
    #and foreign key constraints:
    db.create_tables([Person,])



class PersonItem2(scrapy.Item):
    name=scrapy.Field()
    age=scrapy.Field()
    nickname=scrapy.Field(default='No Nickname')

p = PersonItem2()
print 'p2',p, p.fields
p['name'] = 'John'
p['age'] = '22'
print 'p2',p, p.fields

#Defining a basic DjangoItem:

from scrapy.contrib.peeweeitem import PeeweeItem

class PersonItem(PeeweeItem):
    peewee_model = Person
    nickname=scrapy.Field(default='No Nickname')


#PeeweeItem work just like Item:

p = PersonItem()
print 'p',p
p['name'] = 'John'
p['age'] = '22'

print dir(p)
print 'p.fields', p.fields
print 'p.keys', p.keys()
print p
print 'p type', type(p)

instance=p.save()
print ' p instance type', instance


'''
<type 'dict'> {}
<class 'scrapy.contrib.peeweeitem.PeeweeItem'>
<type 'dict'> {}
<type 'dict'> {'age': <peewee.IntegerField object at 0x00BF0790>, 'birthday': <peewee.DateField object at 0x00BF06D0>, 'is_relative': <peewee.BooleanField object at 0x00BF0850>, 'id': <peewee.PrimaryKeyField object at 0x00BF0D50>, 'name': <peewee.CharField object at 0x00BEE310>}
<class '__main__.PersonItem'>
{'age': '22', 'name': 'John'}
p type <class '__main__.PersonItem'>
 p instance type <__main__.Person object at 0x01A978D0>
'''

