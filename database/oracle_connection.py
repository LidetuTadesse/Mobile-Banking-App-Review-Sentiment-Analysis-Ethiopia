# database/oracle_connection.py
import cx_Oracle

def get_connection():
    try:
        dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")  # Oracle XE default
        connection = cx_Oracle.connect(user="system", password="root", dsn=dsn)
        return connection
    except cx_Oracle.DatabaseError as e:
        print(" Oracle connection failed:", e)
        return None