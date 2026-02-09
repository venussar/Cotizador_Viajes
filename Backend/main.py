from flask import Flask, request
from supabase_client import supabase

app = Flask(__name__)

@app.route("/probar-supabase", methods=["GET"])
def probar_supabase():
    response = supabase.table("cotizaciones").select("*").execute()
    return {
        "resultado": response.data
    }

if __name__ == "__main__":
    app.run(debug=True)

    from cotizador import calcular_cotizacion

@app.route("/cotizar", methods=["POST"])
def cotizar():
    datos = request.json
    vehiculo_id = datos.get("vehiculo_id")

    vehiculo_resp = supabase.table("vehiculos").select("*").eq("id", vehiculo_id).single().execute()
    vehiculo = vehiculo_resp.data

    resultado = calcular_cotizacion(datos, vehiculo)

    supabase.table("cotizaciones").insert({
        "distancia": datos.get("distancia"),
        "dias": datos.get("dias"),
        "peajes": datos.get("peajes"),
        "hotel": datos.get("hotel"),
        "cantidad_conductores": datos.get("cantidad_conductores"),
        "aplica_incentivo": datos.get("aplica_incentivo"),

        "vehiculo_nombre": resultado["vehiculo_nombre"],
        "consumo_km_usado": resultado["consumo_km_usado"],
        "costo_dia_vehiculo_usado": resultado["costo_dia_vehiculo_usado"],
        "precio_combustible_usado": resultado["precio_combustible_usado"],

        "subtotal_proveedor": resultado["subtotal_proveedor"],
        "comision": resultado["comision"],
        "total_cliente": resultado["total_cliente"]
    }).execute()

    return {
        "resultado": resultado
    }


