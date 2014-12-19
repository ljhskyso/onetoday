import peewee
from peewee import *

db = MySQLDatabase('hw2', user='dbhw',passwd='')

class Book(peewee.Model):
    author = peewee.CharField()
    title = peewee.TextField()

    class Meta:
        database = db

Book.create_table()
book = Book(author="me", title='Peewee is cool')
book.save()sa
for book in Book.filter(author="me"):
    print book.title

# Peewee is cool