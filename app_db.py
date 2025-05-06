import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='amisa',
        password='3amisa3@',
        database='employee_nexus'
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


    