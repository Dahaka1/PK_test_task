#pk_test_task 

# ABOUT
This is the simple FastAPI project realizing app includes functions for uploading files to storage and 
handling information about them. Works using all std http-methods.

# BUILT-IN
- Python 3.11;
- FastAPI framework, SQLAlchemy, Pydantic packages;
- loguru - for additional logging;
- PostgreSQL - DB;
- pytest - testing.

# USAGE
- Firstly, you should to do git-clone of the project. Then, start docker container by running commands in the command-line from project directory: 
    - *'docker-compose build'*, *'docker-compose up'*;
- After Postgres DB starting application would automatically initialize database structure using sqlalchemy ORM-models and Alembic migration tool. You should to wait about 5-10 seconds at first-time running;
- Now, you can check all available http-methods in standard Swagger-documentation by using address *'localhost:8000/docs'*;
- All methods include russian-language description of using. You can check how them works using Swagger standard forms or advanced applications such as Postman;

# Notice
- GET-method for files that getting specify file info by its ID *don't work with additional sorting and filtering params in standard Swagger docs page*, because GET-method usually don't provide sending query body-params;
- You can use that params using another app like Postman like it shows on the screenshot below: