from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text, Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('mysql+mysqldb://foodie:epitech@breadnet.cf/foodie')
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

class UsersDbTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    surname = Column(Text)
    email = Column(Text)
    password = Column(Text)
    pseudo = Column(Text)
    token = Column(Text)
    type = Column(Integer)

    def __repr__(self):
        return "<UsersDbTable(id='%d', name='%s', surname='%s', " \
               "email='%s', password='%s', pseudo='%s', token='%s', type='%d')>" % (
            self.id, self.name, self.surname, self.email, self.password,
            self.pseudo, self.token, self.type)

class RestaurantsDbTable(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    address = Column(Text)
    owner_id = Column(Text)
    seats = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)

    def __repr__(self):
        return "<RestaurantDbTable(id='%d', name='%s', description='%s', " \
               "address='%s', owner_id='%d', seats='%d', longitude='%f', latitude='%f')>" % (
            self.id, self.name, self.description, self.address, self.owner_id, self.seats,
            self.longitude, self.latitude
        )

    def set_value_by_name(self, key, value):
        if key == 'id':
            self.id = value
        elif key == 'name':
            self.name = value
        elif key == 'description':
            self.description = value
        elif key == 'address':
            self.address = value
        elif key == 'owner_id':
            self.owner_id = value
        elif key == 'seats':
            self.seats = value
        elif key == 'longitude':
            self.longitude = value
        elif key == 'latitude':
            self.latitude = value

class DishDbTable(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True)
    id_restaurant = Column(Text)
    name = Column(Text)
    description = Column(Text)
    price = Column(Float)

    def __repr__(self):
        return "<DishDbTable(id='%d', id_restaurant='%d' name='%s', description='%s', " \
               "price='%f')>" % (
                   self.id, self.id_restaurant, self.name, self.description, self.price
               )

    def set_value_by_name(self, key, value):
        if key == 'id':
            self.id = value
        elif key == 'name':
            self.name = value
        elif key == 'description':
            self.description = value
        elif key == 'id_restaurant':
            self.id_restaurant = value
        elif key == 'price':
            self.price = value

class ReservationDbTable(Base):
    __tablename__= 'reservations'

    id = Column(Integer, primary_key=True)
    id_restaurant = Column(Integer)
    id_user = Column(Integer)
    dishes = Column(Text, nullable=True)
    date = Column(DateTime)
    nb_people = Column(Integer)

    def __repr__(self):
        return "<ReservationDbTable(id='%d', id_restaurant='%d' id_user='%d', dishes='%s', " \
               "date='%s', nb_people='%d')>" % (
                   self.id, self.id_restaurant, self.id_user, self.dishes, self.date, self.nb_people
               )

    def set_value_by_name(self, key, value):
        if key == 'id':
            self.id = value
        elif key == 'id_user':
            self.id_user = value
        elif key == 'dishes':
            self.dishes = value
        elif key == 'id_restaurant':
            self.id_restaurant = value
        elif key == 'date':
            self.date = value
        elif key == 'nb_people':
            self.nb_people = value