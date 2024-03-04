from flask import Flask
from flask_cors import CORS
from blueprints.image import image_bp
from blueprints.category import category_bp
from blueprints.article import article_bp
from blueprints.commentaire import commentaire_bp
from blueprints.user import user_bp

# Création de l'application
app = Flask(__name__)
CORS(app)

# Enregistrement des Blueprints
app.register_blueprint(category_bp, url_prefix='/category')
app.register_blueprint(image_bp, url_prefix='/image')
app.register_blueprint(article_bp, url_prefix='/article')
app.register_blueprint(commentaire_bp, url_prefix='/commentaire')
app.register_blueprint(user_bp, url_prefix='/user')

#lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
