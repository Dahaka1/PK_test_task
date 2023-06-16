import os.path
from typing import Annotated

from fastapi import UploadFile, File, HTTPException, status, Path, Body

import src.settings
from . import schemas, models
from .database import SessionLocal


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def upload_file(
	file: Annotated[
			UploadFile, File()
		] = None
):
	"""
	Проверка наличия отправляемого файла и его формата
	"""
	if file is None:
		raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="The file wasn't uploaded")

	if any(file.filename.endswith(file_format) for file_format in src.settings.AVAILABLE_FILES_FORMATS):
		return file
	else:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
							detail=f"Got an invalid file format. Only supports to {src.settings.AVAILABLE_FILES_FORMATS}")


def get_file(
	file_id: Annotated[int, Path(ge=1)],
	params: Annotated[dict | None, Body(embed=True)] = None
) -> tuple[schemas.File, str, dict | None]:
	"""
	Проверка правильности заполнения передачи параметров и существования файла.
	Создание временного файла с искомым содержимым для парсинга и фильтрации/сортировки после считывания
	csv-таблицы
	"""
	std_params = [src.settings.FILTERING_QUERY, src.settings.SORTING_QUERY]
	if not params is None:
		if any(not query in std_params for query in params):
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported query."
																				f"Supports only for {std_params}")
		if any(not isinstance(params.get(param), list) for param in params):
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Parameters values must "
																				f"be the list of dicts")
	db = next(get_db())
	file = db.query(models.File).filter_by(id=file_id).first()
	if file is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Chosen file not found")

	if not os.path.exists(src.settings.TEMPORARY_FILES_DIR):
		os.mkdir(src.settings.TEMPORARY_FILES_DIR)
	file_path: str = src.settings.TEMPORARY_FILES_DIR + file.name
	with open(file_path, 'wb') as file_out:
		file_out.write(file.content)

	return file, file_path, params
