import pymysql
import pymysql.cursors
from werkzeug.security import generate_password_hash

# Database connection settings
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'

# Test data
test_users = [
    ('John', 'Doe', 'admin1@example.com', 'Password123456', 'Admin'),
    ('Jane', 'Smith', 'admin2@example.com', 'Password123456', 'Admin'),
    ('Emily', 'Brown', 'admin3@example.com', 'Password123456', 'Admin'),
    ('John', 'Doe', 'user1@example.com', 'Password123456', 'User'),
    ('Jane', 'Smith', 'user2@example.com', 'Password123456', 'User'),
    ('Emily', 'Brown', 'user3@example.com', 'Password123456', 'User')
]

lessons_data = [
    # For Course 1 - Introduction to Computer Science (course_id = 1)
    ('Introduction to Programming', 'Learn the basics of programming with Python.', 1),
    ('Variables and Data Types', 'Understanding variables, data types, and basic operations in Python.', 1),
    ('Control Flow and Loops', 'Introduction to conditional statements and loops in Python.', 1),
    ('Functions and Modules', 'Learn how to create functions and import Python modules.', 1),

    # For Course 2 - Advanced Mathematics (course_id = 2)
    ('Complex Numbers and Their Operations', 'An introduction to complex numbers and operations like addition and multiplication.', 2),
    ('Differentiation Techniques', 'Learn advanced techniques in differentiation and applications.', 2),
    ('Integration and Its Applications', 'Understand the methods of integration and its use in real-world problems.', 2),
    ('Abstract Algebra Basics', 'Explore the fundamentals of abstract algebra, including groups and rings.', 2),

    # For Course 3 - World History (course_id = 3)
    ('Ancient Civilizations', 'Study the major ancient civilizations, including Egypt, Mesopotamia, and the Indus Valley.', 3),
    ('The Rise and Fall of Rome', 'Learn about the Roman Empire and its eventual decline.', 3),
    ('The Middle Ages', 'A look at the feudal system, the role of the Church, and major historical events during the Middle Ages.', 3),
    ('The Renaissance and Enlightenment', 'Explore the cultural movements of the Renaissance and the intellectual advancements of the Enlightenment.', 3),

    # For Course 4 - Organic Chemistry (course_id = 4)
    ('Introduction to Organic Compounds', 'Learn about the structure and properties of organic compounds.', 4),
    ('Functional Groups and Reactions', 'Understand different functional groups and their reaction mechanisms.', 4),
    ('Isomerism in Organic Chemistry', 'Study the concept of isomerism and its importance in organic compounds.', 4),
    ('Synthesis of Organic Molecules', 'Learn how to synthesize complex organic molecules through different chemical reactions.', 4),

    # For Course 5 - Literature Analysis (course_id = 5)
    ('Introduction to Literary Analysis', 'Learn how to analyze and interpret literary works from various genres.', 5),
    ('Themes in Classic Literature', 'Study recurring themes in classic literature, such as love, betrayal, and redemption.', 5),
    ('Character Development and Motivation', 'Analyze the development of characters and their motivations in famous literary works.', 5),
    ('Literary Devices and Their Effects', 'Explore various literary devices like metaphors, symbolism, and irony, and how they affect storytelling.', 5)
]

def create_connection():
    """Create and return a connection to the MySQL database."""
    return pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             cursorclass=pymysql.cursors.DictCursor)

def setup_database():
    # Establish a connection to MySQL server (without selecting a DB)
    connection = pymysql.connect(host=DB_HOST,
                                  user=DB_USER,
                                  password=DB_PASSWORD)
    try:
        with connection.cursor() as cursor:
            # Drop and create the database
            cursor.execute("DROP DATABASE IF EXISTS vebprojekat")
            cursor.execute("CREATE DATABASE IF NOT EXISTS vebprojekat")
            cursor.execute("USE vebprojekat")
            
            # Create the tables
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                role_id INT AUTO_INCREMENT PRIMARY KEY,
                role_name VARCHAR(100) NOT NULL
            )""")
            
            # Insert roles into roles table
            cursor.execute("INSERT INTO roles (role_name) VALUES ('Admin')")
            cursor.execute("INSERT INTO roles (role_name) VALUES ('User')")
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                full_name VARCHAR(255) AS (CONCAT(first_name, ' ', last_name)) VIRTUAL,
                role_id INT,
                FOREIGN KEY (role_id) REFERENCES roles(role_id)
            )""")
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                info TEXT,
                professor VARCHAR(100)
            )""")
            
            # Insert courses into courses table
            cursor.executemany("""
            INSERT INTO courses (course_id, title, info, professor) VALUES (%s, %s, %s, %s)
            """, [
                (1, 'Introduction to Computer Science', 'Fundamentals of programming and computational thinking', 'Dr. Smith'),
                (2, 'Advanced Mathematics', 'Complex analysis and abstract algebra', 'Dr. Johnson'),
                (3, 'World History', 'Comprehensive study of major historical events', 'Prof. Williams'),
                (4, 'Organic Chemistry', 'Study of organic compounds and reactions', 'Dr. Brown'),
                (5, 'Literature Analysis', 'Critical analysis of classical literature', 'Prof. Davis')
            ])
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS lessons (
                lesson_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT,
                course_id INT,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )""")
            
            # Insert lessons into lessons table
            cursor.executemany("""
            INSERT INTO lessons (title, content, course_id) VALUES (%s, %s, %s)
            """, lessons_data)

            # Add index on the email column to speed up queries
            cursor.execute("CREATE INDEX idx_email ON users(email)")

            # Add test users with hashed passwords
            for first_name, last_name, email, password, role_name in test_users:
                # Hash the password
                hashed_password = generate_password_hash(password)
                
                # Get the role_id for the role (Admin or User)
                cursor.execute("SELECT role_id FROM roles WHERE role_name = %s", (role_name,))
                result = cursor.fetchone()
                
                # Ensure the role_id exists
                if result:
                    role_id = result[0]  # Access the first element of the tuple (role_id)
                else:
                    print(f"Role '{role_name}' not found!")
                    continue
                
                # Insert user into the database with the hashed password
                cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password_hash, role_id)
                VALUES (%s, %s, %s, %s, %s)
                """, (first_name, last_name, email, hashed_password, role_id))

            # Commit changes
            connection.commit()
            print("Database and tables created, test data inserted successfully!")

    finally:
        connection.close()

# Run the setup function
if __name__ == '__main__':
    setup_database()
