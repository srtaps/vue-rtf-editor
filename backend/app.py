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
        
        cursor.execute('''
            SELECT users.*, roles.role_name as role_name 
            FROM users 
            JOIN roles ON users.role_id = roles.role_id 
            WHERE users.email = %s
        ''', (email,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            access_token = create_access_token(
                identity=email,
                additional_claims={
                    'user_id': user['user_id'],
                    'role': user['role_name']
                }
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

# Get users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        cursor.execute("""
            SELECT u.user_id, u.full_name, u.email, u.created_at, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.role_id
        """)
        users = cursor.fetchall()
        connection.commit()
        
        return jsonify(users)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Get individual user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        cursor.execute("""
            SELECT u.user_id, u.first_name, u.last_name, 
                   u.email, u.role_id, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.role_id
            WHERE u.user_id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify(user)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)