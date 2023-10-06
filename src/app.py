"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }


    return jsonify(members), 200

######### POST 

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json()
    """  Comentario 
    {
        "first_name": "brian",
        "age": 33,
        "lucky_numbers": [2,5,7]    
    }
    """

    if isinstance(body, dict):
        jackson_family.add_member(body)
        return jsonify("Member added successfully"), 200
    else:
        return jsonify("Bad request"), 400

 ###### GET
 
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    print("id of family member", member_id)
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"msg": "member does not exist"}), 400 

##### DELETE 

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):

    jackson_family.delete_member(member_id)
    return jsonify({"done":True}),200
    # print("id of family member", member_id)
    # message = jackson_family.delete_member(member_id)
    # if message:
    #     return jsonify(message), 200
    # else:
    #     return jsonify({"msg": "member does not exist"}), 400 

##### PUT 

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    body = request.get_json()
    print("id of family member", member_id)
    message = jackson_family.update_member(member_id, body)
    if message:
        return jsonify(message), 200
    else:
        return jsonify({"msg": "error updating member"}), 400 


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)