from flask import Flask
from routes.borrower import borrower_bp

app = Flask(__name__)

app.register_blueprint(borrower_bp)


@app.route("/")
def home():
    return """
    <h1>LoanGuard</h1>

    <a href="/borrowers">
        Borrower Management
    </a>
    """


if __name__ == "__main__":
    app.run(debug=True)