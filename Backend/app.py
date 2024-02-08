from flask import Flask
#import de cors pour autoriser les requêtes cross-origin
from flask_cors import CORS
from blueprints.image import image_bp
from blueprints.category import category_bp


app = Flask(__name__)
CORS(app)

# Ici, tu configurerais l'application avec des choses comme la base de données,
# les extensions, etc.

# Enregistrement des Blueprints
app.register_blueprint(category_bp, url_prefix='/category')
app.register_blueprint(image_bp, url_prefix='/image')

if __name__ == "__main__":
    app.run(debug=True)
