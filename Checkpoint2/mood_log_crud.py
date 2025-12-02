from db_connect import mysql_connect

def create_mood_log(user_id, mood_type_id, mood_color_hex, stress_level, notes):
    conn = mysql_connect()
    cursor = conn.cursor()

    sql = """
        INSERT INTO Mood_log (user_id, mood_type_id, mood_color_hex, stress_level, notes)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (user_id, mood_type_id, mood_color_hex, stress_level, notes))
    conn.commit()

    print("Mood log created with ID:", cursor.lastrowid)

    cursor.close()
    conn.close()
    return cursor.lastrowid

def read_mood_logs():
    conn = mysql_connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Mood_log ORDER BY log_date DESC")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

def update_mood_log(mood_log_id, new_notes):
    conn = mysql_connect()
    cursor = conn.cursor()

    sql = "UPDATE Mood_log SET notes = %s WHERE mood_log_id = %s"
    cursor.execute(sql, (new_notes, mood_log_id))
    conn.commit()

    print("Updated mood log:", mood_log_id)

    cursor.close()
    conn.close()

def delete_mood_log(mood_log_id):
    conn = mysql_connect()
    cursor = conn.cursor()

    sql = "DELETE FROM Mood_log WHERE mood_log_id = %s"
    cursor.execute(sql, (mood_log_id,))
    conn.commit()

    print("Deleted mood log:", mood_log_id)

    cursor.close()
    conn.close()

def filter_mood_logs(min_stress):
    conn = mysql_connect()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM Mood_log
        WHERE stress_level >= %s
        ORDER BY stress_level DESC
    """
    cursor.execute(sql, (min_stress,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows