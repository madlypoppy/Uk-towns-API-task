from sqlalchemy import Integer, Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Country is currently the "parent" of everything. It is the "root".
class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    country = Column(String)


# Town is a child of Country
class Town(Base):
    __tablename__ = 'town'
    id = Column(Integer, primary_key=True)
    county = Column(String)
    name = Column(String)
    grid_reference = Column(String)
    easting = Column(Integer)
    northing = Column(Integer)
    latitude = Column(String)
    longitude = Column(String)
    elevation = Column(Integer)
    postcode_sector = Column(String)
    local_government_area = Column(String)
    nuts_region = Column(String)
    town_type = Column(String)
    # We define the relationship between Country and County here.
    country = relation("Country", backref="town")
    country_id = Column(Integer, ForeignKey('country.id'))


# A bunch of stuff to make the connection to the database work.
def dbconnect():
    engine = create_engine('sqlite:///UK_towns.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()