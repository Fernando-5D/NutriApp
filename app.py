# aviso nutrimental (azucares o sales altas en alimentos, productos o recetas)
import requests
from flask import Flask, render_template
app = Flask(__name__)

apiKey = "4988525657d749cd88a7104290c42ed0"
@app.route("/")
def inicio():
    url_randomRecipes = "https://api.spoonacular.com/recipes/random?includeNutrition=false"
    recetas = requests.get(url_randomRecipes, params = {"apiKey": apiKey, "number": 5}).json()
    return render_template("inicio.html", recetas=recetas)

if __name__ == "__main__":
    app.run(debug=True)
