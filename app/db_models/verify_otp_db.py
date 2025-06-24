import pymysql
import random
from datetime import datetime, timedelta
from .base_db import get_connection

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def store_otp(email, otp_code):
    """Store OTP in database with expiration"""
    conn = get_connection()
    my_cursor = conn.cursor()
    
    try:
        # Delete any existing OTPs for this email
        my_cursor.execute("DELETE FROM password_reset_otps WHERE email = %s", (email,))
        
        # Set expiration time (10 minutes from now)
        expires_at = datetime.now() + timedelta(minutes=10)
        
        # Insert new OTP
        query = """
            INSERT INTO password_reset_otps (email, otp_code, expires_at)
            VALUES (%s, %s, %s)
        """
        my_cursor.execute(query, (email, otp_code, expires_at))
        conn.commit()
        return True
        
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Error storing OTP:", e)
        return False
    finally:
        my_cursor.close()
        conn.close()

def verify_otp(email, otp_code):
    """Verify OTP and check if it's valid"""
    conn = get_connection()
    my_cursor = conn.cursor()
    
    try:
        # Get OTP record
        query = """
            SELECT id, otp_code, expires_at, is_used, attempts 
            FROM password_reset_otps 
            WHERE email = %s AND is_used = FALSE
            ORDER BY created_at DESC LIMIT 1
        """
        my_cursor.execute(query, (email,))
        record = my_cursor.fetchone()
        
        if not record:
            return False, "No valid OTP found for this email"
        
        otp_id, stored_otp, expires_at, is_used, attempts = record
        
        # Check if OTP expired
        if datetime.now() > expires_at:
            return False, "OTP has expired. Please request a new one"
        
        # Check attempts (max 3 attempts)
        if attempts >= 3:
            return False, "Too many failed attempts. Please request a new OTP"
        
        # Check if OTP matches
        if stored_otp != otp_code:
            # Increment attempts
            my_cursor.execute(
                "UPDATE password_reset_otps SET attempts = attempts + 1 WHERE id = %s",
                (otp_id,)
            )
            conn.commit()
            return False, f"Invalid OTP. {3 - (attempts + 1)} attempts remaining"
        
        # OTP is valid - mark as used
        my_cursor.execute(
            "UPDATE password_reset_otps SET is_used = TRUE WHERE id = %s",
            (otp_id,)
        )
        conn.commit()
        return True, "OTP verified successfully"
        
    except pymysql.MySQLError as e:
        print("Error verifying OTP:", e)
        return False, "Database error occurred"
    finally:
        my_cursor.close()
        conn.close()