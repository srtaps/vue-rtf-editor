import pymysql.cursors
from pymysql import IntegrityError
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

# Set up Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'n96zyydqxo09m7xs9c5ot2r828w52zs9' # Change for production
jwt = JWTManager(app)

# Allow requests from Vue
CORS(app)

@app.get("/")
def home():
    return "Hello, world!"

# Register user route
@app.get("/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data['email'].lower().strip()
        password = data['password']
        # Additional columns will be added once the database schema is more structured
        
        hashed_password = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (email, password) VALUES (%s, %s)',
            (email, hashed_password)
        )
        connection.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    except KeyError as e:
        # If ['value'] doesn't exist in data
        return jsonify({
            'error': f'Missing required field: {str(e)}'
        }), 400
        
    except IntegrityError:
        return jsonify({'error': 'Email already registered'}), 409

if __name__ == '__main__':
    app.run(debug=True)