from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:mypassword@localhost:port_number/telecom_db"
engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    connection.execute("""
        ALTER TABLE subscriber ADD COLUMN additional_data JSON;
    """)
