# from sqlalchemy import Integer, ForeignKey, String, Column
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
#
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#
#     addresses = relationship("Address", back_populates="user")
#
# class Address(Base):
#     __tablename__ = 'address'
#     id = Column(Integer, primary_key=True)
#     email = Column(String)
#     user_id = Column(Integer, ForeignKey('user.id'))
#
#     user = relationship("User", back_populates="addresses")

from sqlalchemy import Integer, ForeignKey, String, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref

Base = declarative_base()

# docs here:
# https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationships are an ORM concept (they're not a part of the database).
    #
    # So relationship() will add an attribute to this User object,
    # that gets populated by the ORM.
    #
    # Backref adds a `user` attribute to the Address object.
    #
    # Without `uselist`, this attribute would take an array,
    # like in many-to-many & many-to-one relations.
    address = relationship(
        "Address", backref=backref("user", uselist=False), uselist=False
    )
    vehicles = relationship("Vehicle", backref="user")


class Vehicle(Base):
    __tablename__ = "vehicle"
    id = Column(Integer, primary_key=True)
    license_plate = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))


engine = create_engine("postgresql://dev:dev@localhost:5435/playground")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# here we create a new user with an address
with session.begin():
    user = User(
        name="mike",
        address=Address(email="mike@test.com"),
        vehicles=[Vehicle(license_plate="QWERTY")],
    )
    session.add(user)

with session.begin():
    users = session.query(User).all()
    addresses = session.query(Address).all()
    user = users[0]
    session.delete(user.address)
