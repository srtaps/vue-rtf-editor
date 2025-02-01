import pymysql.cursors
from pymysql import IntegrityError
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required
from functools import wraps
from datetime import timedelta

# Create new DB connection
def get_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='vebprojekat',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection, connection.cursor()

app = Flask(__name__)

# Set up Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'n96zyydqxo09m7xs9c5ot2r828w52zs9' # Change for production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=6)
jwt = JWTManager(app)

# Allow requests from Vue
CORS(app)

# Decorator for admin-only routes
def role_required(allowed_roles):
    def wrapper(fn):
        @jwt_required()
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')
            if not user_role or user_role not in allowed_roles:
                return jsonify({'error': 'Not Authorized'}), 403
           
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# Register user route
@app.route("/register", methods=['POST'])
def register():
    connection, cursor = get_db()
    try:
        data = request.get_json()

        firstName = data['firstName']
        lastName = data['lastName']
        email = data['email'].lower().strip()
        password = data['password']
        
        hashed_password = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, password_hash)
            VALUES (%s, %s, %s, %s)
        """, 
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
    
    finally:
        cursor.close()
        connection.close()

# Login user route
@app.route("/login", methods=['POST'])
def login():
    connection, cursor = get_db()
    try:
        data = request.get_json()
        email = data['email'].lower().strip()
        password = data['password']
        
        cursor.execute("""
            SELECT users.*, roles.role_name as role_name 
            FROM users 
            JOIN roles ON users.role_id = roles.role_id 
            WHERE users.email = %s
        """, (email,))
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
    
    finally:
        cursor.close()
        connection.close()

# Get users
@app.route('/users', methods=['GET'])
@role_required(['Admin'])
def get_users():
    connection, cursor = get_db()
    try:
        cursor.execute("""
            SELECT u.user_id, u.full_name, u.email, u.created_at, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.role_id
        """)
        users = cursor.fetchall()
        
        return jsonify(users)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()
    
# Get individual user
@app.route('/users/<int:user_id>', methods=['GET'])
@role_required(['Admin'])
def get_user(user_id):
    connection, cursor = get_db()
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
    
    finally:
        cursor.close()
        connection.close()

# Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
@role_required(['Admin'])
def update_user(user_id):
    connection, cursor = get_db()
    try:
        data = request.json

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({'message': 'User not found.'}), 404
        
        cursor.execute("""
            UPDATE users 
            SET first_name = %s,
                last_name = %s,
                email = %s,
                role_id = %s
            WHERE user_id = %s
        """, (
            data['first_name'],
            data['last_name'],
            data['email'],
            data['role_id'],
            user_id
        ))
        
        connection.commit()

        return jsonify({'message': 'User has been updated.'})
    
    except KeyError as e:
        return jsonify({
            'error': f'Missing required field: {str(e)}'
        }), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Delete user
@app.route('/users/<int:user_id>', methods=['DELETE'])
@role_required(['Admin'])
def delete_user(user_id):
    connection, cursor = get_db()
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        
        if user is None:
            return jsonify({'message': 'User not found.'}), 404

        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        connection.commit()

        return jsonify({'message': 'User has been deleted.'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Get roles
@app.route('/roles', methods=['GET'])
@role_required(['Admin'])
def get_roles():
    connection, cursor = get_db()
    try:
        cursor.execute("SELECT role_id, role_name FROM roles ORDER BY role_id")
        roles = cursor.fetchall()

        return jsonify(roles)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Get courses
@app.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    connection, cursor = get_db()
    try:
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        return jsonify(courses)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Get individual course
@app.route('/courses/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    connection, cursor = get_db()
    try:
        cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
        
        course = cursor.fetchone()
        if not course:
            return jsonify({'error': 'Course not found'}), 404
            
        return jsonify(course)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Add course
@app.route('/courses', methods=['POST'])
@role_required(['Admin'])
def add_course():
    connection, cursor = get_db()
    try:
        data = request.get_json()

        title = data['title']
        info = data['info']
        professor = data['professor']

        cursor.execute("""
            INSERT INTO courses (title, info, professor)
            VALUES (%s, %s, %s)
        """, 
            (title, info, professor)
        )
        connection.commit()
        
        return jsonify({'message': 'Course added successfully'}), 201

    except KeyError as e:
        return jsonify({
            'error': f'Missing required field: {str(e)}'
        }), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Update course
@app.route('/courses/<int:course_id>', methods=['PUT'])
@role_required(['Admin'])
def update_course(course_id):
    connection, cursor = get_db()
    try:
        data = request.json

        cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
        course = cursor.fetchone()

        if course is None:
            return jsonify({'message': 'Course not found.'}), 404
        
        cursor.execute("""
            UPDATE courses 
            SET title = %s,
                info = %s,
                professor = %s
            WHERE course_id = %s
        """, (
            data['title'],
            data['info'],
            data['professor'],
            course_id
        ))
        
        connection.commit()

        return jsonify({'message': 'Course has been updated.'})
    
    except KeyError as e:
        return jsonify({
            'error': f'Missing required field: {str(e)}'
        }), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Delete course
@app.route('/courses/<int:course_id>', methods=['DELETE'])
@role_required(['Admin'])
def delete_course(course_id):
    connection, cursor = get_db()
    try:
        cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
        course = cursor.fetchone()
        
        if course is None:
            return jsonify({'message': 'Course not found.'}), 404

        cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
        connection.commit()

        return jsonify({'message': 'Course has been deleted.'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Get lessons
@app.route('/lessons', methods=['GET'])
@jwt_required()
def get_lessons():
    connection, cursor = get_db()
    try:
        cursor.execute("""
            SELECT 
                lessons.lesson_id, lessons.title, lessons.content, 
                courses.title AS course_title
            FROM lessons 
            LEFT JOIN courses ON lessons.course_id = courses.course_id
        """)
        lessons = cursor.fetchall()

        return jsonify(lessons)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Get lessons tied to one course
@app.route('/course/<int:course_id>/lessons', methods=['GET'])
@jwt_required()
def get_course_lessons(course_id):
    connection, cursor = get_db()
    try:
        cursor.execute("""
            SELECT title, content FROM lessons 
            WHERE course_id = %s
        """, (course_id,))
        lessons = cursor.fetchall()

        return jsonify(lessons)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Get individual lesson
@app.route('/lessons/<int:lesson_id>', methods=['GET'])
@jwt_required()
def get_lesson(lesson_id):
    connection, cursor = get_db()
    try:
        cursor.execute("""
            SELECT * FROM lessons 
            WHERE lesson_id = %s
        """, (lesson_id,))
        lesson = cursor.fetchone()

        if not lesson:
            return jsonify({'error': 'Course not found'}), 404

        return jsonify(lesson)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Add lesson
@app.route('/lessons', methods=['POST'])
@role_required(['Admin'])
def add_lesson():
    connection, cursor = get_db()
    try:
        data = request.get_json()

        title = data['title']
        content = data['content']
        course_id = data['course_id']

        cursor.execute("""
            INSERT INTO lessons (title, content, course_id)
            VALUES (%s, %s, %s)
        """, 
            (title, content, course_id)
        )
        connection.commit()
        
        return jsonify({'message': 'Lesson added successfully'}), 201

    except KeyError as e:
        return jsonify({
            'error': f'Missing required field: {str(e)}'
        }), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Update lesson
@app.route('/lessons/<int:lesson_id>', methods=['PUT'])
@role_required(['Admin'])
def update_lesson(lesson_id):
    connection, cursor = get_db()
    try:
        data = request.json

        cursor.execute("SELECT * FROM lessons WHERE lesson_id = %s", (lesson_id,))
        lesson = cursor.fetchone()

        if lesson is None:
            return jsonify({'message': 'Lesson not found.'}), 404
        
        cursor.execute("""
            UPDATE lessons 
            SET title = %s,
                content = %s,
                course_id = %s
            WHERE lesson_id = %s
        """, (
            data['title'],
            data['content'],
            data['course_id'],
            lesson_id
        ))
        
        connection.commit()

        return jsonify({'message': 'Lesson has been updated.'})
    
    except KeyError as e:
        return jsonify({
            'error': f'Missing required field: {str(e)}'
        }), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# Delete lesson
@app.route('/lessons/<int:lesson_id>', methods=['DELETE'])
@role_required(['Admin'])
def delete_lesson(lesson_id):
    connection, cursor = get_db()
    try:
        cursor.execute("SELECT * FROM lessons WHERE lesson_id = %s", (lesson_id,))
        lesson = cursor.fetchone()
        
        if lesson is None:
            return jsonify({'message': 'Lesson not found.'}), 404

        cursor.execute("DELETE FROM lessons WHERE lesson_id = %s", (lesson_id,))
        connection.commit()

        return jsonify({'message': 'Lesson has been deleted.'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)