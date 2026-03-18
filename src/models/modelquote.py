from .entities.quote import Quote

class ModelQuote:

    @staticmethod
    def get_all_by_user(db, user_id):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT id, round_trip_distance_km, tolls_value,
                       incentive_value, hotel_cost, commission_percentage,
                       vehicle_id, user_id, created_at
                FROM quotes
                WHERE user_id = %s
                ORDER BY created_at DESC
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
                    user_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s) #espacios para los valores que se van a insertar    
            """

            cursor.execute(sql, (  #Reemplaza cada %s con estos valores
                data["round_trip_distance_km"],
                data["tolls_value"],
                data["incentive_value"],
                data["hotel_cost"],
                data["commission_percentage"],
                data["vehicle_id"],
                data["user_id"]
            ))

            db.connection.commit()

        except Exception as ex:
            raise ex
