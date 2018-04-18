import webapp2
import jinja2
import os
import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

from bookingmodel import BookingModel
from roommodel import RoomModel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class AddRoom(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

        if user:
            main_header = 'Please Add GPU Information Below'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)

        else:
            main_header = 'Please Login to Access This Page..!!'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)

        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user
        }
        template = JINJA_ENVIRONMENT.get_template('addRoom.html')
        self.response.write(template.render(template_values))

    def post(self):
        print("Post method of booking")
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        error_message = ''

        if user:
            main_header = 'Please Add Room Information Below'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            user_given_room_name = self.request.get("room_name")
            my_model_key = ndb.Key('RoomModel', user_given_room_name)
            my_room = my_model_key.get()
            if my_room:
                error_message = 'Room Already exists ! Please use add booking option for booking'
            else:
                my_room = RoomModel(id=user_given_room_name)
                my_room.roomName = user_given_room_name
                my_room.createdBy = user.email()
                my_room.put()
                self.redirect('/')

        else:
            main_header = 'Please Login to Access This Page..!!'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)
        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user,
            'error_message': error_message
        }
        template = JINJA_ENVIRONMENT.get_template('addRoom.html')
        self.response.write(template.render(template_values))


class AddBooking(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        error_message = ''
        user_given_room_name = self.request.get("room_name")

        if user:
            main_header = 'Please Add Room Information Below'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)

            page_id = self.request.get("page_id")
            if page_id == "addBooking":
                user_given_room_name = self.request.get("room_name")
                user_room_key = ndb.Key('RoomModel', user_given_room_name)
                room_ndb_object = user_room_key.get()
                existing_bookings = room_ndb_object.booking
                date_time_format = "%Y-%m-%dT%H:%M"
                # Read user inputs
                new_start_date = self.request.get("startDate")
                new_start_time = self.request.get("startTime")
                new_end_date = self.request.get("endDate")
                new_end_time = self.request.get("endTime")
                new_booking_id = self.request.get("bookingId")
                # Convert user input to date format
                new_start_date_time = datetime.datetime.strptime(new_start_date + "T" + new_start_time,
                                                                 date_time_format)
                new_end_date_time = datetime.datetime.strptime(new_end_date+"T"+new_end_time, date_time_format)
                add_booking_flag = True
                print(new_start_date_time)
                print(new_end_date_time)
                if new_start_date_time >= new_end_date_time:  # Check for start date and time
                    add_booking_flag = False
                    error_message = "Start Time should always be greater than End Time"
                if add_booking_flag and (new_start_date_time < datetime.datetime.now()):  # Check for past Bookings
                    add_booking_flag = False
                    error_message = "No past bookings allowed"
                # Check for add_booking_flag which will be false if any of above conditions are true.!
                if add_booking_flag is True:
                    for each_booking in existing_bookings:
                        existing_start_date_time = each_booking.startTime
                        existing_end_date_time = each_booking.endTime
                        existing_booking_id = each_booking.bookingId
                        if existing_booking_id == new_booking_id:
                            add_booking_flag = False
                            error_message = "Please select unique Booking id. Booking already exists"
                            break
                        if new_start_date_time <= existing_end_date_time and \
                                new_end_date_time >= existing_start_date_time:
                            add_booking_flag = False
                            error_message = "Booking Overlaps, " \
                                            "Please view bookings and make new non-overlapping booking"
                            break
                if add_booking_flag:
                    new_booking = BookingModel(startTime=new_start_date_time,
                                               endTime=new_end_date_time,
                                               bookingId=new_booking_id,
                                               userCreated=user.email()
                                               )  # type: BookingModel
                    room_ndb_object.booking.append(new_booking)
                    room_ndb_object.put()
                    self.redirect('/')

        else:
            main_header = 'Please Login to Access This Page..!!'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)
        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user,
            'error_message': error_message,
            'room_name': user_given_room_name
        }
        template = JINJA_ENVIRONMENT.get_template('addBooking.html')
        self.response.write(template.render(template_values))
