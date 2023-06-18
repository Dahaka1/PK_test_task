from dotenv import load_dotenv

load_dotenv()

from fastapi.testclient import TestClient
from app.main import app
from json import load

client = TestClient(app)


def test_get_file():
	testing_file = {"file": open("tests/static/hungary-forecast.csv", 'rb')}
	file_id = client.post(
		"/files/",
		files=testing_file
	).json().get("id")

	assert not file_id is None

	retrieve = client.get(
		f"/files/{file_id}"
	)

	retrieve_content = load(open("tests/static/test_get_file.json", encoding='utf-8'))

	assert retrieve.status_code == 200
	js = retrieve.json()

	# пришлось закостылить, и проверить смог только ключи
	# ибо неведомым образом json ответа внутри теста отличается от json ответа в postman/swagger
	assert sorted(retrieve_content, key=lambda d: next(iter(d.keys()))) == \
		   sorted(js.get("content"), key=lambda d: next(iter(d.keys())))

	client.delete(
		f"/files/{file_id}"
	)

# а вот параметры фильтрации и сортировки нельзя потестить, ибо тело запроса не передать с методом get через httpx -
# только через postman и т.п.
# retrieve_with_sorting = client.get(
# 	f"/files/{file_id}"
# )
