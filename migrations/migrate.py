import logging
from peewee_migrate import Router
from app.db.database import database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("migrations.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

router = Router(database, migrate_dir='migrations')

if __name__ == '__main__':
    try:
        logger.info("Starting migration process.")
        logger.info("Creating new migration file if there are changes in the models.")
        router.create(auto=True)
        logger.info("Applying all pending migrations.")
        router.run()
        logger.info("Migration process completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during the migration process: {e}")
