from Database import DishDbTable, RestaurantsDbTable, session
from flask import jsonify

from Tools import check_params
from Exceptions import *

class Dish:
    def check_restaurant(self, id):
        q = session.query(RestaurantsDbTable).filter_by(id=id).first()
        if q is None:
            return False
        return True

    def create(self, data):
        check_filter = ['name', 'description', 'id_restaurant', 'price']
        if (check_params(data, check_filter) == False):
            return build_error_response(-1, 'Not enough parameters.')
        if self.check_restaurant(data['id_restaurant']) == False:
            return build_error_response(-2, 'Restaurant does not exist.')
        dish = DishDbTable()
        dish.name = data['name']
        dish.description = data['description']
        dish.id_restaurant = data['id_restaurant']
        dish.price = data['price']
        session.add(dish)
        session.commit()
        return (build_error_response(0, 'All done.'))

    def update(self, id, data):
        allowed_changes = ['name', 'description', 'price', 'id_restaurant']
        if not data:
            return build_error_response(-1, "Not enough parameters.")
        q = session.query(DishDbTable).filter_by(id=id).first()
        if q is not None:
            for key in allowed_changes:
                if key in data:
                    q.set_value_by_name(key, data[key])
            session.commit()
        else:
            return build_error_response(-2, 'Dish does not exist.')
        return build_error_response(0, 'All done.')

    def delete(self, id):
        if id.isdigit() == False:
            return build_error_response(+3, "Bad ID.")
        q = session.query(DishDbTable).filter_by(id=id).first()
        if q is not None:
            session.delete(q)
            session.commit()
        else:
            return build_error_response(-2, "Dish does not exist.")
        return build_error_response(0, 'All done.')

    def get(self, id):
        if id.isdigit() == False:
            return build_error_response(+3, "Bad ID.")
        q = session.query(DishDbTable).filter_by(id=id).first()
        if q is not None:
            retObject = {
                'error': build_error_object(0, 'All done.'),
                'id': id,
                'name': q.name,
                'description': q.description,
                'id_restaurant': q.id_restaurant,
                'price': q.price}
            return jsonify(retObject)
        else:
            return build_error_response(-2, "Dish does not exist.")

    def list(self, id):
        if id.isdigit() == False:
            return build_error_response(+3, "Bad ID.")
        q = session.query(DishDbTable).filter_by(id_restaurant=id).all()
        if q is None:
            return build_error_response(-4, "Unknown error from database.")
        l = list()
        for item in q:
            o = {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'id_restaurant': item.id_restaurant,
                'price': item.price
            }
            l.append(o)
        retObject = {
            'error': build_error_object(0, 'All done'),
            'list': l
        }
        return jsonify(retObject)