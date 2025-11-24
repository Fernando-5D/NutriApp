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
    
@app.route("/calcs")
def calcs():
    return render_template("calcs.html")

@app.route("/calcs/calIMC")
def calIMC():
    return render_template("calIMC.html")

@app.route("/calcs/calIdeal")
def calIdeal():
    return render_template("calIdeal.html")

@app.route("/resultIdeal", methods = ("GET", "POST"))
def resultIdeal():
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        genero = request.form.get("genero")

        if genero == 5:
           peso = (altura - 100) - (altura-150)/4
        else:
           peso = (altura - 100) - (altura-150)/2.5
    
        
    return render_template("calIdeal.html",pesIdeal=peso)

@app.route("/resultIMC", methods = ("GET", "POST"))
def resultIMC():
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        IMC=round(peso / (altura * altura), 1)

        if IMC<18.5:
            clasificacion="Bajo peso"
            return render_template("calIMC.html",clasificacion=clasificacion, IMC=IMC)
        elif 18.5 <= IMC <= 24.9:
            clasificacion="Peso Saludable"
            return render_template("calIMC.html",clasificacion=clasificacion, IMC=IMC)
        elif 25.0 <= IMC <= 29.9:
            clasificacion="Sobre Peso"
            return render_template("calIMC.html",clasificacion=clasificacion, IMC=IMC)
        elif 30.0 <= IMC <= 39.9:
            clasificacion="Obesidad"
            return render_template("calIMC.html",clasificacion=clasificacion, IMC=IMC)
    
    return render_template("calIMC.html",clasificacion=clasificacion, IMC=IMC)

@app.route("/calcs/calcTmb")
def calcTmb():
    if session.get("correo"):
        peso = session.get("peso")
        altura = session.get("altura")
        fechaNacim = datetime.strptime(session.get("fechaNacim"), "%Y-%m-%d").date()
        genero = session.get("genero")
        
        edad = hoy.year - fechaNacim.year
        if (hoy.month, hoy.day) < (fechaNacim.month, fechaNacim.day):
            edad -= 1
        
        return render_template("calcTmb.html", peso=peso, altura=altura, edad=edad, genero=genero)
    return render_template("calcTmb.html")

@app.route("/calcs/calcTmb/result", methods = ("GET", "POST"))
def resultTmb():
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        edad = float(request.form.get("edad"))
        genero = float(request.form.get("genero"))
            
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + genero
        return render_template("resultTmb.html", tmb=tmb)
    
@app.route("/calcs/calcGct")
def calcGct():
    if session.get("correo"):
        peso = session.get("peso")
        altura = session.get("altura")
        fechaNacim = datetime.strptime(session.get("fechaNacim"), "%Y-%m-%d").date()
        genero = session.get("genero")
        actFisica = session.get("actFisica")
        
        edad = hoy.year - fechaNacim.year
        if (hoy.month, hoy.day) < (fechaNacim.month, fechaNacim.day):
            edad -= 1
        
        return render_template("calcGct.html", peso=peso, altura=altura, edad=edad, genero=genero, actFisica=actFisica)
    return render_template("calcGct.html")

@app.route("/calcs/calcGct/result", methods = ("GET", "POST"))
def resultGct():
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        edad = float(request.form.get("edad"))
        genero = float(request.form.get("genero"))
        actFisica = request.form.get("actFisica")
        
        if actFisica == None:
            flash("Selecciona tu nivel de actividad fisica", "danger")
            return render_template("calcGct.html", peso=peso, altura=altura, edad=edad, genero=genero, actFisica=actFisica)
        else:     
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + genero
            gct = tmb * float(actFisica)
            return render_template("resultGct.html", gct=gct)

@app.route("/calcs/calcMacros")
def calcMacros():
    return render_template("calcMacros.html")

@app.route("/calcs/calcMacros/result", methods = ("GET", "POST"))
def resultMacros():
    error = []
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        edad = float(request.form.get("edad"))
        genero = float(request.form.get("genero"))
        actFisica = request.form.get("actFisica")
        proteinas = float(request.form.get("proteinas"))
        grasas = float(request.form.get("grasas"))
        carbs = float(request.form.get("carbs"))
        
        if actFisica == None:
            flash("Selecciona tu nivel de actividad fisica", "danger")
            
        if proteinas + grasas + carbs != 100:
            error.append("La suma de los porcentajes de macronutrientes debe ser igual a 100%")
        
        if error:
            for err in error:
                flash(err, "danger")
            return render_template("calcMacros.html", peso=peso, altura=altura, edad=edad, genero=genero, actFisica=actFisica)
        else:     
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + genero
            gct = tmb * float(actFisica)
            proteinas = round((gct * (proteinas / 100)) / 4, 1)
            grasas = round((gct * (grasas / 100)) / 4, 1)
            carbs = round((gct * (carbs / 100)) / 9, 1)
            return render_template("resultMacros.html", proteinas=proteinas, grasas=grasas, carbs=carbs)
    
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

@app.route("/perfil/editar")
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

