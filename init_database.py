import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text

DB_CONFIG = {
    "user": "postgres",
    "password": "12345",
    "host": "localhost",
    "port": "5432",
    "dbname": "test_db"
}

SQL_SCRIPT = """
CREATE SCHEMA IF NOT EXISTS message_schema;

CREATE TABLE IF NOT EXISTS message_schema.messages (
    id SERIAL PRIMARY KEY,
    sender VARCHAR(100) DEFAULT 'Anons',
    text TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_messages_sender ON message_schema.messages(sender);
"""

def init_db():
    try:

        admin_engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/postgres"
        )

        with admin_engine.connect() as admin_conn:

            exists = admin_conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname='{DB_CONFIG['dbname']}'")
            ).scalar()

            if not exists:

                admin_conn.execute(text(f"CREATE DATABASE {DB_CONFIG['dbname']}"))
                print(f"База данных {DB_CONFIG['dbname']} создана")
            else:
                print(f"База данных {DB_CONFIG['dbname']} уже существует")


        engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
        )

        with engine.connect() as conn:

            conn.execute(text(SQL_SCRIPT))
            print("Таблицы успешно созданы")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    init_db()
