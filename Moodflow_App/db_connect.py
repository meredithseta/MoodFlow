import mysql.connector

def mysql_connect():
    return mysql.connector.connect(
        host='192.168.1.156',
        port=3306,
        database='moodflow',
        user='root',
        password='Torchlight123!'
    )