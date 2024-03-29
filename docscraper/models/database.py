from peewee import AutoField, TextField, ForeignKeyField, SqliteDatabase, Model, DateTimeField
import datetime


db = SqliteDatabase("docscraper.db")


class BaseModel(Model):
    class Meta:
        database = db


# todo add null=True to all fields that could be empty
class Doctors(BaseModel):
    id = AutoField()
    name = TextField()
    profile_url = TextField()
    doctor_id = TextField(null=True)
    field_of_work = TextField()
    address = TextField()
    phone = TextField(null=True)
    email = TextField(null=True)
    office_type = TextField(null=True)
    fax = TextField(null=True)
    website = TextField(null=True)
    lanr = TextField(null=True)
    bsnr = TextField(null=True)
    office_type = TextField(null=True)
    first_scraped = DateTimeField(default=datetime.datetime.now)
    last_scraped = DateTimeField(default=datetime.datetime.now)


class Licenses(BaseModel):
    license_id = AutoField()
    license_type = TextField(null=True)

class Doctors_Licenses(BaseModel):
    doctor_id = ForeignKeyField(Doctors, related_name='doctor_id')
    license_id = ForeignKeyField(Licenses, related_name='license_id')

def setup_database():
    db.connect()
    db.create_tables([Doctors, Licenses, Doctors_Licenses])
    db.close()

