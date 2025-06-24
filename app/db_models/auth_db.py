import pymysql
from .base_db import get_connection

def get_user_by_email(email):
    """Retrieve user data by email address"""
    conn = get_connection()  
    my_cursor = conn.cursor() 
    try:
        my_cursor.execute("SELECT * FROM employee_details WHERE email_id = %s", (email,))
        row = my_cursor.fetchone() 
        if row:
            columns = [desc[0] for desc in my_cursor.description]
            user = dict(zip(columns, row)) 
            return user
        return None
    finally:
        my_cursor.close()
        conn.close()

def update_password(email, hashed_password):
    """Update a user's password"""
    conn = get_connection()
    my_cursor = conn.cursor()
    try:
        result = my_cursor.execute(
            "UPDATE employee_details SET password = %s WHERE email_id = %s",
            (hashed_password, email)
        )
        conn.commit()
        print(f"Rows affected: {my_cursor.rowcount}")  # Debug line
        return True
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Error updating password:", e)
        return False
    finally:
        my_cursor.close()
        conn.close()