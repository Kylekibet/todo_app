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

import os

from dotenv import load_dotenv
from flask import Flask

from extensions import bootstrap, login_manager
from models import User, db
from routes.auth import auth_bp
from routes.pages import pages_bp

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

database_url = os.environ.get('DATABASE_URL')

if not database_url:
    if os.environ.get('VERCEL'):          # Vercel sets this automatically
        raise RuntimeError('DATABASE_URL is not set in Vercel environment variables')
    database_url = 'sqlite:///users.db'   # local development only

# SQLAlchemy needs the driver name in the URL
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql+psycopg://', 1)
elif database_url.startswith('postgresql://'):
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True, 'pool_recycle': 300}

bootstrap.init_app(app)
db.init_app(app)
login_manager.init_app(app)

# creates tables if they do not exist
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(pages_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5100)

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

