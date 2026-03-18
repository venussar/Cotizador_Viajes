class Quote:
#Solo representa una cotización como objeto en memoria
    def __init__(self, id, round_trip_distance_km, tolls_value,
                 incentive_value, hotel_cost, commission_percentage,
                 vehicle_id, user_id, created_at):

        self.id = id
        self.round_trip_distance_km = round_trip_distance_km
        self.tolls_value = tolls_value
        self.incentive_value = incentive_value
        self.hotel_cost = hotel_cost
        self.commission_percentage = commission_percentage
        self.vehicle_id = vehicle_id
        self.user_id = user_id
        self.created_at = created_at
