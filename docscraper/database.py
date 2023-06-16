from peewee import *
import datetime


db = SqliteDatabase('docscraper.db')

class BaseModel(Model):
    class Meta:
        database = db

class Doctors(BaseModel):
    id = AutoField()
    name = TextField()
    profile_url = TextField()
    doctor_id = TextField()
    field_of_work = TextField()
    address = TextField()
    phone = TextField()
    email = TextField()
    office_type = TextField()
    fax = TextField()
    website = TextField()

class Licenses(BaseModel):
    id = ForeignKeyField(Doctors, backref='licenses')
    license_type = TextField()


def setup_database():
    db.connect()
    db.create_tables([Article, Keyword, Author])
    db.close()