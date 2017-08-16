# flight-booking-api-system


FLIGHT BOOKING SYSTEM BACKEND PROJECT 

             USING  PYTHON AND FLASK


REQUIREMENT:



Design a flight booking api system. You should have following end points.



   GET: /flights     : Returns all the flights
   GET: /flight/<flight_no>   : Returns specific flight data
   HEAD: /flight/<flight_no> : Check if flight exist 
   POST /flights      : Add new flight. Each flight must have atleast total seats. 
   PATCH /flight/<flight_no> : Update flight dataDELETE /flight/<flight_no>






Provide booking functions:

      
      GET: /flight/<flight_no>/availability  : must return the number of seats available. 
      
      
      
      POST:  /flight/<flight_no>/book  : In payload you should atleast pass number of seats and booking person's contact email. Response must return a unique booking_id.
      
      
      
      GET: /flight/<flight_no>/book/<booking_id>  : Get booking information.Booking records should also be maintained in a separate collection.  Support Partial/full booking cancellation using 
      
      
      
      
      PATCH/DELETE end points. Use your creativity.e.g. uri /flight/<flight_no>/book/<booking_id>In payload you should pass number of seats to be released. This should update the booked seats in db. If the all seats are released, booking get totally canceled and entry is removed from DB. But if only few seats are released, we just update the DB entry with remaining seats.




Technologies required:

1.Python 3
2.MongoDb Database
3.Pycharm
4.JSON
5.XML

