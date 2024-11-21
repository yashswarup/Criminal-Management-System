from db_connection import get_connection

def create_user(username, password, role):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        conn.commit()
        cursor.close()
        conn.close()

def get_user(username):
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

def insert_data(table, data):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(data.values()))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting data into {table}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def authenticate_user(username, password):
    """
    Verifies if the given username and password match an existing user in the database.

    Parameters:
    - username (str): The user's username.
    - password (str): The user's password.

    Returns:
    - dict: User information if authentication is successful, None otherwise.
    """
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user if user else None
