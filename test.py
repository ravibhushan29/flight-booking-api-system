import unittest
from FlightBooking import *

app = Flask(__name__)


class FlaskTestcase(unittest.TestCase):

    def test_checking_create_flight(self):
        testing = app.test_client(self)
        response = testing.post('/flights', data=dict(flight_no='flight_no'), content_type='application/json')
        self.assertTrue('Error": "Flight_no already exist', response.data)
        self.assertTrue(response.status_code, 409)

    def test_create_flight(self):
        testing = app.test_client(self)
        response = testing.post('/flights',data=json.dumps({'flight_name': 'flight_name', 'flight_no': 'flight_no', 'total_seat': 'total_seat'}),content_type='application/json')
        self.assertTrue('Flight data inserted successfully',response.data)
        response = testing.post ('/flights', content_type='application/json')
        self.assertTrue(response.status_code, 201)
        response= testing.post('/flights', content_type='application/xml')
        self.assertTrue(response.status_code, 201)

    def test_get_flight(self):
        testing = app.test_client(self)
        response = testing.get('/flights',content_type='application/json')
        self.assertTrue(response.status,200)
        response = testing.get('/flights', content_type='application/xml')
        self.assertTrue(response.status_code, 200)


    def test_get_one_flight(self):
        testing = app.test_client(self)
        response = testing.get('/flight/<flight_no>', content_type='application/json')
        self.assertTrue(response.status_code, 200)
        response = testing.get('/flight/<flight_no>', content_type='application/xml')
        self.assertTrue(response.status_code, 200)

    def test_get_flight_exist(self):
        testing = app.test_client(self)
        response = testing.head('/flight/<flight_no>', content_type='application/json')
        self.assertTrue(response.status_code, 200)
        response = testing.get('/flight/<flight_no>', content_type='application/xml')
        self.assertTrue(response.status_code, 200)

    def test_update_flight(self):
        testing = app.test_client(self)
        response = testing.patch('/flight/<flight_no>', data=json.dumps({'total_seat':'total_seat'}),content_type='application/json')
        self.assertTrue('Success": "Flight data is updated', response.data)
        response = testing.patch('/flight/<flight_no>', content_type='application/json')
        self.assertTrue(response.status_code, 200)
        response = testing.patch('/flight/<flight_no>', content_type='application/xml')
        self.assertTrue(response.status_code, 200)


    def test_delete_flight(self):
        tester = app.test_client(self)
        response = tester.delete('/flight/<flight_no>', data=dict(flight_no='flight_no'))
        self.assertTrue(response.status_code, 200)

    def test_create_ticket(self):
        testing = app.test_client(self)
        response = testing.post('/flight/<flight_no>/book',data=json.dumps({'no_of_seat': 'no_of_seat', 'flight_no': 'flight_no', 'user_email': 'user_email','user_mob': 'user_mob','source_airport': 'source_airport', 'destination_airport': 'destination_airport'}),content_type='application/json')
        self.assertTrue('Success: Ticket is booked', response.data)
        response = testing.post('/flight/<flight_no>/book', content_type='application/json')
        self.assertTrue(response.status_code, 201)
        response= testing.post('/flights', content_type='application/xml')
        self.assertTrue(response.status_code, 201)

    def test_get_user(self):
        tester = app.test_client(self)
        response = tester.get('/flight/<flight_no>/book/<booking_id>',content_type='application/json')
        self.assertTrue(response.status,200)
        response = tester.get('/flight/<flight_no>/book/<booking_id>', content_type='application/xml')
        self.assertTrue(response.status_code, 200)

    def test_update_ticket(self):
        testing = app.test_client(self)
        response = testing.patch('/flight/<flight_no>/book/<booking_id>', data=json.dumps({'no_of_seat':'no_of_seat'}),content_type='application/json')
        self.assertTrue('Success": "ticket is updated', response.data)
        response = testing.patch('/flight/<flight_no>/book/<booking_id>', content_type='application/json')
        self.assertTrue(response.status_code, 200)
        response = testing.patch('/flight/<flight_no>/book/<booking_id>', content_type='application/xml')
        self.assertTrue(response.status_code, 200)

    def cancel_ticket(self):
        testing = app.test_client(self)
        response = testing.delete('/flight/<flight_no>/book/<booking_id>', data=dict(booking_id='booking_id'))
        self.assertTrue(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
