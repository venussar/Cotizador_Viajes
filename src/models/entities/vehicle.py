class Vehicle:
# representa un vehiculo como objeto en memoria
    def __init__(self, id, type_vehicles, fuel_consumption_km, daily_vehicle_cost):
        self.id = id
        self.type_vehicles = type_vehicles
        self.fuel_consumption_km = fuel_consumption_km
        self.daily_vehicle_cost = daily_vehicle_cost
