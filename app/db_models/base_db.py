# db_models/base_db.py
import pymysql
from flask import current_app
from datetime import datetime, timedelta
import pytz

def get_connection():
    """Establish a database connection using configuration from the app"""
    return pymysql.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASS'],
        database=current_app.config['DB_NAME'],
        port=current_app.config['DB_PORT']
    )

def get_ist_now():
    """Get current time in IST"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

def get_ist_now_naive():
    """Get current IST time as naive datetime (for MySQL storage)"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).replace(tzinfo=None)

def utc_to_ist(utc_datetime):
    """Convert UTC datetime to IST"""
    if utc_datetime is None:
        return None
    
    # If it's a naive datetime, assume it's UTC
    if utc_datetime.tzinfo is None:
        utc_datetime = pytz.utc.localize(utc_datetime)
    
    ist = pytz.timezone('Asia/Kolkata')
    return utc_datetime.astimezone(ist)

def ist_to_utc(ist_datetime):
    """Convert IST datetime to UTC"""
    if ist_datetime is None:
        return None
    
    ist = pytz.timezone('Asia/Kolkata')
    
    # If it's a naive datetime, assume it's IST
    if ist_datetime.tzinfo is None:
        ist_datetime = ist.localize(ist_datetime)
    
    return ist_datetime.astimezone(pytz.utc)

def format_ist_time(datetime_obj, format_str="%I:%M %p"):
    """Format datetime object to IST time string"""
    if datetime_obj is None:
        return "-"
    
    # Convert to IST if it's UTC
    ist_time = utc_to_ist(datetime_obj)
    return ist_time.strftime(format_str)

def format_ist_date(datetime_obj, format_str="%Y-%m-%d"):
    """Format datetime object to IST date string"""
    if datetime_obj is None:
        return "-"
    
    # Convert to IST if it's UTC
    ist_time = utc_to_ist(datetime_obj)
    return ist_time.strftime(format_str)