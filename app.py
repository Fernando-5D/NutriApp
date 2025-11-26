# NO CORRERLO, esta incompleto y da errores
# aviso nutrimental (azucares o sales altas en alimentos, productos o recetas)

import requests
from datetime import datetime, date
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for, session

app = Flask(__name__)
mysql = MySQL(app)

app.config["SECRET_KEY"] = "nutrishelfporfavortreviñonecesitoexcentar"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "usuarios"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"  

apiKey = "cdea8d91f93441d8a0332ff3ad59725d"
today = date.today()


def crear_tabla_users():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                nombre VARCHAR(100),
                genero CHAR(1),
                fechaNacim DATE,
                actFisica VARCHAR(10),
                peso FLOAT,
                altura FLOAT,
                correo VARCHAR(500) UNIQUE PRIMARY KEY,
                passw VARCHAR(500),
                passwC VARCHAR(500)

            )
        ''')
        mysql.connection.commit()
        print("Tabla 'usuarios' creada o ya existe")
    except Exception as e:
        print(f"Error creando tabla: {e}")


def email_existe(correo):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT correo FROM nutrishelf WHERE correo=%s", (correo,))
    return cursor.fetchone() is not None


def obtener_usuario_por_email(correo):
 try:
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM nutrishelf WHERE correo=%s", (correo,))
    return cursor.fetchone()  
 except Exception as e:
    print(f"Error obteniendo usuario: {e}")
    return None

def registrar_usuario(nombre, genero, fechaNacim, actFisica, peso, altura, correo, passw):
    try:
        cursor = mysql.connection.cursor()
        hashed = generate_password_hash(passw)
        cursor.execute(
            '''INSERT INTO nutrishelf(nombre, genero, fechaNacim, actFisica, peso, altura, correo, passw,passwC)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (nombre, genero, fechaNacim, actFisica, peso, altura, correo, hashed,passwC)
        )
        mysql.connection.commit()
        return True, f"Registrado con exito: {correo}"
    except Exception as e:
        if "Duplicate" in str(e):
            return False, "El correo ingresado ya esta siendo usado por otra cuenta"
        return False, f"Error al registrar usuario: {e}"


def actualizar_usuario_por_correo(correo, nombre, genero, fechaNacim, actFisica, peso, altura):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE nutrishelf
                          SET nombre=%s, genero=%s, fechaNacim=%s, actFisica=%s, peso=%s, altura=%s
                          WHERE correo=%s''',
                       (nombre, genero, fechaNacim, actFisica, peso, altura, correo))
        mysql.connection.commit()
        return True, "Cambios guardados exitosamente"
    except Exception as e:
        return False, f"Error al actualizar perfil: {e}"


def eliminar_usuario_por_correo(correo):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM nutrishelf WHERE correo=%s", (correo,))
        mysql.connection.commit()
        return True, "Tu cuenta ha sido eliminada exitosamente."
    except Exception as e:
        return False, f"Error al eliminar cuenta: {e}"

try:
    crear_tabla_users()
except:
    print("Advertencia: tabla usuarios no verificada.")


@app.route("/")
def inicio():    
    if session.get("correo"):
        # if nutridatoDiario["fecha"] != today:
            # trivia = requests.get("https://api.spoonacular.com/food/trivia/random", params={"apiKey": apiKey})
            # if trivia.status_code == 200:
                # trivia = trivia.json()
                # nutridatoDiario["texto"] = trivia["text"]
                # nutridatoDiario["fecha"] = today
                
        cumple = False
        fechaNacim = datetime.strptime(session.get("fechaNacim"), '%Y-%m-%d').date()
        if today.month == fechaNacim.month and today.day == fechaNacim.day:
            cumple = True
            
        return render_template("inicio.html", cumple=cumple)
    else:
        return render_template("intro.html")

@app.route("/calcs")
def calcs(): return render_template("calcs.html")
@app.route("/calcs/calIMC")
def calIMC(): return render_template("calIMC.html")
@app.route("/calcs/calIdeal")
def calIdeal(): return render_template("calIdeal.html")

@app.route("/resultIdeal", methods=["GET","POST"])
def resultIdeal():
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        genero = request.form.get("genero")
        if genero == 'H':
            peso = (altura - 100) - (altura - 150) / 4
        else:
            peso = (altura - 100) - (altura - 150) / 2.5
        return render_template("calIdeal.html", pesIdeal=peso)
    return render_template("calIdeal.html")

@app.route("/resultIMC", methods=["GET","POST"])
def resultIMC():
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        IMC = round(peso / (altura * altura), 1)
        if IMC < 18.5:
            clasificacion = "Bajo peso"
        elif 18.5 <= IMC <= 24.9:
            clasificacion = "Peso Saludable"
        elif 25 <= IMC <= 29.9:
            clasificacion = "Sobre Peso"
        else:
            clasificacion = "Obesidad"
        return render_template("calIMC.html", clasificacion=clasificacion, IMC=IMC)
    return render_template("calIMC.html")

@app.route("/calcs/calcTmb")
def calcTmb():
    if session.get("correo"):
        peso = session.get("peso")
        altura = session.get("altura")
        fechaNacim = datetime.strptime(session.get("fechaNacim"), '%Y-%m-%d').date()
        genero = session.get("genero")
        edad = today.year - fechaNacim.year
        if (today.month, today.day) < (fechaNacim.month, fechaNacim.day): edad -= 1
        return render_template("calcTmb.html", peso=peso, altura=altura, edad=edad, genero=genero)
    return render_template("calcTmb.html")

@app.route("/calcs/calcTmb/result", methods=["GET","POST"])
def resultTmb():
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        edad = float(request.form.get("edad"))
        genero = request.form.get("genero")
        tmb = (10*peso)+(6.25*altura)-(5*edad)+(5 if genero=='H' else -161)
        return render_template("resultTmb.html", tmb=tmb)

@app.route("/calcs/calcGct")
def calcGct():
    if session.get("correo"):
        peso = session.get("peso")
        altura = session.get("altura")
        fechaNacim = datetime.strptime(session.get("fechaNacim"), '%Y-%m-%d').date()
        genero = session.get("genero")
        actFisica = session.get("actFisica")
        edad = today.year - fechaNacim.year
        if (today.month, today.day) < (fechaNacim.month, fechaNacim.day): edad -= 1
        return render_template("calcGct.html", peso=peso, altura=altura, edad=edad, genero=genero, actFisica=actFisica)
    return render_template("calcGct.html")

@app.route("/calcs/calcGct/result", methods=["GET","POST"])
def resultGct():
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        edad = float(request.form.get("edad"))
        genero = request.form.get("genero")
        actFisica = request.form.get("actFisica")
        if not actFisica:
            flash("Selecciona tu nivel de actividad fisica", "danger")
            return render_template("calcGct.html")
        tmb = (10*peso)+(6.25*altura)-(5*edad)+(5 if genero=='H' else -161)
        gct = tmb * float(actFisica)
        return render_template("resultGct.html", gct=gct)

@app.route("/calcs/calcMacros")
def calcMacros(): return render_template("calcMacros.html")

@app.route("/calcs/calcMacros/result", methods=["GET","POST"])
def resultMacros():
    error = []
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        edad = float(request.form.get("edad"))
        genero = request.form.get("genero")
        actFisica = request.form.get("actFisica")
        proteinas = float(request.form.get("proteinas"))
        grasas = float(request.form.get("grasas"))
        carbs = float(request.form.get("carbs"))
        if proteinas + grasas + carbs != 100:
            error.append("La suma de los porcentajes de macronutrientes debe ser igual a 100%")
        if error:
            for e in error: flash(e,"danger")
            return render_template("calcMacros.html")
        tmb = (10*peso)+(6.25*altura)-(5*edad)+(5 if genero=='H' else -161)
        gct = tmb * float(actFisica)
        return render_template("resultMacros.html",
                               proteinas=round((gct*(proteinas/100))/4,1),
                               grasas=round((gct*(grasas/100))/4,1),
                               carbs=round((gct*(carbs/100))/9,1))

@app.route("/perfil")
def perfil():
    nombre = session.get("nombre")
    genero = session.get("genero")
    fecha = datetime.strptime(session.get("fechaNacim"), '%Y-%m-%d').strftime('%d-%B-%Y')
    peso = session.get("peso")
    altura = session.get("altura")
    correo = session.get("correo")
    act = session.get("actFisica")
    return render_template("perfil.html", nombre=nombre, genero=("Hombre" if genero=='H' else "Mujer"),
                           fechaNacim=fecha,peso=peso,altura=altura,correo=correo,actFisica=act)

@app.route("/perfil/editar")
def editarPerfil():
    if not session.get("correo"): return redirect(url_for("sesion"))
    return render_template("editarPerfil.html", **session)

@app.route("/guardarCambiosPerfil", methods=["GET","POST"])
def guardarCambiosPerfil():
    if request.method == "POST":
        correo = session.get("correo")
        nombre = request.form.get("nombre")
        genero = request.form.get("genero")
        fechaNacim = request.form.get("fechaNacim")
        peso = request.form.get("peso")
        altura = request.form.get("altura")
        actFisica = request.form.get("actFisica")
        ok,msg = actualizar_usuario_por_correo(correo,nombre,genero,fechaNacim,actFisica,peso,altura)
        flash(msg, "success" if ok else "danger")
        if ok:
            session.update({"nombre":nombre,"genero":genero,"fechaNacim":fechaNacim,
                            "peso":peso,"altura":altura,"actFisica":actFisica})
        return redirect(url_for("perfil"))

@app.route("/eliminarCuenta", methods=["GET","POST"])
def eliminarCuenta():
    correo = session.get("correo")
    if not correo: return redirect(url_for("sesion"))
    ok,msg = eliminar_usuario_por_correo(correo)
    flash(msg, "success" if ok else "danger")
    if ok: session.clear()
    return redirect(url_for("sesion"))

@app.route("/cerrarSes")
def cerrarSes(): session.clear(); return redirect(url_for("sesion"))

@app.route("/sesion")
def sesion(): return render_template("sesion.html")

@app.route("/iniciandoSesion", methods=["GET","POST"])
def iniciandoSesion():
    if request.method == "POST":
        correo = request.form.get("correo")
        usuario = obtener_usuario_por_email(correo)
        if usuario:
            passw = request.form.get("passw")
            if check_password_hash(usuario["passw"], passw):
                session.update({
                    "nombre": usuario["nombre"],
                    "genero": usuario["genero"],
                    "fechaNacim": str(usuario["fechaNacim"]),
                    "actFisica": usuario["actFisica"],
                    "peso": usuario["peso"],
                    "altura": usuario["altura"],
                    "correo": usuario["correo"],
                    "passw": usuario["passw"],
                    "passwC": usuario["passwC"]
                })
            else:
                flash("La contraseña es incorrecta","danger")
        else:
            flash("No se encontro el usuario","danger")
        if get_flashed_messages(): return render_template("sesion.html")
        return redirect(url_for("inicio"))

@app.route("/registro")
def registro(): return render_template("registro.html")

@app.route('/registrando', methods=["GET","POST"])
def registrando():
    error=[]
    if request.method=="POST":
        nombre=request.form.get("nombre")
        genero=request.form.get("genero")
        fechaNacim=datetime.strptime(request.form["fechaNacim"],'%Y-%m-%d').date()
        actFisica=request.form.get("actFisica")
        peso=float(request.form.get("peso"))
        altura=float(request.form.get("altura"))
        correo=request.form.get("correo")
        passw=request.form.get("passw")
        passwC=request.form.get("passwC")
        if fechaNacim>today: error.append("La fecha no puede ser futura")
        if not actFisica: error.append("Selecciona tu nivel de actividad fisica")
        if peso<=0: error.append("El peso no puede ser menor a 1kg")
        if altura<=0: error.append("La altura no puede ser menor a 1cm")
        if email_existe(correo): error.append("El correo ya esta siendo usado")
        if passw!=passwC: error.append("La confirmacion no coincide")
        if error:
            for e in error: flash(e,"danger")
            return render_template("registro.html")
        ok,msg = registrar_usuario(nombre,genero,fechaNacim,actFisica,peso,altura,correo,passw,passwC)
        flash(msg,"success" if ok else "danger")
        return redirect(url_for("sesion")) if ok else render_template("registro.html")

if __name__ == "__main__": app.run(debug=True)

