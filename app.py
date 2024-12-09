from flask import Flask, render_template, request, session, redirect, url_for, flash
import random
import hashlib
import time  # Para medir el tiempo de minado

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Necesario para usar sesiones
cambio_sesion = 1  # Variable global para manejar la sesión

# Función para simular el precio del Bitcoin
def obtener_precio_bitcoin():
    return round(random.uniform(20000, 60000), 2)

# Función que maneja la compra de bitcoins
def comprar_bitcoin(dinero_a_gastar):
    dinero = session.get('dinero', 100.0)  # Inicializar el dinero si no está en la sesión
    bitcoins = session.get('bitcoins', 0.0)  # Obtener bitcoins de la sesión
    precio_bitcoin = obtener_precio_bitcoin()  # Obtener precio actual de bitcoin

    # Verificar si el usuario tiene suficiente dinero
    if dinero_a_gastar <= dinero:
        # Calcular la cantidad de bitcoins que puede comprar
        cantidad_bitcoins = dinero_a_gastar / precio_bitcoin
        # Actualizar dinero y bitcoins
        dinero -= dinero_a_gastar
        bitcoins += cantidad_bitcoins
        # Guardar los valores actualizados en la sesión
        session['dinero'] = dinero
        session['bitcoins'] = bitcoins
        session['precio_bitcoin'] = precio_bitcoin
        return True, dinero, bitcoins, precio_bitcoin
    return False, dinero, bitcoins, precio_bitcoin

@app.route('/', methods=['GET', 'POST'])
def index():
    global cambio_sesion

    # Inicializar la sesión solo la primera vez que se accede
    if cambio_sesion == 1:
        session.clear()  # Borra todos los valores de la sesión (aseguramos que no haya persistencia)
        session['dinero'] = 100.0  # Establecer el dinero a 100$
        session['bitcoins'] = 0.0  # Establecer los bitcoins a 0
        session['sesion_iniciada'] = True  # Marcar que la sesión ha sido iniciada
        cambio_sesion += 1

    # Obtener dinero, bitcoins y precio desde la sesión
    dinero = session['dinero']
    bitcoins = session['bitcoins']
    precio_bitcoin = obtener_precio_bitcoin()  # Obtener el precio actual de bitcoin

    mensaje = ""  # Variable para el mensaje de éxito o error

    # Si se recibe una solicitud POST (se presionó el botón)
    if request.method == 'POST':
        try:
            dinero_a_gastar = float(request.form['cantidad'])  # Cantidad de dinero a gastar
        except ValueError:
            dinero_a_gastar = 0.0

        # Llamar a la función para procesar la compra
        exito, dinero, bitcoins, precio_bitcoin = comprar_bitcoin(dinero_a_gastar)

        # Mensaje de éxito o error
        if exito:
            mensaje = f"¡Compra realizada con éxito! Has comprado {dinero_a_gastar / precio_bitcoin:.7f} BTC."
            session['mensaje'] = mensaje  # Guardar el mensaje en la sesión
        else:
            mensaje = "No tienes suficiente dinero para realizar esta compra."
            session['mensaje'] = mensaje  # Guardar el mensaje en la sesión

        # Guardar los valores actualizados en la sesión
        session['dinero'] = dinero
        session['bitcoins'] = bitcoins
        session['precio_bitcoin'] = precio_bitcoin

        # Redirigir al mismo lugar con una solicitud GET
        return redirect(url_for('index'))

    # Datos para el gráfico (simulación de precios históricos)
    precios_simulados = [20000, 25000, 22000, 27000, 30000]
    tiempos = [1, 2, 3, 4, 5]

    # Obtener el mensaje de la sesión
    mensaje = session.get('mensaje', "")

    return render_template(
        'index.html',
        dinero=dinero,
        bitcoins=bitcoins,
        precio_bitcoin=precio_bitcoin,
        precios_simulados=precios_simulados,
        tiempos=tiempos,
        mensaje=mensaje  # Pasar el mensaje al template
    )
import time  # Para medir el tiempo de minado

@app.route('/minar', methods=['GET', 'POST'])
def minar():
    # Obtener dinero y bitcoins desde la sesión
    dinero = session.get('dinero', 100.0)  # Valor predeterminado
    bitcoins = session.get('bitcoins', 0.0)  # Valor predeterminado

    # Simulamos el bloque con 2 transacciones
    transacciones = [
        {
            "comprador": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "vendedor": "1EzWVfHKZnqYmQjd2AfCvVG83s7G5Q6hsA",
            "cantidad": 0.005,
            "precio": 45000,
            "hash": hashlib.sha256("Compra de 0.005 BTC a $45000".encode()).hexdigest()
        },
        {
            "comprador": "1LuvQ4cDyoq64MvfDT98ZX9jwFFdRTedA3",
            "vendedor": "1Zxg1cd7TbVfe2uCkswhLNwHRRfhhA7d58",
            "cantidad": 0.010,
            "precio": 46000,
            "hash": hashlib.sha256("Compra de 0.010 BTC a $46000".encode()).hexdigest()
        }
    ]

    # Simulamos el bloque como la concatenación de las transacciones
    bloque_data = ''.join([f"{tx['comprador']} {tx['vendedor']} {tx['cantidad']} BTC {tx['precio']} USD" for tx in transacciones])

    # Dificultad del bloque (valor objetivo)
    dificultad = 2**240  # Target para el hash válido (muy sencillo)
    bloque_data = ''.join([f"{tx['comprador']} {tx['vendedor']} {tx['cantidad']} BTC {tx['precio']} USD" for tx in transacciones])
    hash_bloque = hashlib.sha256(bloque_data.encode()).hexdigest()  # Hash del bloque
    intentos = 0

    # Solo ejecutar el minado si el usuario pulsa el botón
    if request.method == 'POST' and 'iniciar_minado' in request.form:
        nonce = 0  # Inicializar el nonce
        intentos = 0
        inicio = time.time()  # Iniciar medición del tiempo

        # Intentar encontrar un hash válido
        while True:
            intentos += 1
            datos_a_hashear = f"{bloque_data}{nonce}"  # Añadimos el nonce al bloque
            hash_bloque = hashlib.sha256(datos_a_hashear.encode()).hexdigest()  # Calculamos el hash
            if int(hash_bloque, 16) <= dificultad:  # Convertimos el hash a entero y lo comparamos con la dificultad
                break  # Hash válido encontrado
            nonce += 1  # Incrementamos el nonce para el siguiente intento

        fin = time.time()  # Terminar medición del tiempo
        tiempo_minado = round(fin - inicio, 2)  # Tiempo en segundos

        # Mensaje para el frontend
        session['mensaje_minado'] = f"¡Bloque minado con éxito en {intentos} intentos y {tiempo_minado} segundos!"

    # Obtener el mensaje de la sesión (si lo hay)
    mensaje_minado = session.pop('mensaje_minado', None)

    # Pasar todos los datos al template
    return render_template(
        'minar.html',
        transacciones=transacciones,
        hash_bloque=hash_bloque,
        dificultad=dificultad,
        intentos=intentos,
        mensaje_minado=mensaje_minado,
        dinero=dinero,
        bitcoins=bitcoins
    )


@app.route('/vender')
def vender():
    return render_template('vender.html', mensaje="Esta es la página para vender bitcoins.")

if __name__ == "__main__":
    app.run(debug=True)
