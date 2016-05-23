from Database import ReservationDbTable, RestaurantsDbTable, session
from sqlalchemy import func
from flask import jsonify

from Tools import check_params
from Exceptions import build_error_response, build_error_object

class Reservation:
    def check_availibility(self, id, date, nb_people):
        q1 = session.query(RestaurantsDbTable).filter_by(id=id).first()
        if q1 is None:
            return -1
        q2 = session.query(func.sum(ReservationDbTable.nb_people).label('people'))\
        .filter(ReservationDbTable.id_restaurant==id, ReservationDbTable.date==date).first()
        reserved = q2[0]
        if reserved is None:
            reserved = 0
        if reserved + nb_people > q1.seats:
            return -2
        return 0

    def place(self, data):
        check_filter = ['id_restaurant', 'date', 'id_user', 'nb_people']
        if check_params(data, check_filter) == False:
            return build_error_response(-1, 'Not enough parameters.')

        err_code = self.check_availibility(data['id_restaurant'], data['date'], data['nb_people'])
        if err_code == -1:
            return build_error_response(-5, 'Restaurant does not exist.')
        elif err_code == -2:
            return build_error_response(-6, 'Not enough seats.')
        reservation = ReservationDbTable()
        reservation.id_restaurant = data['id_restaurant']
        reservation.date = data['date']
        reservation.id_user = data['id_user']
        reservation.nb_people = data['nb_people']
        session.add(reservation)
        session.commit()
        return build_error_response(0, 'All done.')

    def update(self, id, data):
        allowed_changes = ['id_restaurant', 'date', 'nb_people']
        if not data:
            return build_error_response(-1, "Not enough parameters.")
        q = session.query(ReservationDbTable).filter_by(id=id).first()
        if q is not None:
            for key in allowed_changes:
                if key in data:
                    q.set_value_by_name(key, data[key])
            session.commit()
        return build_error_response(0, 'All done.')

    def cancel(self, id):
        if id.isdigit() == False:
            return build_error_response(+3, "Bad ID.")
        q = session.query(ReservationDbTable).filter_by(id=id).first()
        if q is not None:
            session.delete(q)
            session.commit()
        else:
            return build_error_response(-2, "Reservation does not exist.")
        return build_error_response(0, 'All done.')

    def list_by_restaurant(self, id):
        if id.isdigit() == False:
            return build_error_response(+3, "Bad ID.")
        q = session.query(ReservationDbTable).filter_by(id_restaurant=id).all()
        if q is None:
            return build_error_response(-4, "Unknown error from database.")
        l = list()
        for item in q:
            o = {
                'id': item.id,
                'id_user' : item.id_user,
                'id_restaurant' : item.id_restaurant,
                'dishes' : item.dishes,
                'date' : item.date,
                'nb_people' : item.nb_people
            }
            l.append(o)
        retObject = {
            'error': build_error_object(0, 'All done'),
            'list': l
        }
        return jsonify(retObject)

    def list_by_user(self, id):
        if id.isdigit() == False:
            return build_error_response(+3, "Bad ID.")
        q = session.query(ReservationDbTable).filter_by(id_user=id).all()
        if q is None:
            return build_error_response(-4, "Unknown error from database.")
        l = list()
        for item in q:
            o = {
                'id': item.id,
                'id_user': item.id_user,
                'id_restaurant': item.id_restaurant,
                'dishes': item.dishes,
                'date': item.date,
                'nb_people': item.nb_people
            }
            l.append(o)
        retObject = {
            'error': build_error_object(0, 'All done'),
            'list': l
        }
        return jsonify(retObject)

