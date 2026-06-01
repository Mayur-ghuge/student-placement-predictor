import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mayur@1646",
        database="placement_predictor"
    )

    return connection