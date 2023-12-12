from flask import Flask, render_template, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase    
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)

#Creamos la cadena de conexion 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokedex.sqlite"

#Vinculamos la base de datos con la app
db = SQLAlchemy(app)

#Creamos el modelo
class pokemon(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)

#con esta sentencia se crea las tablas 
with app.app_context():
    db.create_all()




def get_pokemon_data(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r = requests.get(url).json()
    return r 

@app.route("/home")
def home():
    return render_template('pokemon.html')

@app.route("/detalle")
def detalle():
    return render_template('detalle.html')

#pruebas de base de datos 
@app.route("/insert")
def insert():
    new_pokemon = 'Pikachu'
    if new_pokemon:
            obj = pokemon(name=new_pokemon)
            db.session.add(obj)
            db.session.commit()
    return 'Pokemon Agregado'

@app.route("/select")
def select():
    Lista_pokemon = pokemon.query.all()
    for p in Lista_pokemon:
        print(p.name)
    return 'alo'

@app.route("/select/<name>")
def selectbyname(name):
    poke = pokemon.query.filter_by(name=name).first()
    return str(poke.id)


if __name__ == '__main__':
    app.run(debug=True)