from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager(app)

from home.home import home_bp
app.register_blueprint(home_bp)

from auth.auth import auth_bp
app.register_blueprint(auth_bp)

from tool.tool import tool_bp
app.register_blueprint(tool_bp)

if __name__ == '__main__':
    app.run()
