from flask import Flask

app = Flask(__name__)


@app.route("/")
def read_root():
    return {
        "message": "Flask App Demo",
        "info": "This is a simple Flask application running in Docker.",
    }


@app.route("/health")
def health_check():
    return {"status": "healthy"}

