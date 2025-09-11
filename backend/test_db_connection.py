import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os

# Use the full URL directly for this test
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5433/learning_platform"

print(f"Attempting to connect to the database at: {DATABASE_URL}")
print(f"Using SQLAlchemy version: {sqlalchemy.__version__}")

try:
    # Create the SQLAlchemy engine
    engine = sqlalchemy.create_engine(DATABASE_URL)
    
    print("Engine created successfully.")
    
    # Attempt to establish a connection
    with engine.connect() as connection:
        print("Connection successful!")
        
        # Execute a simple test query
        result = connection.execute(sqlalchemy.text("SELECT 1"))
        for row in result:
            print(f"Test query result: {row}")
            
    print("\nDatabase connection test PASSED.")

except Exception as e:
    print("\nDatabase connection test FAILED.")
    print("An error occurred while connecting to the database:")
    import traceback
    traceback.print_exc()
