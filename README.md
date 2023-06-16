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
- After Postgres DB starting application will automatically initialize database structure using sqlalchemy ORM-models and Alembic migration tool. You should to wait about 5-10 seconds at first-time running;
- Now, you can check all available http-methods in standard Swagger-documentation by using address *'localhost:8000/docs'*;
- All methods include russian-language description of using. You can check how them works using Swagger standard forms or advanced applications such as Postman;

# Notice!!!
- GET-method for files for getting specify file info by its ID *don't work with additional sorting and filtering params in standard Swagger docs page*, because GET-method usually don't provide sending query body-params;
- You can use that params using another app like Postman like it shows on the screenshot below:

![alt text](https://github.com/Dahaka1/pk_test_task/blob/main/app/blob/get_file_query_params.png?raw=true)

- I didn't path operation function receiving params with query Path (url-string), because its uncomfortably to add many params for url.

# RUS
# ИСПОЛЬЗОВАНИЕ
- Во-первых, вам следует сделать git-клон проекта. Затем запустите контейнер docker, выполнив команды в командной строке из каталога проекта: 
    - *'docker-compose build'*, *'docker-compose up'*;
- После запуска Postgres DB приложение автоматически инициализирует структуру базы данных с помощью ORM-моделей sqlalchemy и инструмента миграции Alembic. При первом запуске вам следует подождать около 5-10 секунд;
- Теперь вы можете проверить все доступные http-методы в стандартной документации Swagger, используя адрес *'localhost:8000/docs'*;
- Все методы включают русскоязычное описание использования. Вы можете проверить, как они работают, используя стандартные формы Swagger или расширенные приложения, такие как Postman;

# Обратите внимание!!!
- GET-метод для файлов для получения информации о файле по его идентификатору *не работает с дополнительными параметрами сортировки и фильтрации на стандартной странице документации Swagger*, поскольку GET-метод обычно не предоставляет возможность отправлять параметры в теле запроса;
- Вы можете использовать эти параметры с помощью другого приложения, такого как Postman, как показано на скриншоте ниже:

![альтернативный текст](https://github.com/Dahaka1/pk_test_task/blob/main/app/blob/get_file_query_params.png?raw=true)

- Я не использовал получение параметров с помощью пути запроса (в url-строке), потому что неудобно добавлять много параметров в url.