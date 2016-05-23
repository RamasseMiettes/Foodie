from Database import session
from flask import abort, jsonify

from Database import RestaurantsDbTable, ReservationDbTable, DishDbTable

from Tools import check_params
from Exceptions import build_error_response, build_error_object

class Restaurants:
    def create(self, data):
        check_filter = ['name', 'description', 'address', 'owner_id', 'seats', 'longitude', 'latitude']
        if (check_params(data, check_filter) == False):
            return build_error_response(-1, 'Not enough parameters.')
        restaurant = RestaurantsDbTable()
        restaurant.name = data['name']
        restaurant.address = data['address']
        restaurant.description = data['description']
        restaurant.owner_id = data['owner_id']
        restaurant.seats = data['seats']
        restaurant.longitude = data['longitude']
        restaurant.latitude = data['latitude']
        session.add(restaurant)
        session.commit()
        return (build_error_response(0, 'All done.'))

    def update(self, id, data):
        allowed_changes = ['name', 'description', 'address', 'seats', 'longitude', 'latitude']
        if not data:
            return build_error_response(-1, "Not enough parameters.")
        q = session.query(RestaurantsDbTable).filter_by(id = id).first()
        if q is not None:
            for key in allowed_changes:
                if key in data:
                    q.set_value_by_name(key, data[key])
            session.commit()
        else:
            return build_error_response(-2, 'Restaurant does not exist.')
        return build_error_response(0, 'All done.')

    def delete(self, id):
        if id.isdigit() == False:
            return build_error_response(+3, "Bad ID.")
        q = session.query(RestaurantsDbTable).filter_by(id = id).first()
        if q is not None:
            q2 = session.query(ReservationDbTable).filter_by(id_restaurant=id).all()
            q3 = session.query(DishDbTable).filter_by(id_restaurant=id).all()
            for i in q2:
                session.delete(i)
            for i in q3:
                session.delete(i)
            session.delete(q)
            session.commit()
        else:
            return build_error_response(-2, "Restaurant does not exist.")
        return build_error_response(0, 'All done.')

    def get(self, id):
        if id.isdigit() == False:
            return build_error_response(+3, "Bad ID.")
        q = session.query(RestaurantsDbTable).filter_by(id=id).first()
        if q is not None:
            retObject = {
                'error' : build_error_object(0, 'All done.'),
                'id' : id,
                'name' : q.name,
                'description' : q.description,
                'address' : q.address,
                'owner_id' : q.owner_id,
                'seats' : q.seats,
                'longitude' : q.longitude,
                'latitude' : q.latitude}
            return jsonify(retObject)
        else:
            return build_error_response(-2, "Restaurant does not exist.")

    def list(self):
        q = session.query(RestaurantsDbTable).all()
        if q is None:
            return  build_error_response(-4, "Unknown error from database.")
        l = list()
        for item in q:
            o = {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'address': item.address,
                'owner_id': item.owner_id,
                'seats': item.seats,
                'longitude': item.longitude,
                'latitude': item.latitude
            }
            l.append(o)
        retObject = {
            'error' : build_error_object(0, 'All done'),
            'list' : l
        }
        return jsonify(retObject)

    def search_by_name(self, name):
        name = '%' + name + '%'
        q = session.query(RestaurantsDbTable).filter(RestaurantsDbTable.name.like(name)).all()
        if q is None:
            return build_error_response(-4, "Unknown error from database.")
        l = list()
        for item in q:
            o = {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'address': item.address,
                'owner_id': item.owner_id,
                'seats': item.seats,
                'longitude': item.longitude,
                'latitude': item.latitude
            }
            l.append(o)
        retObject = {
            'error': build_error_object(0, 'All done'),
            'list': l
        }
        return jsonify(retObject)

    def search_by_owner(self, id):
        if id.isdigit() == False:
            return build_error_response(+3, "Bad ID.")
        q = session.query(RestaurantsDbTable).filter_by(owner_id = id).all()
        if q is None:
            return build_error_response(-4, "Unknown error from database.")
        l = list()
        for item in q:
            o = {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'address': item.address,
                'owner_id': item.owner_id,
                'seats': item.seats,
                'longitude': item.longitude,
                'latitude': item.latitude
            }
            l.append(o)
        retObject = {
            'error': build_error_object(0, 'All done'),
            'list': l
        }
        return jsonify(retObject)