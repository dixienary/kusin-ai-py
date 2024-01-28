import bcrypt
from mysql.connector import Error

def create_user(conn, email, password, confirm_password):
    if password != confirm_password:
        return "Passwords do not match"

    # Check if email already exists
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return "Email already exists. Please use a different email."
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, hashed_password))
        conn.commit()
        return "User created successfully"
    except Error as e:
        return f"Error creating user: {e}"
    finally:
        cursor.close()

def login_user(conn, email, password):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        if not result:
            return "Account does not exist"
        
        stored_password = result[0]
        # Ensure stored_password is in bytes
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return "Login successful"
        else:
            return "Wrong password or email"
    except Error as e:
        return f"Error during login: {e}"
    finally:
        cursor.close()

