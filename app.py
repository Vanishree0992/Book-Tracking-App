from flask import Flask
from config import Config
from extensions import db, login_manager, migrate
from routes import app as main_app  # importing the Flask app instance from routes

def create_app():
    app = main_app  # use the app defined in routes.py

    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
