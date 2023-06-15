from dotenv import load_dotenv

load_dotenv()

from src import start_app, logger_init
from app.database import database_init
from app.models import File


def main():
	logger_init()
	database_init()
	start_app()


if __name__ == '__main__':
	main()
