import pymongo
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId # generates id
from flask import jsonify, request # converts bson to json
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) # declares flask app
app.secret_key = "secretkey"
app.config['MONGO_URI'] = "mongodb://localhost:27017/mydb"

mongo = PyMongo(app) # initializing app, connects mongodb to pymongo library

@app.route('/add', methods=['POST'])
def add_employee():
    _json = request.json
    name = _json['name']
    address = _json['address']
    age = _json['age']
    gender = _json['gender']

    if name and address and age and gender and request.method == 'POST':
        # hashed_password = generate_password_hash(password)
        # id = mongo.db.Employees.insert({'name': name, 'address': address, 'pwd': hashed_password})
        client = pymongo.MongoClient()
        db = client["my_database"]
        col = db["Employees"]
        col.insert_one({'name': name, 'address': address, 'age': age, 'gender': gender})
        response = jsonify("User added successfully.")
        response.status_code = 200 # for success
        return response
    else:
        return not_found()

@app.route('/employees')
def employees():
    client = pymongo.MongoClient()
    db = client["my_database"]
    col = db["Employees"]
    employees = col.find()
    response = dumps(employees)
    return response

@app.route('/employees/<id>')
def employee(id):
    client = pymongo.MongoClient()
    db = client["my_database"]
    col = db["Employees"]
    employee = col.find({'_id': ObjectId(id)})
    response = dumps(employee)
    return response

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    client = pymongo.MongoClient()
    db = client["my_database"]
    col = db["Employees"]
    col.delete_one({'_id': ObjectId(id)})
    response = jsonify("User deleted successfully.")
    response.status_code = 200
    return response

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    client = pymongo.MongoClient()
    db = client["my_database"]
    col = db["Employees"]

    _id = id
    _json = request.json
    name = _json['name']
    address = _json['address']
    age = _json['age']
    gender = _json['gender']

    if name and address and age and gender and _id and request.method == 'PUT':
        # _hashed_password = generate_password_hash(password)
        col.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': name, 'address': address, 'age': age, 'gender': gender}})
        response = jsonify("User updated successfully")
        response.status_code = 200
        return response
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found' + request.url
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True) # automatically restarts app if any changes