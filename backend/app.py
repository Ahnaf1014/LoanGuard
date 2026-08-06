from flask import Flask
from routes.borrower import borrower_bp
from routes.application import application_bp
from routes.dashboard import dashboard_bp
from config import Config

app = Flask(__name__)


app.config["SECRET_KEY"] = Config.SECRET_KEY
app.register_blueprint(borrower_bp)
app.register_blueprint(application_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
