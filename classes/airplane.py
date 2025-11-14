class Airplane:
    def __init__(self,id, name, model, seatsQuantity, maxDistance):
        self.id = id
        self.name = name
        self.model = model
        self.seatsQuantity = seatsQuantity
        self.maxDistance = maxDistance

    def __str__(self):
        return f"{self.name} {self.model}, quantity of seats: {self.seatsQuantity}, max distance: {self.maxDistance} km"

    def showInformation(self):
        print(f"{self.name} {self.model}, quantity of seats: {self.seatsQuantity}, max distance: {self.maxDistance} km")
        