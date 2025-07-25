from flask import Flask, render_template, request, redirect, session
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave-secreta-para-session'  # Necesaria para usar sesiones (recordar área seleccionada)

# Inicializa Firebase con credenciales y URL de la base de datos
cred = credentials.Certificate("firebase-credenciales.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://callmanager-79f04-default-rtdb.firebaseio.com/'
})

@app.route("/", methods=["GET"])
def index():
    # Referencias a llamadas y áreas
    llamadas_ref = db.reference("llamadas")
    areas_ref = db.reference("areas")

    # Obtener llamadas y áreas desde Firebase
    llamadas = llamadas_ref.get() or {}
    areas = areas_ref.get() or {}

    # Obtener el área predeterminada desde la sesión (si no, usar "Sistemas")
    area_predeterminada = session.get("area_predeterminada", "Sistemas")

    # Renderizar la plantilla HTML con los datos
    return render_template("index.html", llamadas=llamadas, areas=areas, area_predeterminada=area_predeterminada)

@app.route("/agregar", methods=["POST"])
def agregar():
    ref = db.reference("llamadas")

    # Obtener el área seleccionada del formulario
    area_seleccionada = request.form["area"]

    # Construir los datos de la nueva llamada
    datos_nueva_llamada = {
        "numero": request.form["numero"],
        "nombre": request.form.get("nombre", "Ciudadano"),  # Valor por defecto "Ciudadano"
        "lugar": request.form["lugar"],
        "duracion": request.form["duracion"],
        "area": area_seleccionada,
        "transferida": request.form["transferida"],
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Guardar la llamada en Firebase
    ref.push(datos_nueva_llamada)

    # Guardar el área seleccionada en la sesión para uso futuro
    session["area_predeterminada"] = area_seleccionada

    return redirect("/")

@app.route("/actualizar", methods=["POST"])
def actualizar():
    llamadas_ref = db.reference("llamadas")
    llamadas = llamadas_ref.get() or {}

    # Recorrer todas las llamadas y actualizarlas con los datos del formulario
    for key in llamadas:
        actualizacion = {
            "numero": request.form.get(f"numero_{key}"),
            "nombre": request.form.get(f"nombre_{key}"),
            "lugar": request.form.get(f"lugar_{key}"),
            "duracion": request.form.get(f"duracion_{key}"),
            "area": request.form.get(f"area_{key}"),
            "transferida": request.form.get(f"transferida_{key}"),
            "fecha_hora": request.form.get(f"fecha_hora_{key}")
        }
        llamadas_ref.child(key).update(actualizacion)

    return redirect("/")

@app.route("/agregar_area", methods=["POST"])
def agregar_area():
    nueva_area = request.form.get("nueva_area", "").strip()
    if nueva_area:
        areas_ref = db.reference("areas")
        areas_ref.push(nueva_area)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
