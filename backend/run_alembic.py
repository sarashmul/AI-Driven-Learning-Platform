from alembic.config import Config
from alembic import command
import os

# Ensure the script is run from the backend directory context
# This helps alembic find the alembic.ini file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_migrations():
    """Runs alembic migrations programmatically."""
    print("Attempting to run Alembic migrations from script...")
    try:
        # Create an Alembic Config object
        # The second argument points to the alembic.ini file
        alembic_cfg = Config("alembic.ini")

        # Optionally, you can override configuration settings here
        # This ensures we are using the correct database URL, bypassing any other potential configurations
        print("Setting sqlalchemy.url programmatically...")
        alembic_cfg.set_main_option(
            "sqlalchemy.url", 
            "postgresql+psycopg://postgres:password@localhost:5433/learning_platform"
        )
        
        print("Alembic config loaded. Generating new revision...")
        # Generate a new revision
        command.revision(alembic_cfg, autogenerate=True, message="Initial migration from script")
        
        print("\nRevision generated successfully. Now upgrading to head...")
        # Apply the migration
        command.upgrade(alembic_cfg, "head")
        
        print("\nMigrations applied successfully!")

    except Exception as e:
        print("\nAn error occurred during the migration process:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_migrations()
