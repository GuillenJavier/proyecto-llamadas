from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

app = Flask(__name__)

# Inicializa Firebase
cred = credentials.Certificate("firebase-credenciales.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://callmanager-79f04-default-rtdb.firebaseio.com/'  # ← Reemplaza por tu URL de Firebase
})

@app.route("/", methods=["GET"])
def index():
    ref = db.reference("llamadas")
    llamadas = ref.get() or {}
    return render_template("index.html", llamadas=llamadas)

@app.route("/actualizar", methods=["POST"])
def actualizar():
    ref = db.reference("llamadas")
    llamadas = ref.get() or {}

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
        ref.child(key).update(actualizacion)

    return redirect("/")

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

if __name__ == "__main__":
    app.run(debug=True)
