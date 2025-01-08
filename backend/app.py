import pymysql.cursors
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required

# Connection to database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='your_db_name',
    cursorclass=pymysql.cursors.DictCursor
)

# Create the cursor, keep it open
cursor = connection.cursor()

app = Flask(__name__)

# Allow requests from Vue
CORS(app)

@app.get("/")
def home():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(debug=True)