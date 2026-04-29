# The file that launches the database at 5000 and makes sure it's accessable by the frontend (aka API)

import os
from flask import Flask
from flask_cors import CORS
from models import db       # Vi importerer db fra vores nye models.py
from routes.product_routes import product_bp
# from flasgger import Swagger  # Do we really need swagger?


# Find den absolutte sti til mappen hvor app.py ligger (ROOT/backend/)
basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    
    # Konfiguration af database
    db_path = os.path.join(basedir, 'instance', 'inventory.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'din_hemmelige_noegle' # Skift denne i produktion

    # Tillad React (localhost:3000) at tale med Flask (localhost:5000)
    CORS(app)
    
    # # Initialiser Swagger
    # swagger = Swagger(app, template={
    #     "info": {
    #         "title": "Lagerstyring API",
    #         "description": "API dokumentation for det systemet"
    #     }
    # })

    # Initialiser databasen med appen
    db.init_app(app)

    with app.app_context():
        # Dette sikrer at mappen 'instance' findes, før vi opretter DB
        if not os.path.exists(os.path.join(basedir, 'instance')):
            os.makedirs(os.path.join(basedir, 'instance'))
        # Dette opretter .db filen og alle tabeller ud fra models.py
        db.create_all()
        print("Database og tabeller er oprettet!")

    # Her skal vi senere registrere vores Blueprints (ruter)
    app.register_blueprint(product_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
