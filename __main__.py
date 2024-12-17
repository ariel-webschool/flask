from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost:3306/taches_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy et Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modèle de la table des tâches
class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    complete = db.Column(db.Boolean, default=False)

    def __init__(self, titre, description, complete):
        self.titre = titre
        self.description = description
        self.complete = complete

# Schéma Marshmallow pour la sérialisation
class TacheSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tache
        load_instance = True

# Initialisation du schéma

tache_schema = TacheSchema()               # Pour une tâche unique
taches_schema = TacheSchema(many=True)     # Pour plusieurs tâches

# Création de la base de données (décommente pour initialiser)
# with app.app_context():
#     db.create_all()

# Route pour ajouter une tâche
@app.route('/taches', methods=['POST'])
def add_tache():
    titre = request.json['titre']
    description = request.json.get('description', '')
    complete = request.json.get('complete', False)

    nouvelle_tache = Tache(titre, description, complete)
    db.session.add(nouvelle_tache)
    db.session.commit()

    return tache_schema.jsonify(nouvelle_tache), 201

# Route pour récupérer toutes les tâches
@app.route('/taches', methods=['GET'])
def get_taches():
    toutes_les_taches = Tache.query.all()
    return taches_schema.jsonify(toutes_les_taches)

# Route pour récupérer une tâche par ID
@app.route('/taches/<int:id>', methods=['GET'])
def get_tache(id):
    tache = Tache.query.get_or_404(id)
    return tache_schema.jsonify(tache)

# Route pour mettre à jour une tâche par ID
@app.route('/taches/<int:id>', methods=['PUT'])
def update_tache(id):
    tache = Tache.query.get_or_404(id)

    titre = request.json.get('titre', tache.titre)
    description = request.json.get('description', tache.description)
    complete = request.json.get('complete', tache.complete)

    tache.titre = titre
    tache.description = description
    tache.complete = complete

    db.session.commit()
    return tache_schema.jsonify(tache)

# Route pour supprimer une tâche par ID
@app.route('/taches/<int:id>', methods=['DELETE'])
def delete_tache(id):
    tache = Tache.query.get_or_404(id)
    db.session.delete(tache)
    db.session.commit()
    return jsonify({"message": "Tâche supprimée avec succès"}), 200

# Point d'entrée principal
if __name__ == '__main__':
    app.run(debug=True)
