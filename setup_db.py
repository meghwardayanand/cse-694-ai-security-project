from sqlalchemy import create_engine, text
import sqlite3


def create_db_engine():
    try:
        engine = create_engine("sqlite:///demo.db")
        return engine
    except Exception as e:
        raise ValueError('ERROR: DB Engine Creation Error!')

def connect_db(engine):
    try:
        connection = engine.connect()
        return connection
    except Exception as e:
        raise ValueError('ERROR: DB Connection Error!')

def create_tables(connection):
    try:
        connection.execute(text(
            """DROP TABLE IF EXISTS users;"""
        ))
        connection.execute(text(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER
                );
            """
        ))
    except Exception as e:
        raise ValueError('ERROR: Table Not Created!')
    finally:
        connection.close()

def add_data(data):
    with sqlite3.connect("demo.db") as conn:
        cursor = conn.cursor()

        for table, records in data.items():
            for record in records:
                keys = list(record.keys())
                values = list([f"'{str(item)}'" for item in record.values()])
                cursor.execute(
                    f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({', '.join(values)});"
                )

            cursor.execute(f"SELECT * FROM {table}")
            print(cursor.fetchall())

def setup():
    engine = create_db_engine()
    connection = connect_db(engine)
    create_tables(connection)
    data = {
        "users": [
            {'name': 'Alice', 'age': 34},
            {'name': 'Bob', 'age': 23},
            {'name': 'Charlie', 'age': 25},
            {'name': 'Kim', 'age': 30},
            {'name': 'George', 'age': 50},
        ]
    }
    add_data(data)


if __name__ == "__main__":
    setup()
    with sqlite3.connect("demo.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users;")
        print(cursor.fetchall())
    print("Database setup complete.")
