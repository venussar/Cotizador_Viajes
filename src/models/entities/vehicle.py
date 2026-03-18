class Vehicle:
# representa un vehiculo como objeto en memoria
    def __init__(self, id, type_vehicles, fuel_consumption_km, driver_cost, labor_cost):
        self.id = id
        self.type_vehicles = type_vehicles
        self.fuel_consumption_km = fuel_consumption_km
        self.driver_cost = driver_cost
        self.labor_cost = labor_cost
