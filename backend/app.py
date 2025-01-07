from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

@app.get("/")
def home():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(debug=True)