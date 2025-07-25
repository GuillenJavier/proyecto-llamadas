from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

app = Flask(__name__)

# Inicializa Firebase
cred = credentials.Certificate("firebase-credenciales.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://callmanager-79f04-default-rtdb.firebaseio.com/'
})

# Áreas predeterminadas
AREAS = ["Sistemas", "Desarrollo Urbano", "Obras Públicas", "Presidencia", "Atención Ciudadana"]

@app.route("/", methods=["GET"])
def index():
    ref = db.reference("llamadas")
    llamadas = ref.get() or {}
    return render_template("index.html", llamadas=llamadas, areas=AREAS)

@app.route("/agregar", methods=["POST"])
def agregar():
    ref = db.reference("llamadas")
    datos_nueva_llamada = {
        "numero": request.form["numero"],
        "nombre": request.form["nombre"] or "Ciudadano",
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
    ref = db.reference("llamadas")
    llamadas = ref.get() or {}

    for key in llamadas:
        nuevo_nombre = request.form.get(f"nombre_{key}")
        if nuevo_nombre:
            ref.child(key).update({"nombre": nuevo_nombre})

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
