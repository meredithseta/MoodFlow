import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="moodflow"
    )

def log_audit_action(user_id, action, table_name, record_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Audit_log (user_id, action, table_name, record_id)
        VALUES (%s, %s, %s, %s)
    """, (user_id, action, table_name, record_id))
    conn.commit()
    cur.close()
    conn.close()

