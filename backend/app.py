from flask import Flask
from routes.borrower import borrower_bp
from routes.application import application_bp

app = Flask(__name__)

app.register_blueprint(borrower_bp)
app.register_blueprint(application_bp)


@app.route("/")
def home():
    return """
    <h1>LoanGuard</h1>

    <ul>
        <li>
            <a href="/borrowers">
                Borrowers
            </a>
        </li>

        <li>
            <a href="/applications">
                Loan Applications
            </a>
        </li>
    </ul>
    """


if __name__ == "__main__":
    app.run(debug=True)
