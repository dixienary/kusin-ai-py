# user_management.py

import bcrypt
from flask import request, jsonify

def create_user(email, password):
    cursor = conn.cursor()

    # Hash the password before storing it in the database
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        # Insert user details into the 'users' table
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                       (email, password_hash))
        conn.commit()
        return jsonify({'success': True, 'message': 'User created successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()

def login_user(email, password):
    cursor = conn.cursor()

    try:
        # Retrieve hashed password from the database based on the provided email
        cursor.execute("SELECT user_id, password_hash FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()

        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1].encode('utf-8')):
            # Successful login
            return jsonify({'success': True, 'user_id': user_data[0], 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
