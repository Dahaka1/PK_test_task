import os.path
import shutil

import src.settings
from . import models, schemas
from sqlalchemy.orm import Session
from fastapi import UploadFile
from . import utils
from shutil import copyfileobj, rmtree


def create_file(db: Session, uploaded_file: UploadFile) -> schemas.File:
	if not os.path.exists(src.settings.TEMPORARY_FILES_DIR):
		os.mkdir(src.settings.TEMPORARY_FILES_DIR)
	temp_path = src.settings.TEMPORARY_FILES_DIR + uploaded_file.filename
	with open(temp_path, "wb") as buffer:
		copyfileobj(uploaded_file.file, buffer)

	saved_file = open(temp_path, 'rb')
	file = models.File(
		name=uploaded_file.filename,
		size=uploaded_file.size,
		content=saved_file.read()
	)
	saved_file.close()

	db.add(file)
	db.commit()
	db.refresh(file)

	file_schema = schemas.File(
		id=file.id,
		name=file.name,
		size=file.size,
		fields=utils.parse_fields(temp_path)
	)

	for field in file_schema.fields:
		db_field = models.Field(
			file_id=file_schema.id,
			name=field
		)
		db.add(db_field)
		db.commit()

	rmtree(src.settings.TEMPORARY_FILES_DIR)

	return file_schema


def get_files(db: Session) -> list[schemas.File]:
	files = db.query(
		models.File
	).all()
	return [
		schemas.File(
			id=file.id, name=file.name, size=file.size, fields=file.get_fields(db=db)
		) for file in files
	]


def get_file(file: models.File, filepath: str, params: dict, db: Session) -> dict[str] | Exception:
	data = utils.parse_file(filepath)
	sorting_query = src.settings.SORTING_QUERY
	sorting: list[dict] | None = params.get(sorting_query) if not params is None else None
	if not sorting is None:
		for param in sorting:
			if isinstance(param, dict):
				column = param.get("column_name")
				order = param.get("order_by")
				if all(p is not None for p in (column, order)):
					if not column in file.get_fields(db=db):
						return Exception(f"Column '{column}' doesn't exists")
					if not order in src.settings.ORDERING_PARAMS:
						return Exception(f"Ordering param isn't supported. "
										 f"It must be in {src.settings.ORDERING_PARAMS}")

					data = sorted(data, key=lambda data_dict: int(data_dict[column])
					if str(data_dict[column]).isdigit() else data_dict[column],
								  reverse=True if order == "desc" else False)

				else:
					return Exception("Got an non-supportable params dict format. "
									 "It must includes keys 'column_name' and 'order_by'")
	return data
