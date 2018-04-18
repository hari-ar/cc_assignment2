from google.appengine.ext import ndb


class BookingModel(ndb.Model):
    bookingId = ndb.StringProperty()
    startTime = ndb.DateTimeProperty()
    endTime = ndb.DateTimeProperty()
    userCreated = ndb.StringProperty()


class RoomModel(ndb.Model):
    roomName = ndb.StringProperty()
    booking = ndb.StructuredProperty(BookingModel, repeated=True)
    createdBy = ndb.StringProperty()

