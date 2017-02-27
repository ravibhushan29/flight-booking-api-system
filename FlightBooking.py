from flask import Flask, jsonify, request, render_template,make_response
from flask_pymongo import PyMongo
import json
import xmltodict
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'Flight'
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/flights', methods=['POST'])
def create_flight():
    flight_data = mongo.db.flight_details
    if request.headers['Content-Type'] == 'application/xml':
        obj= xmltodict.parse(request.data)['detail']
        info = flight_data.find_one({'flight_no': obj['flight_no']})
        if info:
            dublicate_response = make_response('<error>Flight already exist</error>')
            dublicate_response.status_code = 409
            dublicate_response.mimetype = 'application/xml'
            return dublicate_response
        else:
            flight_data.insert({'flight_name': obj['flight_name'],'flight_no': obj['flight_no'], 'total_seat': obj['total_seat']})
            success_response = make_response('<Success>Flight data inserted successfully</Success>')
            success_response.status_code = 201
            success_response.mimetype = 'application/xml'
            return success_response

    elif request.headers['Content-Type'] == 'application/json':
        flight_name = request.json['flight_name']
        flight_no = request.json['flight_no']
        total_seat = request.json['total_seat']
        info = flight_data.find_one({'flight_no': flight_no})
        if info:
            dublicate_response = make_response(json.dumps({"Error": "Flight_no already exist"}))
            dublicate_response.status_code = 409
            dublicate_response.mimetype = 'application/json'
            return dublicate_response

        else:
            flight_data.insert({'flight_name': flight_name, 'flight_no': flight_no, 'total_seat': total_seat})

            success_response = make_response(json.dumps({"Success": "Flight data inserted successfully"}))
            success_response.status_code = 201
            success_response.mimetype = 'application/json'
        return success_response


@app.route('/flights', methods=['GET'])
def get_flight():
    flight_data= mongo.db.flight_details
    info = []
    for index in flight_data.find():
        info.append({'flight_name': index['flight_name'], 'flight_no': index['flight_no'], 'total_seat': index['total_seat'], })
    if request.headers['Content-Type'] == 'application/xml':
        template = render_template('data.xml', info=info)
        xml_response = make_response(template)
        xml_response.headers['Content-Type'] = 'application/xml'
        return xml_response
    elif request.headers['Content-Type'] == 'application/json':
        return jsonify(info)


@app.route('/flight/<flight_no>', methods=['GET'])
def get_one_user(flight_no):
    flight_data = mongo.db.flight_details
    info = flight_data.find_one({'flight_no': flight_no})
    if info:
        result = {'flight_name': info['flight_name'], 'flight_no': info['flight_no'], 'total_seat': info['total_seat']}
    else:
        error_response=make_response(jsonify({"Error":"Flight_no is wrong. Plz enter right flight_no"}))
        error_response.status_code=404
        error_response.mimetype='application/json'
        return error_response
    if request.headers['Content-Type'] == 'application/xml':
        template = render_template('data_one.xml', info=info)
        xml_one_data = make_response(template)
        xml_one_data.headers['Content-Type'] = 'application/xml'
        return xml_one_data
    elif request.headers['Content-Type'] == 'application/json':
        return jsonify(result)


@app.route('/flight/<flight_no>', methods=['HEAD'])
def get_flight_exist(flight_no):
    flight_data = mongo.db.flight_details
    info = flight_data.find_one({'flight_no': flight_no})
    if info:
        flight_exist_response = make_response()
        flight_exist_response.status_code = 200
        return flight_exist_response
    else:
        flight_not_exist_response=make_response()
        flight_not_exist_response.status_code=404
        return flight_not_exist_response



@app.route('/flight/<flight_no>', methods=['PATCH'])
def update_flight(flight_no):
    flight_data = mongo.db.flight_details
    info = flight_data.find_one({'flight_no': flight_no})


    if request.headers['Content-Type'] == 'application/json':
        total_seat = request.json['total_seat']

        if info:
            info['total_seat'] = total_seat
            flight_data.save(info)
        else:
            error_response = make_response(json.dumps({"Error": "Flight does not exist"}))
            error_response.status_code = 404
            error_response.mimetype = 'application/json'
            return error_response

        update_response = make_response(json.dumps({"Success": "Flight data is updated"}))
        update_response.status_code = 200
        update_response.mimetype = 'application/json'
        return update_response
    elif request.headers['Content-Type'] == 'application/xml':
        obj= xmltodict.parse(request.data)['detail']
        data=dict(obj)
        if info:
            info['total_seat']=data['total_seat']
            flight_data.save(info)
            success_response = make_response('<Success>Flight data updated successfully</Success>')
            success_response.status_code = 200
            success_response.mimetype = 'application/xml'
            return success_response
        else:
            error_response = make_response('<error>Flight not exist</error>')
            error_response.status_code = 404
            error_response.mimetype = 'application/xml'
            return error_response

@app.route('/flight/<flight_no>', methods=['DELETE'])
def delete_fight(flight_no):
    flight_data = mongo.db.flight_details
    info = flight_data.find_one({'flight_no': flight_no})
    if request.headers['Content-Type'] == 'application/json':
        if info:
            flight_data.remove(info)
        else:
            error_response = make_response(json.dumps({"Error": "Flight does not exist"}))
            error_response.status_code = 404
            error_response.mimetype = 'application/json'
            return error_response
        delete_fight_response = make_response(json.dumps({"Message": "Flight data is deleted"}))
        delete_fight_response.status_code = 200
        delete_fight_response.mimetype = 'application/json'
        return delete_fight_response

    elif request.headers['Content-Type'] == 'application/xml':
        if info:
            flight_data.remove(info)
            success_response = make_response('<Success>Flight data is deleted</Success>')
            success_response.status_code = 200
            success_response.mimetype = 'application/xml'
            return success_response
        else:
            error_response = make_response('<error>Flight_no not exist</error>')
            error_response.status_code = 404
            error_response.mimetype = 'application/xml'
            return error_response
@app.route('/flight/<flight_no>/availability', methods=['GET'])
def get_available(flight_no):
    flight_data = mongo.db.flight_details
    info = flight_data.find_one({'flight_no': flight_no})
    if info:
        total_seat=(info['total_seat'])
        pipe =[{'$match': {'flight_no':flight_no}},{'$group': {'_id': None, 'total': {'$sum': '$no_of_seat'}}}]
        value_total_sumofseat=mongo.db.Booked_seat.aggregate(pipeline=pipe)
        for search in value_total_sumofseat:
            total_booked=search['total']
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
def create_ticket( flight_no ):
    flight_data = mongo.db.flight_details
    booking_data=mongo.db.Booked_seat
    info = flight_data.find_one({'flight_no': flight_no})

    total_seat = (info['total_seat'])
    pipe = [{'$match': {'flight_no': flight_no}}, {'$group': {'_id': None, 'total': {'$sum': '$no_of_seat'}}}]
    value_total_sumofseat = mongo.db.Booked_seat.aggregate(pipeline=pipe)
    for search in value_total_sumofseat:
        total_booked = search['total']
        availvable_seat = total_seat - total_booked

        if availvable_seat < 1 :

            error_response = make_response(json.dumps({"Error": "ticket is not availABLE"}))
            error_response.status_code = 400
            error_response.mimetype = 'application/json'
            return error_response

        else:
            if request.headers['Content-Type'] == 'application/json':
                no_of_seat = request.json['no_of_seat']
                flight_no = request.json['flight_no']
                user_email = request.json['user_email']
                user_mob = request.json['user_mob']
                source_airport = request.json['source_airport']
                destination_airport = request.json['destination_airport']
                info = flight_data.find_one({'flight_no': flight_no})
                _id = ObjectId()
                _id = ObjectId(str(_id))
                booking_id = str(_id)
                if availvable_seat>=no_of_seat:
                    if info:
                        booking_data.insert(
                            {'no_of_seat': no_of_seat, 'flight_no': flight_no, 'user_email': user_email,
                             'user_mob': user_mob,
                             'source_airport': source_airport, 'destination_airport': destination_airport})

                        booking_response = make_response(jsonify({'booking_id': booking_id}))
                        booking_response.mimetype = 'application/json'
                        booking_response.status_code = 201
                        return booking_response
                    else:
                        error_response = make_response(json.dumps({"Error": "Flight_no does not exist, please enter right flight_no"}))
                        error_response.status_code = 404
                        error_response.mimetype = 'application/json'
                    return error_response
                else:
                    invalid_booking = make_response(json.dumps({"Error": "Entered no_of_seat is more than Available seat"}))
                    invalid_booking.status_code = 400
                    invalid_booking.mimetype = 'application/json'
                return invalid_booking

            elif request.headers['Content-Type'] == 'application/xml':
                obj = xmltodict.parse(request.data)['detail']
                info = flight_data.find_one({'flight_no': obj['flight_no']})
                if info:
                    flight_data.insert({'no_of_seat': obj['no_of_seat'], 'flight_no': obj['flight_no'],'user_email': obj['user_email'],'user_mob':obj['user_mob'],
                                        'source_airport':obj['source_airport'],'destination_airport':obj['destination_airport']})
                    booking_response = make_response('<booking_id>Your ticket is booked</booking_id>')
                    booking_response.status_code = 201
                    booking_response.mimetype = 'application/xml'
                    return booking_response

                else:
                    error_response = make_response('<error>Flight does not exist</error>')
                    error_response.status_code = 404
                    error_response.mimetype = 'application/xml'
                    return error_response



@app.route('/flight/<flight_no>/book/<booking_id>' , methods=['GET'])
def get_user(flight_no,booking_id):
    booking_data = mongo.db.Booked_seat
    match =booking_data.find_one({'_id':ObjectId(booking_id)})

    if match:
        result = ({'no_of_seat':match['no_of_seat'], 'flight_no': match['flight_no'], 'user_email': match['user_email'],'user_mob': match['user_mob'],'source_airport': match['source_airport'], 'destination_airport': match['destination_airport']})
    else:
        my=make_response(jsonify({"Error":"Flight_no or booking_id is wrong."}))
        my.status_code=404
        my.mimetype='application/json'
        return my

    if request.headers['Content-Type'] == 'application/xml':
        template = render_template('booking_one.xml', match=match)
        xml_one_data = make_response(template)
        xml_one_data.headers['Content-Type'] = 'application/xml'
        return xml_one_data
    elif request.headers['Content-Type'] == 'application/json':
        return jsonify(result)

@app.route('/flight/<flight_no>/book/<booking_id>', methods=['PATCH'])
def update_ticket(flight_no,booking_id):
    booking_data = mongo.db.Booked_seat
    match = booking_data.find_one({'_id': ObjectId(booking_id)})
    if request.headers['Content-Type'] == 'application/json':
        no_of_seat = request.json['no_of_seat']
        if match:  # for decrement in no. of ticket
            result = (match['no_of_seat'])
            final = result - no_of_seat
            match['no_of_seat'] = final
            booking_data.save(match)
        else:
            error_update = make_response(json.dumps({"Error": "Flight or booking_id does not exist"}))
            error_update.status_code = 404
            error_update.mimetype = 'application/json'
            return error_update

        update_response = make_response(json.dumps({"Success": "Ticket is updated"}))
        update_response.status_code = 200
        update_response.mimetype = 'application/json'
        return update_response
    elif request.headers['Content-Type'] == 'application/xml':
        obj= xmltodict.parse(request.data)['detail']
        data=dict(obj)
        if match:
            remain_seat=match['no_of_seat']-data['no_of_seat']
            match['no_of_seat']=remain_seat
            booking_data.save(match)
            success_response = make_response('<Success>Flight data updated successfully</Success>')
            success_response.status_code = 200
            success_response.mimetype = 'application/xml'
            return success_response
        else:
            error_response = make_response('<error>Flight not exist</error>')
            error_response.status_code = 404
            error_response.mimetype = 'application/xml'
            return error_response


@app.route('/flight/<flight_no>/book/<booking_id>', methods=['DELETE'])
def cancel_ticket(flight_no,booking_id):
    booking_data = mongo.db.Booked_seat
    match = booking_data.find_one({'_id': ObjectId(booking_id)})
    if request.headers['Content-Type'] == 'application/json':
        if match:
            booking_data.remove(match)
        else:
            error_response = make_response(json.dumps({"Error": "Flight or booking_id does not exist"}))
            error_response.status_code = 404
            error_response.mimetype = 'application/json'
            return error_response
        cancel_response = make_response(json.dumps({"Message": "ticket is cancelled"}))
        cancel_response.status_code = 200
        cancel_response.mimetype = 'application/json'
        return cancel_response
    elif request.headers['Content-Type'] == 'application/xml':
        if match:
            booking_data.remove(match)
            cancel_response = make_response('<Success>Ticket is cancelled</Success>')
            cancel_response.status_code = 200
            cancel_response.mimetype = 'application/xml'
            return cancel_response
        else:
            error_response = make_response('<error>Flight_no not exist</error>')
            error_response.status_code = 404
            error_response.mimetype = 'application/xml'
            return error_response

if __name__ == '__main__':
    app.run(debug=True)









