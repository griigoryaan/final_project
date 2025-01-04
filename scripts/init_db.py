import psycopg2
from psycopg2 import sql

def create_database():
    host = "localhost"
    user = "postgres"
    password = "your_password"
    database_name = "telecom_db"
    owner = "postgres"

    try:
        conn = psycopg2.connect(host=host, user=user, password=password)
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(
            sql.SQL("""
            CREATE DATABASE {db_name}
            WITH OWNER {owner}
            ENCODING 'UTF8'
            TEMPLATE template0;
            """).format(
                db_name=sql.Identifier(database_name),
                owner=sql.Identifier(owner),
            )
        )
        print(f"Database '{database_name}' created successfully.")

    except Exception as e:
        print(f"Error creating database: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()
