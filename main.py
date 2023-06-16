from dotenv import load_dotenv
import time

load_dotenv()

time.sleep(5)  # waiting for database-container initializing

from src import start_app, logger_init
from app.database import database_init


def main():
	logger_init()
	database_init()
	start_app()


if __name__ == '__main__':
	main()
