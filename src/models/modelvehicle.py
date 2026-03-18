from .entities.vehicle import Vehicle

class ModelVehicle:

    @staticmethod #Significa que el método no necesita usar self ni cls.
    def get_all(db):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT id, type_vehicles, fuel_consumption_km, driver_cost, labor_cost
                FROM vehicles
            """
            cursor.execute(sql)
            rows = cursor.fetchall() # Trae todos los resultados

            vehicles = []
            for row in rows:
                vehicle = Vehicle(    #crea un objeto 
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
                vehicles.append(vehicle)

            return vehicles

        except Exception as ex:
            raise ex


    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT id, type_vehicles, fuel_consumption_km, driver_cost, labor_cost
                FROM vehicles
                WHERE id = %s  #filtra por id
            """
            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row is not None:
                return Vehicle(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
            else:
                return None

        except Exception as ex:
            raise ex

    @staticmethod
    def create(db, data):
        try:
            cursor = db.connection.cursor()
            sql = """
                INSERT INTO vehicles (type_vehicles, fuel_consumption_km, driver_cost, labor_cost)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data["type_vehicles"],
                data["fuel_consumption_km"],
                data["driver_cost"],
                data["labor_cost"]
            ))
            db.connection.commit()
        except Exception as ex:
            raise ex

    @staticmethod
    def update(db, id, data):
        try:
            cursor = db.connection.cursor()
            sql = """
                UPDATE vehicles
                SET type_vehicles = %s,
                    fuel_consumption_km = %s,
                    driver_cost = %s,
                    labor_cost = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                data["type_vehicles"],
                data["fuel_consumption_km"],
                data["driver_cost"],
                data["labor_cost"],
                id
            ))
            db.connection.commit()
        except Exception as ex:
            raise ex

    @staticmethod
    def delete(db, id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM vehicles WHERE id = %s"
            cursor.execute(sql, (id,))
            db.connection.commit()
        except Exception as ex:
            raise ex
