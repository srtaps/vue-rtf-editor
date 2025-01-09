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
    password='root',
    database='vebprojekat',
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
@app.route("/register", methods=['POST'])
def register():
    try:
        data = request.get_json()

        firstName = data['firstName']
        lastName = data['lastName']
        email = data['email'].lower().strip()
        password = data['password']
        
        hashed_password = generate_password_hash(password)
        cursor.execute(
            '''
            INSERT INTO users (first_name, last_name, email, password_hash)
            VALUES (%s, %s, %s, %s)
            ''', 
            (firstName, lastName, email, hashed_password)
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

# Login user route
@app.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email'].lower().strip()
        password = data['password']
        
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        print(user)
        
        if user and check_password_hash(user['password_hash'], password):
            access_token = create_access_token(
                identity=email,
                # additional_claims={
                #     # Claims will be added when the schema is more structured
                # }
            )
            
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token
            }), 200
        else:
            return jsonify({
                'error': 'Invalid email or password'
            }), 401
            
    except KeyError as e:
        return jsonify({
            'error': f'Missing required field: {str(e)}'
        }), 400

if __name__ == '__main__':
    app.run(debug=True)