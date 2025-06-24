# db_models/base_db.py
import pymysql
from flask import current_app

def get_connection():
    """Establish a database connection using configuration from the app"""
    connection = pymysql.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASS'],
        database=current_app.config['DB_NAME'],
        port=current_app.config['DB_PORT'],
    )

    try:
        # Set timezone to Indian Standard Time
        cursor = connection.cursor()
        cursor.execute("SET time_zone = '+05:30'")
        cursor.close()
    except Exception as e:
        print(f"Warning: Could not set timezone: {e}")
    
    return connection