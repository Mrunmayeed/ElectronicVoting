# app.py
from flask import Flask
from flask_session import Session
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.judge_controller import judge_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(judge_bp)

if __name__ == "__main__":
    app.run(debug=True)
