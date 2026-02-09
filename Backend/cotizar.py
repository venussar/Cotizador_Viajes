def calcular_cotizacion(datos, vehiculo): #datos los envia el usuario, vehiculo los envia supabase  
    distancia = datos.get("distancia", 0)
    dias = datos.get("dias", 1)
    peajes = datos.get("peajes", 0)
    hotel = datos.get("hotel", 0)
    cantidad_conductores = datos.get("cantidad_conductores", 1)
    aplica_incentivo = datos.get("aplica_incentivo", False)

    consumo_km = vehiculo["consumo_km"]
    costo_dia = vehiculo["costo_dia"]
    precio_combustible = 15000
    incentivo = 50000 if aplica_incentivo else 0

    costo_combustible = distancia * consumo_km * precio_combustible
    costo_vehiculo = costo_dia * dias
    costo_conductores = cantidad_conductores * 100000 * dias

    subtotal = (
        costo_combustible +
        costo_vehiculo +
        costo_conductores +
        peajes +
        hotel +
        incentivo
    )

    comision = subtotal * 0.15
    total_cliente = subtotal + comision

    return {
        "vehiculo_nombre": vehiculo["nombre"],
        "consumo_km_usado": consumo_km,
        "costo_dia_vehiculo_usado": costo_dia,
        "precio_combustible_usado": precio_combustible,
        "subtotal_proveedor": subtotal,
        "comision": comision,
        "total_cliente": total_cliente
    }
