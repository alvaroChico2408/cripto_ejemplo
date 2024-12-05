from flask import Flask, render_template, request, session, redirect, url_for, flash
import random

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

@app.route('/minar')
def minar():
    return render_template('minar.html', mensaje="Esta es la página para minar bitcoins.")

@app.route('/vender')
def vender():
    return render_template('vender.html', mensaje="Esta es la página para vender bitcoins.")

if __name__ == "__main__":
    app.run(debug=True)
