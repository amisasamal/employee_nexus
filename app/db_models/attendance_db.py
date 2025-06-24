import pymysql
from datetime import datetime, date
from .base_db import get_connection

def clock_in_employee(employee_id):
    """Clock in an employee for today"""
    conn = get_connection()
    my_cursor = conn.cursor()

    try:
        today = date.today()
        
        # Check if already clocked in today
        my_cursor.execute(
            "SELECT id FROM attendance_records WHERE employee_id = %s AND date = %s",
            (employee_id, today)
        )
        existing = my_cursor.fetchone()
        
        if existing:
            return False, "Already clocked in today"
        
        # Insert clock in record
        query = """
            INSERT INTO attendance_records (employee_id, clock_in, date, status)
            VALUES (%s, %s, %s, 'present')
        """
        my_cursor.execute(query, (employee_id, datetime.now(), today))
        conn.commit()
        return True, "Clocked in successfully"
        
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Error clocking in:", e)
        return False, "Database error occurred"
    finally:
        my_cursor.close()
        conn.close()

def clock_out_employee(employee_id):
    """Clock out an employee for today"""
    conn = get_connection()
    my_cursor = conn.cursor()
    
    try:
        today = date.today()
        
        # Get today's attendance record
        my_cursor.execute(
            "SELECT id, clock_in, clock_out FROM attendance_records WHERE employee_id = %s AND date = %s",
            (employee_id, today)
        )
        record = my_cursor.fetchone()
        
        if not record:
            return False, "Need to clock in first"
        
        if record[2]:  # clock_out already exists
            return False, "Already clocked out today"
        
        # Update with clock out time and calculate hours
        clock_out_time = datetime.now()
        clock_in_time = record[1]
        total_hours = (clock_out_time - clock_in_time).total_seconds() / 3600
        
        query = """
            UPDATE attendance_records 
            SET clock_out = %s, total_hours = %s 
            WHERE id = %s
        """
        my_cursor.execute(query, (clock_out_time, round(total_hours, 2), record[0]))
        conn.commit()
        
        return True, f"Clocked out successfully! Total hours: {round(total_hours, 2)}"
        
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Error clocking out:", e)
        return False, "Database error occurred"
    finally:
        my_cursor.close()
        conn.close()

def get_today_attendance(employee_id):
    """Get today's attendance record for an employee"""
    conn = get_connection()
    my_cursor = conn.cursor()
    
    try:
        today = date.today()
        my_cursor.execute(
            "SELECT * FROM attendance_records WHERE employee_id = %s AND date = %s",
            (employee_id, today)
        )
        row = my_cursor.fetchone()
        
        if row:
            columns = [desc[0] for desc in my_cursor.description]
            return dict(zip(columns, row))
        return None
        
    finally:
        my_cursor.close()
        conn.close()

def get_employee_attendance_history(employee_id, limit=10):
    """Get recent attendance history for an employee"""
    conn = get_connection()
    my_cursor = conn.cursor()
    
    try:
        my_cursor.execute(
            "SELECT * FROM attendance_records WHERE employee_id = %s ORDER BY date DESC LIMIT %s",
            (employee_id, limit)
        )
        rows = my_cursor.fetchall()
        
        if rows:
            columns = [desc[0] for desc in my_cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []
        
    finally:
        my_cursor.close()
        conn.close()