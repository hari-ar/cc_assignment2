import webapp2
import jinja2
import os
import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
from model import RoomModel,BookingModel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Search(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        error_message = ''
        room_data = []
        if user:
            main_header = 'Search for bookings by Date'
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
            'user': user,
            'room_list': room_data,
            'error_message': error_message
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        error_message = ''

        if user:
            main_header = 'Search for bookings by Date'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            date_time_format = "%Y-%m-%d"
            # Read user inputs
            search_date_string = self.request.get("date")
            search_date = datetime.datetime.strptime(search_date_string, date_time_format).date()
            total_data = RoomModel.query().fetch()
            room_data = []
            for each_room in total_data:
                booking_data = []
                for each_booking in each_room.booking:
                    start_date = each_booking.startTime.date()
                    end_date = each_booking.endTime.date()
                    if start_date == search_date:  # Matching date for start date.
                        booking_data.append(each_booking)
                    elif end_date == search_date:  # Matching date for end date.
                        booking_data.append(each_booking)
                    # Matching date for booking if date is in between two dates.
                    elif (start_date <= search_date) and (end_date >= search_date):
                        booking_data.append(each_booking)
                if len(booking_data) > 0:
                    my_room = each_room
                    my_room.booking = booking_data
                    room_data.append(my_room)
            if len(room_data) == 0:  # If no bookings are matched, return the user error message.
                error_message = 'No Bookings found on date : '+search_date_string.strftime(date_time_format)

        else:
            main_header = 'Please Login to Access This Page..!!'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)
        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user,
            'room_list': room_data,
            'error_message': error_message
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))
