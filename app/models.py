from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from .consts import condition_labels, comorbidity_labels

USER_ADMIN = 128
USER_NORMAL = 8

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(102), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    admin = db.Column(db.Integer, default=USER_NORMAL)
    
    def verify_password(self, password):
        return check_password_hash(self.encrypted_password, password)
    
    @property
    def password(self):
        pass

    @password.setter
    def password(self, value):
        self.encrypted_password = generate_password_hash(value)
    
    @classmethod
    def create_element(cls, username, password, admin=False):
        user = User(username=username, password=password)
        if admin:
            user.admin=USER_ADMIN
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_id(cls, id):
        return User.query.filter_by(id=id).first()
    
    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def set_admin(cls):
        if User.get_by_username('Administrator') == None:
            User.create_element('Administrator','password',True)
    
    @property
    def is_admin(self):
        if self.admin == USER_ADMIN:
            return True
        else:
            return False

    @classmethod
    def update_element(cls, id, name, phone, email):
        user = User.get_by_id(id)
        if user is None:
            return False
        else:
            user.name = name
            user.phone = phone
            user.email = email
            db.session.add(user)
            db.session.commit()
            return user

condi_person = db.Table(
    'condi_person',
    db.Column('person_id', db.Integer, db.ForeignKey('persons.id'), primary_key=True),
    db.Column('condi_id', db.Integer, db.ForeignKey('condis.id'), primary_key=True)
)

comorbidity_person = db.Table(
    'comorbidity_person',
    db.Column('person_id', db.Integer, db.ForeignKey('persons.id'), primary_key=True),
    db.Column('comorbidity_id', db.Integer, db.ForeignKey('comorbidities.id'), primary_key=True)
)

class Condi(db.Model):
    __tablename__ = 'condis'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text(), nullable=False)

    @classmethod # Metodo que crea un registro en la tabla Condi de la BD
    def create_element(cls, label):
        cond = Condi(label=label)
        db.session.add(cond)
        db.session.commit()
        return cond

    @classmethod # Metodo que crea las condiciones por Default
    def set_default(cls):
        for label in condition_labels:
            if Condi.get_by_label(label) == None:
                Condi.create_element(label)

    @classmethod # Metodo que busca el primer elemento a partir del 'label'
    def get_by_label(cls, label):
        return Condi.query.filter_by(label=label).first()

    @classmethod # Metodo que busca el primer elemento a partir del 'id'
    def get_by_id(cls, id):
        return Condi.query.filter_by(id=id).first()

class Comorbidity(db.Model):
    __tablename__ = 'comorbidities'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text(), nullable=False)

    @classmethod # Metodo que crea un registro en la tabla Comorbidity de la BD
    def create_element(cls, label):
        comor = Comorbidity(label=label)
        db.session.add(comor)
        db.session.commit()
        return comor

    @classmethod # Metodo que crea las comorbilidades por Default
    def set_default(cls):
        for label in comorbidity_labels:
            if Comorbidity.get_by_label(label) == None:
                Comorbidity.create_element(label)

    @classmethod # Metodo que busca el primer elemento a partir del 'label'
    def get_by_label(cls, label):
        return Comorbidity.query.filter_by(label=label).first()

    @classmethod # Metodo que busca el primer elemento a partir del 'id'
    def get_by_id(cls, id):
        return Comorbidity.query.filter_by(id=id).first()


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Numeric(4,1), nullable=False)
    disease_temp = db.Column(db.String(50), nullable=False)
    observations = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    condis = db.relationship(
        'Condi',
        secondary=condi_person,
        backref='persons'
    )
    comors = db.relationship(
        'Comorbidity',
        secondary=comorbidity_person,
        backref='persons'
    )

    @classmethod # Metodo que crea un registro en la tabla Person de la BD
    def create_element(cls, name, age, phone, email, temperature, 
                        disease_temp, observations):
        per = Person(name=name, age=age, phone=phone, email=email, temperature=temperature,
                    disease_temp=disease_temp, observations=observations)
        db.session.add(per)
        db.session.commit()
        return per

    @classmethod # Metodo que asocia un registro Person con un Condi
    def set_condi(cls, id, condi):
        per = Person.query.filter_by(id=id).first()
        per.condis.append(condi)
        db.session.commit()

    @classmethod # Metodo que asocia un registro Person con un Comorbidity
    def set_comor(cls, id, comor):
        per = Person.query.filter_by(id=id).first()
        per.comors.append(comor)
        db.session.commit()

    @classmethod
    def get_all(cls, page, per_page):
        return db.session.query(Person).paginate(page=page, per_page=per_page)