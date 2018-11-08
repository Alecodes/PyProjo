from peewee import *
from os import path
ROOT = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(ROOT,"users.db"))

class User(Model):
    sname = CharField()
    fname = CharField()
    lname = CharField()
    email = CharField(unique=True)
    phone = CharField()
    password = CharField()
    class Meta:
        database = db


class Patient(Model):
    sname = CharField()
    fname = CharField()
    lname = CharField()
    wardnumber = IntegerField()
    nextofkin = CharField()
    nextofkinfon = CharField()

    class Meta:
        database = db


User.create_table(fail_silently=True)
Patient.create_table(fail_silently=True)