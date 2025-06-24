# db_models/base_db.py
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