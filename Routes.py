import os

from flask import Flask, request, abort, jsonify
from flask_apidoc import ApiDoc
from flask_apidoc.commands import GenerateApiDoc
from flask_script import Manager
from flask.ext.httpauth import HTTPBasicAuth

from Users import Users
from Restaurant import Restaurants
from Reservation import Reservation
from Dish import Dish

from Database import Session, session

from Exceptions import exception_not_implemented

app = Flask(__name__)
doc = ApiDoc(app=app)
auth = HTTPBasicAuth()
restaurants = Restaurants()
dish = Dish()
reservation = Reservation()

"""Routes for documentation"""
@app.route('/', methods=['GET'])
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)
""""""

# @auth.verify_password
# def verify_password(token):
#     # first try to authenticate by token
#     user = User.verify_auth_token(username_or_token)
#     if not user:
#         # try to authenticate with username/password
#         user = User.query.filter_by(username = username_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True

"""Routes for user"""
@app.route('/user/create', methods=['POST'])
def register_user():
    """
        @api {post} /user/create Add a new user
        @apiVersion 1.0.0
        @apiName add_user
        @apiGroup User

        @apiParam {String}      name        User's name.
        @apiParam {String}      surname     User's surname.
        @apiParam {String}      email       User's email.
        @apiParam {String}      pseudo      User's pseudo.
        @apiParam {Number}      type        User's type.
        @apiParam {String}      password    User's password.

        @apiSuccess {String}    Token       Must be used in every request to the API.
        """
    if not request.json:
        abort(400)
    user_input = request.json

    user = Users()
    for field in user.field_for_register:
        value = user_input.get(field)
        if value == '' or value == None:
            abort(400)
    token = user.register(user_input)
    return jsonify({'token': token})

@app.route('/user/login', methods=['POST'])
def login_user():

    if not request.json:
        abort(400)

    user = Users()
    if request.json['email'] == None or request.json['email'] == '':
        abort(400)
    if request.json['password'] == None or request.json['password'] == '':
        abort(400)

    user_info = user.login(request.json)
    return jsonify(user_info)
    return

@app.route('/user/update', methods=['PUT'])
#@auth.login_required
def update_user():

    if not request.json:
        abort(400)
    isEmpty = True
    user = Users()
    for field in user.field_for_register:
        value = request.json.get(field)
        if value != '' and value != None:
            isEmpty = False

    if isEmpty is False:
        updateUser = user.update(request.json)
        return jsonify(updateUser)
    else:
        abort(400)


@app.route('/restaurant/create', methods=['POST'])
def create_restaurant():
    return restaurants.create(request.json)

@app.route('/restaurant/<id>/update', methods=['PUT'])
def update_restaurant(id):
    return restaurants.update(id, request.json)

@app.route('/restaurant/<id>/delete', methods=['DELETE'])
def delete_restaurant(id):
    return restaurants.delete(id)

@app.route('/restaurant/search_name/<name>', methods=['GET'])
def search_restaurant_by_name(name):
    return restaurants.search_by_name(name)

@app.route('/restaurant/search_owner/<id>', methods=['GET'])
def search_restaurant_by_owner(id):
    return restaurants.search_by_owner(id)

@app.route('/restaurant/search_nearby/<lon>/<lat>', methods=['GET'])
def search_restaurant_nearby(lon, lat):
    return exception_not_implemented()

@app.route('/restaurant/list', methods=['GET'])
def list_restaurant():
    return restaurants.list()

@app.route('/restaurant/get/<id>', methods=['GET'])
def get_restaurant(id):
    return restaurants.get(id)

@app.route('/restaurant/<id>/reservations', methods=['GET'])
def get_reservation_restaurant(id):
    return reservation.list_by_restaurant(id)


@app.route('/dish/create', methods=['POST'])
def create_dish():
    return dish.create(request.json)

@app.route('/dish/<id>/update', methods=['PUT'])
def update_dish(id):
    return dish.update(id, request.json)

@app.route('/dish/<id>/delete', methods=['DELETE'])
def delete_dish(id):
    return dish.delete(id)

@app.route('/dish/list/<id>', methods=['GET'])
def get_dishes(id):
    return dish.list(id)


@app.route('/reservation/place', methods=['POST'])
def place_reservation():
    return reservation.place(request.json)

@app.route('/reservation/<id>/cancel', methods=['DELETE'])
def cancel_reservation(id):
    return reservation.cancel(id)

@app.route('/reservation/<id>/update', methods=['PUT'])
def update_reservation(id):
    return reservation.update(id, request.json)

@app.route('/reservation/by_user/<id>')
def list_user_reservation(id):
    return reservation.list_by_user(id)


@app.route('/restart')
def restart_db():
    session.close()
    return 'OK'

""""""

manager = Manager(app)
manager.add_command('apidoc', GenerateApiDoc())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Port : %i" % port)
    app.debug = True
    #app.run()
    app.run(host='0.0.0.0', port=port)