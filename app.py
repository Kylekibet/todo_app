from flask import Flask
from extensions import bootstrap, login_manager
from routes.pages import pages_bp
from routes.auth import auth_bp
import os
from dotenv import load_dotenv
from models import db, User

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///to-do.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to-do.db'

bootstrap.init_app(app)
db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()
    print("Tables created.")
    
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))



# Blueprints
app.register_blueprint(pages_bp)
app.register_blueprint(auth_bp)


if __name__ == '__main__':
    app.run()

