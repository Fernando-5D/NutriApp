# aviso nutrimental (azucares o sales altas en alimentos, productos o recetas)
from datetime import datetime, date
from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for, session
app = Flask(__name__)

app.config["SECRET_KEY"] = "nutrishelfporfavortrevinecesitoexcentar"
usuarios = {}

@app.route("/")
def inicio():  
    if session.get("correo"):
        return render_template("inicio.html")
    else:
        return render_template("intro.html")
    
@app.route("/perfil")
def perfil():
    nombre = session["nombre"]
    correo = session["correo"]
    genero = session["genero"]
    fechaNacim = session["fechaNacim"]
    actFisica = session["actFisica"]
    edad = session["edad"]
    peso = session["peso"]
    altura = session["altura"]
    correo = session["correo"]
    return render_template("perfil.html", nombre = nombre, correo = correo, genero = genero, fechaNacim=fechaNacim , actFisica=actFisica , edad= edad , peso=peso, altura=altura, correo = correo)

@app.route("/guardarCambiosPerfil")
def guardarCambiosPerfil():  
    return

@app.route("/cerrarSes")
def cerrarSes():
    session.clear()  
    return redirect(url_for("sesion"))  

@app.route("/sesion")
def sesion():  
    return render_template("sesion.html")

@app.route("/iniciandoSesion", methods = ("GET", "POST"))
def iniciandoSesion():
    if request.method == "POST":
        correo = request.form.get("correo")
        if correo in usuarios:
            passw = request.form.get("passw")
            if passw == usuarios[correo]["passw"]:
                session["nombre"] = usuarios[correo]["nombre"]
                session["genero"] = usuarios[correo]["genero"]
                session["fechaNacim"] = usuarios[correo]["fechaNacim"]
                session["edad"] = usuarios[correo]["edad"]
                session["actFisica"] = usuarios[correo]["actFisica"]
                session["peso"] = usuarios[correo]["peso"]
                session["altura"] = usuarios[correo]["altura"]
                session["correo"] = usuarios[correo]["correo"]
                session["passw"] = usuarios[correo]["passw"]
            else:
                flash("La contraseña es incorrecta", "danger")
        else:
            flash("No se encontro el usuario, ingresaste el correo correctamente?", "danger")
        
        if get_flashed_messages():
            return render_template("sesion.html")
        else:
            return redirect(url_for("inicio"))

@app.route("/registro")
def registro():  
    return render_template("registro.html")

@app.route('/registrando', methods = ("GET", "POST"))
def registrando():
    error = []
    if request.method == "POST":
        nombre = request.form.get("nombre")
        genero = request.form.get("genero")
        fechaNacim = datetime.strptime(request.form["fechaNacim"], '%Y-%m-%d').date()
        actFisica = request.form.get("actFisica")
        peso = request.form.get("peso")
        altura = request.form.get("altura")
        correo = request.form.get("correo")
        passw = request.form.get("passw")
        passwC = request.form.get("passwC")
        
        hoy = date.today()
        edad = None
        if fechaNacim <= hoy:
            edad = hoy.year - fechaNacim.year
            if hoy.day < fechaNacim.day and hoy.month < fechaNacim.month:
                edad -= 1
        else:
            error.append("La fecha no puede ser futura")
        
        if not actFisica:
            error.append("Selecciona tu nivel de actividad fisica")
        
        if usuarios.get(correo):
            error.append("El correo ingresado ya esta siendo usado por otra cuenta")
        
        if passwC != passw:
            error.append("La confirmacion de la contraseña no coincide")

        if error:
            for err in error:
                flash(err, "danger")
            return render_template("registro.html")
        else:
            usuarios[correo] = {
                "nombre": nombre,
                "genero": genero,
                "fechaNacim": fechaNacim,
                "edad": edad,
                "actFisica": actFisica,
                "peso": peso,
                "altura": altura,
                "correo": correo,
                "passw": passw
            }

            flash(f"Registrado con exito: {correo}", "success")
            return redirect(url_for("sesion"))

if __name__ == "__main__":
    app.run(debug=True)


