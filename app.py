# aviso nutrimental (azucares o sales altas en alimentos, productos o recetas)
from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for, session
app = Flask(__name__)

usuarios = {}

@app.route("/")
def inicio():  
    return render_template("intro.html")

@app.route("/sesion")
def sesion():  
    return render_template("sesion.html")

@app.route("/iniciandoSesion", methods = ("GET", "POST"))
def iniciandoSesion():
    if request.method == "POST":
        correo = request.form.get("correo")
        if correo in usuarios:
            passw = request.form.get("passw")
            if passw == usuarios[correo].passw:
                session["nombre"] = usuarios[correo].nombre
                session["fechaNacim"] = usuarios[correo].fechaNacim
                session["genero"] = usuarios[correo].genero
                session["peso"] = usuarios[correo].peso
                session["altura"] = usuarios[correo].altura
                session["actFisica"] = usuarios[correo].actFisica
                session["correo"] = usuarios[correo].correo
                session["passw"] = usuarios[correo].passw
            else:
                flash("La contraseña es incorrecta.")
        else:
            flash("No se encontro el usuario, ingresaste el correo correctamente?")
        
        if get_flashed_messages():
            return redirect(url_for("sesion"))
        else:
            return render_template("inicio.html")

@app.route("/registro")
def registro():  
    return render_template("registro.html")

@app.route("/registrando")
def registrando():  
    return

if __name__ == "__main__":
    app.run(debug=True)
