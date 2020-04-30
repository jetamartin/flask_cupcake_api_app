"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, redirect, render_template, flash 
from secrets import API_SECRET_KEY
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = API_SECRET_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# GET /api/cupcakes
  # Get data about all cupcakes.
  # Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
  # The values should come from each cupcake instance.

@app.route('/api/cupcakes')
def list_cupcakes():
  """Get and return list of all cupcakes in JSON  """
  all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
  return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
  """ Find cupcake with matching id """
  matching_cupcake = Cupcake.query.get_or_404(id).serialize()
  return jsonify(cupcake = matching_cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
  """ Create a new cupcake """
  new_cupcake = Cupcake(flavor = request.json['flavor'], size = request.json['size'], 
                rating = request.json['rating'], image = request.json['image'])
  db.session.add(new_cupcake)
  db.session.commit() 
  response_json = jsonify(cupcake = new_cupcake.serialize())            
  return (response_json, 201)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
  """Update a cupcake """
  cupcake = Cupcake.query.get_or_404(id)
  cupcake.flavor = request.json.get("flavor",cupcake.flavor)
  cupcake.size = request.json.get('size', cupcake.size)
  cupcake.rating = request.json.get('rating', cupcake.rating)
  cupcake.image = request.json.get('image', cupcake.image)
  db.session.commit()
  return jsonify(cupcake = cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
  """ Delete cupcake """
  cupcake = Cupcake.query.get_or_404(id)
  db.session.delete(cupcake)
  db.session.commit()
  return jsonify(message="delete")

