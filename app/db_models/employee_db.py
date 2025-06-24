import pymysql
from .base_db import get_connection

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