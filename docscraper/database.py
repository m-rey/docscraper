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
    db.create_tables([Doctors, Licenses])
    db.close()


# run as main to setup database
# this is obviously bad UX, but it's just for testing
if __name__ == '__main__':
    setup_database()