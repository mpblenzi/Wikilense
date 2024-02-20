from flask import Flask
#import de cors pour autoriser les requêtes cross-origin
from flask_cors import CORS
from blueprints.image import image_bp
from blueprints.category import category_bp
from blueprints.article import article_bp
from blueprints.commentaire import commentaire_bp


app = Flask(__name__)
CORS(app)

# Ici, tu configurerais l'application avec des choses comme la base de données,
# les extensions, etc.

# Enregistrement des Blueprints
app.register_blueprint(category_bp, url_prefix='/category')
app.register_blueprint(image_bp, url_prefix='/image')
app.register_blueprint(article_bp, url_prefix='/article')
app.register_blueprint(commentaire_bp, url_prefix='/commentaire')

if __name__ == "__main__":
    app.run(debug=True)
