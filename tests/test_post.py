from dotenv import load_dotenv

load_dotenv()

from fastapi.testclient import TestClient
from app.main import app
import src.settings
from app.models import File
from app.dependencies import get_db

client = TestClient(app)


def test_create_file():
	testing_file = {"file": open("tests/static/hungary-forecast.csv", 'rb')}
	response = client.post(
		"/files/",
		files=testing_file
	)
	assert response.status_code == 200
	js = response.json()
	assert js.get("name") == "hungary-forecast.csv"
	assert js.get("size") == 840
	assert js.get("fields") == [
		"country",
		"Year",
		"Population",
		"Yearly %   Change",
		"Yearly  Change",
		"Migrants (net)",
		"Median Age",
		"Fertility Rate",
		"Density (P/KmВІ)",
		"Urban  Pop %",
		"Urban Population",
		"Country's Share of  World Pop",
		"World Population",
		"Rank"
	]
	db = next(get_db())
	assert js.get("id") == db.query(
		File
	).order_by(File.id.desc()).first().id
	client.delete(f"/files/{js.get('id')}")


def test_create_empty_file():
	response = client.post("/files/")
	assert response.status_code == 405
	assert response.json() == {"detail": "The file wasn't uploaded"}


def test_create_non_supported_format_file():
	testing_file = {"file": open("tests/static/test.png", 'rb')}
	response = client.post(
		"/files/",
		files=testing_file
	)
	assert response.status_code == 400
	assert response.json() == {
		"detail": f"Got an invalid file format. Only supports to {src.settings.AVAILABLE_FILES_FORMATS}"
	}



