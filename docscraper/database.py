from peewee import *
import datetime


db = SqliteDatabase('docscraper.db')

class BaseModel(Model):
    class Meta:
        database = db

# todo add null=True to all fields, that could be empty
class Doctors(BaseModel):
    id = AutoField()
    name = TextField()
    profile_url = TextField()
    doctor_id = TextField()
    field_of_work = TextField()
    address = TextField()
    phone = TextField()
    email = TextField(null=True)
    office_type = TextField()
    fax = TextField(null=True)
    website = TextField(null=True)
    office_type = TextField(null=True)
    distance = TextField(null=True)
    first_scraped = DateTimeField(default=datetime.datetime.now)
    last_scraped = DateTimeField(default=datetime.datetime.now)

class Licenses(BaseModel):
    id = ForeignKeyField(Doctors, backref='licenses')
    license_type = TextField()


def setup_database():
    db.connect()
    db.create_tables([Doctors, Licenses])
    db.close()

def insert_item(item):
    db.create_tables([Doctors, Licenses])
    item.save()

# run as main to setup database
# this is obviously bad UX, but it's just for testing
if __name__ == '__main__':
    setup_database()