import webapp2
import jinja2
import os

from google.appengine.api import users
from model import RoomModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Download(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        error_message = ''

        # User Authentication.
        if user:
            self.response.headers['Content-Type'] = 'text/csv'  # Responsible for file
            # File name is set to info.csv
            self.response.headers['Content-Disposition'] = "attachment; filename=info.csv"
            # Header in csv
            self.response.out.write(','.join(['Room Id', 'Room Created By', 'Booking Id',
                                              'Booking Start Date Time', 'Booking End Date Time',
                                              'Booked By']))
            self.response.out.write('\n')
            total_data = RoomModel.query().fetch()
            date_time_format = "%Y-%m-%d %H:%M"
            for each_room in total_data:
                for each_booking in each_room.booking:
                    self.response.out.write(','.join([each_room.roomName, each_room.createdBy, each_booking.bookingId,
                                                      each_booking.startTime.strftime(date_time_format),
                                                      each_booking.endTime.strftime(date_time_format),
                                                      each_booking.userCreated]))
                    self.response.out.write('\n')
        else:
            main_header = 'Please Login to Access This Page..!!'
            room_data = []
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)
            self.response.headers['Content-Type'] = 'text/html'
            template_values = {
                'main_header': main_header,
                'login_logout': login_logout,
                'login_logout_url': login_logout_url,
                'user': user,
                'room_list': room_data,
                'error_message': error_message
            }
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
