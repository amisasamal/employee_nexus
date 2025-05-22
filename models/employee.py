import pymysql
from flask import current_app

def get_connection():
    """Establish a database connection using configuration from the app"""
    return pymysql.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASS'],
        database=current_app.config['DB_NAME']
    )

def submit_data(data):
    """Insert a new employee record into the database"""
    conn = get_connection()
    my_cursor = conn.cursor()
    try:
        query = """
            INSERT INTO employee_details (
                employee_id, salutation, first_name, middle_name, last_name, 
                date_of_birth, joined_on, post, mobile_number, email_id, password
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['employee_id'], data['salutation'], data['first_name'], 
            data['middle_name'], data['last_name'], data['date_of_birth'], 
            data['joined_on'], data['post'], data['mobile_number'], 
            data['email_id'], data['password']
        )
        my_cursor.execute(query, values)
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Error while interacting with the database:", e)
        raise
    finally:
        my_cursor.close()
        conn.close()

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
        my_cursor.execute(
            "UPDATE employee_details SET password = %s WHERE email_id = %s", 
            (hashed_password, email)
        )
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Error updating password:", e)
        raise
    finally:     
        my_cursor.close()
        conn.close()

def get_all_employees():
    """Retrieve all employees from the database"""
    conn = get_connection()
    my_cursor = conn.cursor()
    try:
        my_cursor.execute("SELECT * FROM employee_details ORDER BY first_name, last_name")
        rows = my_cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in my_cursor.description]
            employees = [dict(zip(columns, row)) for row in rows]
            return employees
        return []
    finally:
        my_cursor.close()
        conn.close()