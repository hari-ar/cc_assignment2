import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from roommodel import RoomModel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class DeleteRoom(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        error_message = ''

        if user:
            main_header = 'Rooms Information'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            room_list = RoomModel.query().fetch()
            user_given_room_name = self.request.get("room_name")
            user_room_key = ndb.Key('RoomModel', user_given_room_name)
            room_ndb_object = user_room_key.get()
            existing_bookings = room_ndb_object.booking
            if len(existing_bookings) == 0:
                room_ndb_object.key.delete()
                error_message = "Room is deleted, please click on home to see updated info."
            else:
                error_message = "Warning : Rooms which have bookings, can not be deleted. Please delete bookings first."
        else:
            main_header = 'Please Login to Access This Page..!!'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)
        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user,
            'room_list': room_list,
            'error_message': error_message
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class DeleteBooking(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        error_message = ''

        if user:
            main_header = 'Rooms Information'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            room_list = RoomModel.query().fetch()
            user_given_room_name = self.request.get("room_name")
            user_room_key = ndb.Key('RoomModel', user_given_room_name)
            room_ndb_object = user_room_key.get()
            new_booking_id = self.request.get("bookingId")
            print("Booking id")
            print(new_booking_id)
            existing_bookings = room_ndb_object.booking
            for each_booking in existing_bookings:
                if each_booking.bookingId == new_booking_id:
                    room_ndb_object.booking.remove(each_booking)
                    room_ndb_object.put()
                    break

        else:
            main_header = 'Please Login to Access This Page..!!'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)
        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user,
            'room_list': room_list,
            'error_message': error_message
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))