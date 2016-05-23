from passlib.handlers.sha2_crypt import sha256_crypt
from Database import session, UsersDbTable
from flask import abort, jsonify
import random


class Users:
    field_for_register = ['name', 'surname', 'email', 'password', 'pseudo', 'type']

    def register(self, data):
        customer = session.query(UsersDbTable).filter_by(email=data['email']).first()
        if customer is None:
            bits = random.getrandbits(126)
            token = hex(bits)
            customer = UsersDbTable(name=data['name'],
                                    surname=data['surname'],
                                    email=data['email'],
                                    password=sha256_crypt.encrypt(data['password']),
                                    pseudo=data['pseudo'],
                                    type=data['type'],
                                    token=token)
            session.add(customer)
            session.commit()
            return customer.token
        else:
            abort(409)

    def update(self, data):
        customer = session.query(UsersDbTable).filter_by(email=data['email']).first()
        if customer is None:
            abort(400)
        else:
            customer.name = customer.name if (data['name'] == '' or data['name'] == None) else data['name']
            customer.surname = customer.surname if (data['surname'] == '' or data['surname'] == None) else data['surname']
            customer.email = customer.email if (data['email'] == '' or data['email'] == None) else data['email']
            customer.password = customer.password if (data['password'] == '' or data['password'] == None) else sha256_crypt.encrypt(data['password'])
            customer.pseudo = customer.pseudo if (data['pseudo'] == '' or data['pseudo'] == None) else data['pseudo']
            customer.type = customer.type if (data['type'] == '' or data['type'] == None) else data['type']

            session.add(customer)
            session.commit()
            return (
            {'name': customer.name, 'surname': customer.surname, 'email': customer.email, 'pseudo': customer.pseudo,
             'type': customer.type, 'token': customer.token, 'id': customer.id})

    def login(self, data):
        customer = session.query(UsersDbTable).filter_by(email=data['email']).first()
        if customer is not None:
            if sha256_crypt.verify(data['password'], customer.password) is False:
                abort(401)
            else:
                return (
                    {'name': customer.name, 'surname': customer.surname, 'email': customer.email,
                     'pseudo': customer.pseudo,
                     'type': customer.type, 'token': customer.token})
        else:
            abort(401)

    def check_token(self, token):
        customer = session.query(UsersDbTable).filter_by(email=data['email']).first()
        if customer is not None:
            if sha256_crypt.verify(data['password'], customer.password) is False:
                abort(401)
            else:
                return (
                    {'name': customer.name, 'surname': customer.surname, 'email': customer.email,
                     'pseudo': customer.pseudo,
                     'type': customer.type, 'token': customer.token})
        else:
            abort(401)

    def search_user_by_name(self, name):
        customer = session.query(UsersDbTable).filter_by(name=name).all()
        if customer is not None:
            return customer
        else:
            abort(401)

    def delete(self, data):
        customer = session.query(UsersDbTable).filter_by(token=data['token']).first()
        if customer is not None:
            session.delete(customer)
            session.commit()
        else:
            abort(409)

    def get_manager(self, data):
        customer = session.query(UsersDbTable).filter_by(token=data['token']).first()
        if customer is not None:
            json = jsonify({'first_name': customer.first_name,
                            'last_name': customer.last_name,
                            'email_adress': customer.email_adress
                            })
        else:
            abort(409)
        return json
