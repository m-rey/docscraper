from peewee import (
    AutoField,
    SQL,
    TextField,
    ForeignKeyField,
    SqliteDatabase,
    Model,
    DateTimeField,
    CompositeKey,
)
import datetime

db = SqliteDatabase("docscraper.db")


class BaseModel(Model):
    class Meta:
        database = db


# todo add null=True to all fields that could be empty
class Doctor(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField()
    profile_url = TextField()
    doc_nr = TextField(null=True)
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

    class Meta:
        constraints = [
            SQL(
                "UNIQUE (id, name, profile_url, doc_nr, field_of_work, address, phone, email, office_type, fax, website, lanr, bsnr, office_type)"
            )
        ]


class Scrape(BaseModel):
    id = AutoField(primary_key=True)
    query = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)


class Scrape_Doctor(BaseModel):
    id_scrape = ForeignKeyField(Scrape, related_name="id")
    id_doctor = ForeignKeyField(Doctor, related_name="id")

    class Meta:
        database = db
        db_table = "scrape_doctor"
        primary_key = CompositeKey("id_scrape", "id_doctor")


class License(BaseModel):
    title = TextField()
    id = AutoField(primary_key=True)
    id_scrape_scrape_doctor = ForeignKeyField(Scrape_Doctor, related_name="id_scrape")
    id_doctor_scrape_doctor = ForeignKeyField(Scrape_Doctor, related_name="id_doctor")


def setup_database():
    db.connect()
    db.create_tables([Doctor, Scrape, Scrape_Doctor, License])
    db.close()


setup_database()
