import os
from flask import Flask
from views import auth_bp, post_bp, team_bp, message_bp
from flask_migrate import Migrate
from models import db
from flask_jwt_extended import JWTManager  
import os 
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'njhgvfdcdrtyujhgcdrtyujhgcxdfghjkjbv'  
app.config['JWT_TOKEN_LOCATION'] = ['headers']  

# Initialize Extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)  

# Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(post_bp, url_prefix='/posts')
app.register_blueprint(team_bp, url_prefix='/teams')
app.register_blueprint(message_bp, url_prefix='/messages')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
