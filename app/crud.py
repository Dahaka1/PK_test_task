import os.path
from shutil import copyfileobj, rmtree
from typing import Any

from fastapi import UploadFile
from sqlalchemy.orm import Session

import src.settings
from . import models, schemas
from . import utils


def create_file(db: Session, uploaded_file: UploadFile) -> schemas.File:
	"""
	Создает файл в БД (сначала копирует из буфера в реальный файл, затем байты сохраняет в content
	в объекте sqlalchemy)
	"""
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


def get_file(file: models.File, filepath: str, params: dict, db: Session) -> tuple[schemas.File, list[dict]] | Exception:
	"""
	Громоздкая функция. Делает фильтрацию и сортировку
	"""
	data = utils.parse_file(filepath)
	sorting_query, filtering_query = src.settings.SORTING_QUERY, src.settings.FILTERING_QUERY
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

					data = utils.sort_data(data=data, column=column, order=order)

				else:
					return Exception("Got an non-supportable sorting params dict format. "
									 "It must includes keys 'column_name' and 'order_by'")
			else:
				return Exception("Param must be dict")

	filtering: list[dict] | None = params.get(filtering_query) if not params is None else None
	if not filtering is None:
		for param in filtering:
			if isinstance(param, dict):
				column = param.get("column_name")
				filter_ge, filter_le = param.get("ge"), param.get("le")
				if not column is None and any((filter_ge, filter_le)):
					if not column in file.get_fields(db=db):
						return Exception(f"Column '{column}' doesn't exists")
					try:
						float(filter_ge), float(filter_le)
					except ValueError:
						return Exception("Filtering values must be numbers ("
										 "you can choose length for string columns and "
										 "range of values for integer/float columns)")
					except TypeError:
						pass
					if filter_ge:
						data = utils.filter_data(
							filtering_data=data, filtering_type="ge", value=filter_ge, data_column=column
						)
						if isinstance(data, Exception):
							return Exception(str(data))
					if filter_le:
						data = utils.filter_data(
							filtering_data=data, filtering_type="le", value=filter_le, data_column=column
						)
						if isinstance(data, Exception):
							return Exception(str(data))

				else:
					return Exception("Got an non-supportable filtering params dict format. "
									 "It must includes keys 'column_name' and 'ge'/'le'")
			else:
				return Exception("Param must be dict")

	file_schema = schemas.File(
		id=file.id, name=file.name, size=file.size, fields=file.get_fields(db=db)
	)

	return file_schema, data


def update_file(file_for_updating: Any, updated_file: schemas.FileBase, db: Session) -> schemas.File:
	"""
	Обновляет имя существующего файла
	"""
	file_for_updating.name = updated_file.name
	db.commit()
	db.refresh(file_for_updating)
	return schemas.File(
		id=file_for_updating.id, name=file_for_updating.name, fields=file_for_updating.get_fields(db=db),
		size=file_for_updating.size
	)


def delete_file(file: Any, db: Session) -> schemas.File:
	"""
	Удаляет существующий файл
	"""
	file_schema = schemas.File(
		id=file.id, name=file.name, size=file.size, fields=file.get_fields(db=db)
	)
	db.query(
		models.File
	).filter_by(id=file.id).delete()
	db.commit()
	return file_schema
