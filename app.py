from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

app = Flask(__name__)

# Inicialización de Firebase con tus credenciales
cred = credentials.Certificate("firebase-credenciales.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://callmanager-79f04-default-rtdb.firebaseio.com/'
})

@app.route("/", methods=["GET"])
def index():
    # Referencias a llamadas y áreas en Firebase
    llamadas_ref = db.reference("llamadas")
    areas_ref = db.reference("areas")

    llamadas = llamadas_ref.get() or {}
    areas = areas_ref.get() or {}

    return render_template("index.html", llamadas=llamadas, areas=areas)

@app.route("/agregar", methods=["POST"])
def agregar():
    ref = db.reference("llamadas")
    datos_nueva_llamada = {
        "numero": request.form["numero"],
        "nombre": request.form["nombre"],
        "lugar": request.form["lugar"],
        "duracion": request.form["duracion"],
        "area": request.form["area"],
        "transferida": request.form["transferida"],
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ref.push(datos_nueva_llamada)
    return redirect("/")

@app.route("/actualizar", methods=["POST"])
def actualizar():
    llamadas_ref = db.reference("llamadas")
    llamadas = llamadas_ref.get() or {}

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
    nueva_area = request.form.get("nueva_area").strip()
    if nueva_area:
        areas_ref = db.reference("areas")
        areas_ref.push(nueva_area)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
