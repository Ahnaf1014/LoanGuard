from flask import Flask
from database.connection import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    try:
        conn = get_connection()
        conn.close()
        return "<h1>✅ LoanGuard Database Connected Successfully</h1>"

    except Exception as e:
        return f"<h1>❌ Database Connection Failed</h1><br>{e}"


if __name__ == "__main__":
    app.run(debug=True)