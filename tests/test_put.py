from dotenv import load_dotenv

load_dotenv()

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_put_file():
	testing_file = {"file": open("tests/blob/hungary-forecast.csv", 'rb')}
	file_id = client.post(
		"/files/",
		files=testing_file
	).json().get("id")

	file_update = client.put(
		f"/files/{file_id}",
		json={"name": "Qwerty.csv"}
	)

	assert file_update.status_code == 200
	assert file_update.json().get("name") == "Qwerty.csv"

	client.delete(
		f"/files/{file_id}"
	)


def test_put_non_existing_file():
	file_update = client.put(
		f"/files/123123141",
		json={"name": "Qwerty.csv"}
	)
	assert file_update.status_code == 404
	assert file_update.json() == {"detail": "File not found"}

