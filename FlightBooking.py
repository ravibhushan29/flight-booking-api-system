

from flask import Flask, jsonify, request, render_template,make_response
from flask_pymongo import PyMongo
import json
import xmltodict
from bson.objectid import ObjectId
import bson


app = Flask(__name__)
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'Flight'
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/flights', methods=['POST'])
def create_flight():
    u = mongo.db.flight_details
    if request.headers['Content-Type'] == 'application/xml':
        obj= xmltodict.parse(request.data)['detail']
        info = u.find_one({'flight_no': obj['flight_no']})
        if info:
            m = make_response(json.dumps({"Error": "User already exist"}))
            m.status_code = 409
            m.mimetype = 'application/json'
            return m
        else:
            users_id = u.insert({'flight_name': obj['flight_name'], 'flight_no': obj['flight_no'], 'total_seat': obj['total_seat']})

            message = make_response(json.dumps({"Success": "Data inserted successfully"}))
            message.status_code = 201
            message.mimetype = 'application/json'
            return message

    elif request.headers['Content-Type'] == 'application/json':
        flight_name = request.json['flight_name']
        flight_no = request.json['flight_no']
        total_seat = request.json['total_seat']
        info = u.find_one({'flight_no': flight_no})
        if info:
            m = make_response(json.dumps({"Error": "Flight_no already exist"}))
            m.status_code = 409
            m.mimetype = 'application/json'

            return m

        else:
            users_id = u.insert({'flight_name': flight_name, 'flight_no': flight_no, 'total_seat': total_seat})

            message = make_response(json.dumps({"Success": "Flight data inserted successfully"}))
            message.status_code = 201
            message.mimetype = 'application/json'

        return message


@app.route('/flights', methods=['GET'])
def get_flight():
    u = mongo.db.flight_details
    info = []
    for q in u.find():
        info.append({'flight_name': q['flight_name'], 'flight_no': q['flight_no'], 'total_seat': q['total_seat'], })
    if request.headers['Content-Type'] == 'application/xml':
        template = render_template('data.xml', info=info)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        return response
    elif request.headers['Content-Type'] == 'application/json':
        return jsonify(info)


@app.route('/flight/<flight_no>', methods=['GET'])
def get_one_user(flight_no):
    u = mongo.db.flight_details
    info = u.find_one({'flight_no': flight_no})
    if info:
        result = {'flight_name': info['flight_name'], 'flight_no': info['flight_no'], 'total_seat': info['total_seat']}
    else:
        my=make_response(jsonify({"Error":"Flight_no is wrong. Plz enter right flight_no"}))
        my.status_code=404
        my.mimetype='application/json'
        return my
    if request.headers['Content-Type'] == 'application/xml':
        template = render_template('data_one.xml', info=info)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        return response
    elif request.headers['Content-Type'] == 'application/json':
        return jsonify(result)



@app.route('/flight/<flight_no>', methods=['HEAD'])
def get_flight_exist(flight_no):
    u = mongo.db.flight_details
    info = u.find_one({'flight_no': flight_no})
    if info:
        my = make_response()
        my.status_code = 200
        my.mimetype = 'application/json'
        return my
    else:
        my=make_response()
        my.status_code=404
        my.mimetype='application/json'
        return my



@app.route('/flight/<flight_no>', methods=['PATCH'])
def update_flight(flight_no):
    u = mongo.db.flight_details
    v =mongo.db.Booked_seat

    total_seat = request.json['total_seat']
    info = u.find_one({'flight_no': flight_no})
    match =v.find({'flight_no': flight_no})
    if info:
        info['total_seat'] = total_seat

        u.save(info)
    else:
        m=make_response(json.dumps({"Error":"Flight does not exist"}))
        m.status_code=404
        m.mimetype='application/json'
        return m

    ms=make_response(json.dumps({"Success":"Flight data is updated"}))
    ms.status_code=200
    ms.mimetype='application/json'
    return ms

@app.route('/flight/<flight_no>', methods=['DELETE'])
def delete_fight(flight_no):
    u = mongo.db.flight_details
    info = u.find_one({'flight_no': flight_no})
    if info:
        u.remove(info)
    else:
        m=make_response(json.dumps({"Error":"Flight does not exist"}))
        m.status_code=404
        m.mimetype='application/json'
        return m
    msg=make_response(json.dumps({"Message":"Flight data is deleted"}))
    msg.status_code=200
    msg.mimetype='application/json'
    return msg
@app.route('/flight/<flight_no>/availability', methods=['GET'])
def get_available(flight_no):
    u = mongo.db.flight_details
    l=mongo.db.Booked_seat
    info = u.find_one({'flight_no': flight_no})
    match=l.find({'flight_no': flight_no})
    if info:
        total_seat=(info['total_seat'])
        pipe =[{'$match': {'flight_no':flight_no}},{'$group': {'_id': None, 'total': {'$sum': '$no_of_seat'}}}]
        v=mongo.db.Booked_seat.aggregate(pipeline=pipe)
        for r in v:
            total_booked=r['total']
            availvable_seat=total_seat-total_booked



    else:
        my=make_response(jsonify({"Error":"Flight_no is wrong. Plz enter right flight_no"}))
        my.status_code=404
        my.mimetype='application/json'
        return my
    if request.headers['Content-Type'] == 'application/xml':
        template = render_template('data_one.xml', info=info)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        return response
    elif request.headers['Content-Type'] == 'application/json':
        return jsonify({"availvable_seat":availvable_seat})


@app.route('/flight/<flight_no>/book', methods=['POST'])
def create_ticket(flight_no):
    u = mongo.db.flight_details
    v = mongo.db.Booked_seat

    no_of_seat = request.json['no_of_seat']
    flight_no=request.json['flight_no']
    user_email = request.json['user_email']
    user_mob =request.json['user_mob']
    source_airport = request.json['source_airport']
    destination_airport=request.json['destination_airport']
    info = u.find_one({'flight_no': flight_no})
    _id= ObjectId()
    _id== ObjectId(str(_id))
    booking_id=str(_id)



    if info :
        users = v.insert({'no_of_seat': no_of_seat, 'flight_no': flight_no, 'user_email': user_email,'user_mob': user_mob,'source_airport': source_airport, 'destination_airport': destination_airport})
        print(users)
        message = make_response(jsonify({'booking_id':booking_id}))
        message.mimetype='text'

        message.status_code = 201



        return message



    else:
        m = make_response(json.dumps({"Error": "Flight_no does not exist, please enter right flight_no"}))
        m.status_code = 404
        m.mimetype = 'application/json'

    return m



@app.route('/flight/<flight_no>/book/<booking_id>' , methods=['GET'])
def get_user(flight_no,booking_id):
    u = mongo.db.flight_details
    v = mongo.db.Booked_seat
    info = v.find_one({'flight_no': flight_no})


    match =v.find_one({'_id':ObjectId(booking_id)})

    if info and match:
        result = ({'no_of_seat':match['no_of_seat'], 'flight_no': match['flight_no'], 'user_email': match['user_email'],'user_mob': match['user_mob'],'source_airport': match['source_airport'], 'destination_airport': match['destination_airport']})
    else:
        my=make_response(jsonify({"Error":"Flight_no or booking_id is wrong."}))
        my.status_code=404
        my.mimetype='application/json'
        return my

    return jsonify(result)

@app.route('/flight/<flight_no>/book/<booking_id>', methods=['PATCH'])
def update_ticket(flight_no,booking_id):
    u = mongo.db.flight_details
    v = mongo.db.Booked_seat

    no_of_seat = request.json['no_of_seat']
    info = v.find_one({'flight_no': flight_no})
    match = v.find_one({'_id': ObjectId(booking_id)})
    if match:          #for decrement in no. of ticket
        result=(match['no_of_seat'])
        final=result-no_of_seat

        match['no_of_seat']=final

        v.save(match)

    else:
        m=make_response(json.dumps({"Error":"Flight or booking_id does not exist"}))
        m.status_code=404
        m.mimetype='application/json'
        return m

    ms=make_response(json.dumps({"Success":"Ticket is updated"}))
    ms.status_code=200
    ms.mimetype='application/json'
    return ms

@app.route('/flight/<flight_no>/book/<booking_id>', methods=['DELETE'])
def canceal_ticket(flight_no,booking_id):
    u = mongo.db.flight_details
    info = u.find_one({'flight_no': flight_no})
    v = mongo.db.Booked_seat
    match = v.find_one({'_id': ObjectId(booking_id)})

    if info and match:
        v.remove(match)
    else:
        m=make_response(json.dumps({"Error":"Flight or booking_id does not exist"}))
        m.status_code=404
        m.mimetype='application/json'
        return m
    msg=make_response(json.dumps({"Message":"ticket is cancealed"}))
    msg.status_code=200
    msg.mimetype='application/json'
    return msg



if __name__ == '__main__':
    app.run(debug=True)




