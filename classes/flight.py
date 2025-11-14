class Flight:
    def __init__(self, id ,airplane, origin, destination, distance, duration, ticketPrice, points):
        self.id = id
        self.airplane = airplane #object of airplane
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.duration = duration  #in hours
        self.ticketPrice = ticketPrice
        self.points = points

    def __str__(self):
        return (f"Flight {self.origin} -> {self.destination}, distance: {self.distance} km, duration: {self.duration} h, \nprice: {self.ticketPrice}, points: {self.points}, airplane: {self.airplane.name} {self.airplane.model}")
        
    def ShowInformation(self):
        print((f"Flight {self.origin} -> {self.destination}, distance: {self.distance} km, duration: {self.duration} h, \nprice: {self.ticketPrice}, points: {self.points}, airplane: {self.airplane.name} {self.airplane.model}"))
        