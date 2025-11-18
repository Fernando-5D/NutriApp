# aviso nutrimental (azucares o sales altas en alimentos, productos o recetas)
import requests
from datetime import datetime, date
from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for, session
app = Flask(__name__)

app.config["SECRET_KEY"] = "nutrishelfporfavortreviñonecesitoexcentar"
usuarios = {}

params = {
    "apiKey": "cdea8d91f93441d8a0332ff3ad59725d"
}

hoy = date.today()
nutridatoDiario = {
    "texto": None,
    "fecha": None
}

@app.route("/")
def inicio():    
    if session.get("correo"):
        if nutridatoDiario["fecha"] != hoy:
            trivia = requests.get("https://api.spoonacular.com/food/trivia/random", params=params)
            if trivia.status_code == 200:
                trivia = trivia.json()
                nutridatoDiario["texto"] = trivia["text"]
                nutridatoDiario["fecha"] = hoy
                
        cumple = False
        fechaNacim = datetime.strptime(session.get("fechaNacim"), '%Y-%m-%d').date()
        if hoy.month == fechaNacim.month and hoy.day == fechaNacim.day:
            cumple = True
            
        return render_template("inicio.html", nutridato=nutridatoDiario["texto"], cumple=cumple)
    else:
        return render_template("intro.html")
    
@app.route("/perfil")
def perfil():
    nombre = session.get("nombre")
    genero = session.get("genero")
    fechaNacim = datetime.strptime(session.get("fechaNacim"), "%Y-%m-%d").date().strftime("%d-%B-%Y")
    peso = session.get("peso")
    altura = session.get("altura")
    correo = session.get("correo")
    actFisica = session.get("actFisica")
    
    meses = {
        "January": "Enero",
        "February": "Febrero",
        "March": "Marzo",
        "April": "Abril",
        "May": "Mayo",
        "June": "Junio",
        "July": "Julio",
        "August": "Agosto",
        "September": "Septiembre",
        "October": "Octubre",
        "November": "Noviembre",
        "December": "Diciembre"
    }
    
    fechaNacim = fechaNacim.split("-")
    fechaNacim[1] = meses[fechaNacim[1]]
    fechaNacim = " de ".join(fechaNacim)
        
    if actFisica == "1.2":
        actFisica = "Sedentario (Nada)"
    elif actFisica == "1.375":
        actFisica = "Actividad Ligera"
    elif actFisica == "1.55":
        actFisica = "Actividad Moderada"
    elif actFisica == "1.725":
        actFisica = "Actividad Alta"
    
    if genero == "5":
        genero = "Hombre"
    elif genero == "-161":
        genero = "Mujer"

    return render_template("perfil.html", nombre = nombre,  genero = genero, fechaNacim=fechaNacim , peso=peso, altura=altura, correo = correo, actFisica=actFisica)

@app.route("/editarPerfil")
def editarPerfil():
    if not session.get("correo"):
        return redirect(url_for("sesion"))

    return render_template("editarPerfil.html", nombre=session["nombre"], correo=session["correo"], genero=session["genero"], fechaNacim=session["fechaNacim"],peso=session["peso"], altura=session["altura"],actFisica=session["actFisica"])

@app.route("/guardarCambiosPerfil", methods = ("GET", "POST"))
def guardarCambiosPerfil():  
    if request.method == "POST":
        correo = session.get("correo")

        nombre = request.form.get("nombre")
        genero = request.form.get("genero")
        fechaNacim = datetime.strptime(request.form["fechaNacim"], '%Y-%m-%d').date()
        peso = request.form.get("peso")
        altura = request.form.get("altura")
        actFisica = request.form.get("actFisica")

        usuarios[correo]["nombre"] = nombre
        usuarios[correo]["genero"] = genero
        usuarios[correo]["fechaNacim"] = str(fechaNacim)
        usuarios[correo]["peso"] = peso
        usuarios[correo]["altura"] = altura
        usuarios[correo]["actFisica"] = actFisica

        session["nombre"] = nombre
        session["genero"] = genero
        session["fechaNacim"] = str(fechaNacim)
        session["peso"] = peso
        session["altura"] = altura
        session["actFisica"] = actFisica

        flash("Cambios guardados exitosamente", "success")
        return redirect(url_for("perfil"))

@app.route("/eliminarCuenta", methods = ("GET", "POST"))
def eliminarCuenta():
    correo = session.get("correo")
    if not correo:
        return redirect(url_for("sesion"))

    if correo in usuarios:
        del usuarios[correo]
    session.clear()

    flash("Tu cuenta ha sido eliminada exitosamente.", "success")
    return redirect(url_for("sesion"))



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
                session["fechaNacim"] = str(usuarios[correo]["fechaNacim"])
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
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        correo = request.form.get("correo")
        passw = request.form.get("passw")
        passwC = request.form.get("passwC")
        
        if fechaNacim > hoy:
            error.append("La fecha no puede ser futura")
        
        if not actFisica:
            error.append("Selecciona tu nivel de actividad fisica")
        
        if peso <= 0:
            error.append("El peso no puede ser menor a 1kg")
            
        if altura <= 0:
            error.append("La altura no puede ser menor a 1cm")
        
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
                "fechaNacim": str(fechaNacim),
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
