from google.appengine.ext import ndb
from bookingmodel import BookingModel


class RoomModel(ndb.Model):
    roomName = ndb.StringProperty()
    booking = ndb.StructuredProperty(BookingModel, repeated=True)
    createdBy = ndb.StringProperty()
