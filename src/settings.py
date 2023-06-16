import os


DATABASE_PARAMS = {"user": os.environ.get("DB_USER"), "password": os.environ.get("DB_PASSWORD"),
	"host": os.environ.get("DB_HOST"), "port": os.environ.get("DB_PORT"), "dbname": os.environ.get("DB_NAME")}

DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % tuple(DATABASE_PARAMS.values())

STARTING_COMMAND = "uvicorn app.main:app --host 0.0.0.0 --port 8000"

STANDARD_DB_TABLES_AMOUNT = 3  # with alembic versions table

TEMPORARY_FILES_DIR = "tmp/"

AVAILABLE_FILES_FORMATS = [
	".csv"
]

FILTERING_QUERY = "filtered_by"
SORTING_QUERY = "sorted_by"

ORDERING_PARAMS = [
	"asc",
	"desc"
]

DATABASE_INIT_COMMANDS = [
	"alembic revision --autogenerate -m 'created'",
	"alembic upgrade head"
]


# loguru settings
LOGGING_FORMAT = '{time} {level} {message}'
ERRORS_OUTPUT_FILE = 'logs.log'
LOGGING_LEVELS = [
	"ERROR",
	"INFO"
]