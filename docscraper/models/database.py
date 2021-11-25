import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine(
    "sqlite:///docscraper.db", echo=True
)  # echo=True for debugging only
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile_url = Column(String)
    doc_nr = Column(String)
    field_of_work = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    office_type = Column(String)
    fax = Column(String)
    website = Column(String)
    lanr = Column(String)
    bsnr = Column(String)
    scrape_doctor = relationship(
        "scrape_doctor"
    )  # I am not sure, what this is for tbh.

    def __repr__(self):
        return (
            "<Doctor(name='%s', profile_url='%s', doc_nr='%s', field_of_work='%s', address='%s', phone='%s', email='%s', office_type='%s', fax='%s', website='%s', lanr='%s', bsnr='%s', office_type='%s')>"
            % (
                self.name,
                self.profile_url,
                self.doc_nr,
                self.field_of_work,
                self.address,
                self.phone,
                self.email,
                self.office_type,
                self.fax,
                self.website,
                self.lanr,
                self.bsnr,
            )
        )


class Scrape(Base):
    __tablename__ = "scrape"

    id = Column(
        Integer, primary_key=True
    )  # autoincrement is not recommended for sqlite and not needed. Remember to set it when switching to another database engine.
    query = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    scrape_doctor = relationship("scrape_doctor")

    def __repr__(self):
        return "<Scrape(query='%s', timestamp='%s')>" % (self.query, self.timestamp)


class Scrape_Doctor(Base):
    __tablename__ = "scrape_doctor"

    id_scrape = Column(Integer, ForeignKey("scrape.id"), primary_key=True)
    id_doctor = Column(Integer, ForeignKey("doctor.id"), primary_key=True)
    doctor = relationship("doctor", backref="scrape_doctor")
    scrape = relationship("scrape", backref="scrape_doctor")
    license = relationship("license", backref="scrape_doctor")

    def __repr__(self):
        return "<Scrape_Doctor(id_scrape='%s', id_doctor='%s')>" % (
            self.id_scrape,
            self.id_doctor,
        )


class License(Base):
    __tablename__ = "license"

    title = Column(String)
    id = Column(Integer, primary_key=True)
    id_scrape_scrape_doctor = Column(Integer, ForeignKey("scrape_doctor.id_scrape"))
    id_doctor_scrape_doctor = Column(Integer, ForeignKey("scrape_doctor.id_doctor"))
    # these are some confusing column names.
    scrape_doctor = relationship("scrape_doctor")

    def __repr__(self):
        return (
            "<License(title='%s', id='%s', id_scrape_scrape_doctor='%s', id_doctor_scrape_doctor='%s')>"
            % (
                self.title,
                self.id,
                self.id_scrape_scrape_doctor,
                self.id_doctor_scrape_doctor,
            )
        )


# set PRAGMA foreign_keys = ON before every connection to the database.
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def setup_database():
    Base.metadata.create_all(engine)


# only for debugging purposes.
if __name__ == "__main__":
    setup_database()
