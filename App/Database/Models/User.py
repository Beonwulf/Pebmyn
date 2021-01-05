from flask_security import Security, UserMixin, RoleMixin, SQLAlchemyUserDatastore
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey
from App.Database.db import db, Base


class Role(db.Model, RoleMixin):
    __tablename__ = 'Role'

    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __str__(self):
        return self.name


class RolesUsers(db.Model):
    __tablename__ = 'Roles_Users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('User.id'))
    role_id = Column('role_id', Integer(), ForeignKey('Role.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    password = Column(String(100), nullable=False)
    first_name = Column(String(55))
    last_name = Column(String(55))
    roles = relationship('Role', secondary='Roles_Users', backref=backref('Users', lazy='dynamic'))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    confirmed_at = Column(DateTime())
    active = Column(Boolean)
    
    
    # Custom User Payload
    def get_security_payload(self):
        return {
            'id': self.id,
            'name': self.username,
            'email': self.email,
            'confirmed': self.confirmed_at
        }


    def table_exists(self):
        pass

    def __int__(self):
        return self.id

    def __str__(self):
        return self.email
