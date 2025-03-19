import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SQLAlchemyEnum, DateTime, Float, Numeric, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from eralchemy2 import render_er

Base = declarative_base()
db = SQLAlchemy()

# Enum for categories of favorites
class CategoryType(enum.Enum):  
    PLANET = "planet"  
    VEHICLE = "vehicle"  
    CHARACTER = "character"  

# User Table
class User(Base):
    __tablename__ = 'user'    
    id = Column(Integer, primary_key=True)
    user_name = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    first_name = Column(String(250))
    last_name = Column(String(250))
    email = Column(String(250), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    favourites = relationship('Favourites', back_populates='user')
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # Do not serialize the password for security reasons
        }

# Favorites Table
class Favourites(Base):
    __tablename__ = 'favourites'    
    id = Column(Integer, primary_key=True)
    type = Column(SQLAlchemyEnum(CategoryType), nullable=False)    
    user_id = Column(Integer, ForeignKey('user.id'))
    planet_id = Column(Integer, ForeignKey('planets.id'), nullable=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=True)
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=True)
    
    user = relationship('User', back_populates='favourites')
    planet = relationship('Planets')
    vehicle = relationship('Vehicles')
    character = relationship('Characters')

# Planets Table
class Planets(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    orbital_period = Column(Float)
    population = Column(Float)
    climate = Column(String(50))

# Vehicles Table
class Vehicles(Base):
    __tablename__ = 'vehicles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    model = Column(String(50))
    vehicle_class = Column(String(50))
    manufacturer = Column(String(50))
    cost_in_credits = Column(Numeric(10, 2))
    length = Column(Float)
    crew = Column(Integer)
    passengers = Column(Integer)

# Characters Table
class Characters(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    gender = Column(String(20))
    birth_year = Column(String(20))
    height = Column(Float)
    mass = Column(Float)

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
