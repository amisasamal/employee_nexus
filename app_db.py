import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

def submit_data(data):
    conn=get_connection()
    my_cursor=conn.cursor()
    try:
        query="""
            INSERT INTO employee_details (employee_id,salutation,first_name,middle_name,last_name,date_of_birth,joined_on,post,mobile_number,email_id,password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = ( data['employee_id'], data['salutation'], data['first_name'], data['middle_name'], data['last_name'], data['date_of_birth'], data['joined_on'], 
                data['post'], data['mobile_number'], data['email_id'], data['password']
        )
        my_cursor.execute(query,values)
        conn.commit()
    except pymysql.MySQLError as e:
        print("Error while interacting with the database:", e)
    finally:
        # Ensure the cursor and connection are always closed, even if there is an error    
        my_cursor.close()
        conn.close()

def get_user_by_email(email):
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
    conn = get_connection()
    my_cursor = conn.cursor()
    try:
        my_cursor.execute("UPDATE employee_details SET password = %s WHERE email_id = %s", (hashed_password, email))
        conn.commit()
    except pymysql.MySQLError as e:
        print("Error updating password:", e)   
    finally:     
        my_cursor.close()
        conn.close()    