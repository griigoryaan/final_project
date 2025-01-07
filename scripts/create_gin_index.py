from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:mypassword@localhost:port_number/telecom_db"
engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    connection.execute("""
        CREATE INDEX ix_subscriber_additional_data
        ON subscriber
        USING GIN (additional_data jsonb_path_ops);
    """)
