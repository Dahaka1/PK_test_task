from dotenv import load_dotenv

load_dotenv()

from fastapi.testclient import TestClient
from app.main import app
from app import schemas, models
from app.dependencies import get_db

client = TestClient(app)


def test_delete_file():
	testing_file = {"file": open("tests/blob/hungary-forecast.csv", 'rb')}
	file_id = client.post(
		"/files/",
		files=testing_file
	).json().get("id")

	db = next(iter(get_db()))
	file = db.query(
		models.File
	).filter_by(id=file_id).first()

	fields = file.get_fields(db=db)

	response = client.delete(
		f"/files/{file_id}"
	)

	assert response.status_code == 200

	js = response.json()

	assert js.get("name") == file.name
	assert js.get("size") == file.size
	assert js.get("id") == file.id
	assert set(js.get("fields")) == set(fields)


def test_delete_non_existing_file():
	response = client.delete(
		"/files/213412"
	)
	assert response.status_code == 404
	assert response.json() == {"detail": "File not found"}
