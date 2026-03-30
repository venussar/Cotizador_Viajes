from .entities.quote import Quote

class ModelQuote:

    @staticmethod
    def get_all_by_user(db, user_id):
        try:
            cursor = db.connection.cursor() #canal para hablar con la base de datos
            sql = """
                SELECT q.id, q.round_trip_distance_km, q.tolls_value,
                       q.incentive_value, q.hotel_cost, q.commission_percentage,
                       q.vehicle_id, q.user_id, q.created_at,
                       q.fuel_price, q.subtotal, q.commission_value, q.total,
                       v.type_vehicles, u.namee
                FROM quotes q
                LEFT JOIN vehicles v ON q.vehicle_id = v.id
                LEFT JOIN users u ON q.user_id = u.id
                WHERE q.user_id = %s
                ORDER BY q.created_at DESC
            """
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()

            quotes = []
            for row in rows:
                quote = Quote(*row)
                quotes.append(quote)

            return quotes

        except Exception as ex:
            raise ex


    @staticmethod
    def create(db, data):
        try:
            cursor = db.connection.cursor()
            sql = """
                INSERT INTO quotes (
                    round_trip_distance_km,
                    tolls_value,
                    incentive_value,
                    hotel_cost,
                    commission_percentage,
                    vehicle_id,
                    user_id,
                    fuel_price,
                    subtotal,
                    commission_value,
                    total
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                data["round_trip_distance_km"],
                data["tolls_value"],
                data["incentive_value"],
                data["hotel_cost"],
                data["commission_percentage"],
                data["vehicle_id"],
                data["user_id"],
                data["fuel_price"],
                data["subtotal"],
                data["commission_value"],
                data["total"]
            ))

            db.connection.commit()

        except Exception as ex:
            raise ex
