import logging
import logging.handlers
import random
import time
from pathlib import Path


LOG_PATH = Path("app.log")


def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_PATH,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Ensure file-only logging
    logger.handlers.clear()
    logger.addHandler(file_handler)


class DatabaseService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect(self):
        self.logger.info("Connecting to database")
        time.sleep(0.1)

        if random.random() < 0.1:
            self.logger.error("Database connection failed")
            raise ConnectionError("DB unavailable")

        self.logger.debug("Database connection established")

    def query(self, sql):
        self.logger.debug("Executing query: %s", sql)
        time.sleep(0.05)
        return {"rows": random.randint(0, 10)}


class PaymentService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def process_payment(self, user_id, amount):
        self.logger.info(
            "Processing payment | user=%s amount=%.2f", user_id, amount
        )

        if amount <= 0:
            self.logger.warning(
                "Rejected payment with non-positive amount | user=%s", user_id
            )
            return False

        if random.random() < 0.2:
            self.logger.error(
                "Payment gateway timeout | user=%s", user_id
            )
            return False

        self.logger.info(
            "Payment successful | user=%s amount=%.2f", user_id, amount
        )
        return True


def main():
    logger = logging.getLogger("App")
    logger.info("Application starting")

    db = DatabaseService()
    payments = PaymentService()

    try:
        db.connect()
    except Exception:
        logger.critical("Startup failed", exc_info=True)
        return

    for i in range(5):
        user_id = f"user-{i}"
        amount = random.choice([10, 25, -5, 100])

        logger.debug("Handling request | user=%s", user_id)

        if payments.process_payment(user_id, amount):
            result = db.query("SELECT * FROM transactions")
            logger.debug("Query result: %s", result)

        time.sleep(0.2)

    logger.info("Application shutting down")

if __name__ == "__main__":
    configure_logging()
    main()
