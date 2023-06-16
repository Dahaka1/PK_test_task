from shutil import rmtree
from typing import Annotated

from fastapi import FastAPI, UploadFile, Depends, HTTPException, status, Path, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import src.settings
from . import crud
from . import dependencies
from . import schemas, models

app = FastAPI()


@app.post("/files/", response_model=schemas.File)
def create_file(
	file: Annotated[UploadFile, Depends(dependencies.upload_file)],
	db: Session = Depends(dependencies.get_db)
):
	"""
	Отправка файла. Тело запроса: multipart/form-data ("file": *файл*).
	Возвращает Pydantic-объект созданного файла
	"""
	file: schemas.File = crud.create_file(db=db, uploaded_file=file)

	return file


@app.get("/files/", response_model=list[schemas.File])
def get_files(
	db: Session = Depends(dependencies.get_db)
):
	"""
	Get-метод для получения всех файлов. Возвращаются объекты Pydantic
	"""
	return crud.get_files(db=db)


@app.get("/files/{file_id}")
def get_file(
	file: Annotated[schemas.File, Depends(dependencies.get_file)],
	db: Session = Depends(dependencies.get_db)
):
	"""
	Получить информацию о файле и его содержимое, ИД которого указывается в url
	Более подробно - в README.md
	"""
	response = crud.get_file(*file, db=db)
	rmtree(src.settings.TEMPORARY_FILES_DIR)  # remove after creating in crud.get_file func
	if isinstance(response, Exception):
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
							detail=str(response))

	file_schema, file_data = response
	response_serialized = jsonable_encoder(file_data)
	return {"file": file_schema,
			"content": response_serialized}


@app.put("/files/{file_id}", response_model=schemas.File)
def update_file(
	file_id: Annotated[int, Path(ge=1)],
	file: Annotated[schemas.FileBase, Body()],
	db: Session = Depends(dependencies.get_db)
):
	"""
	Обновить файл. Обновить можно только имя файла. Возвращается Pydantic-объект обновленного файла
	"""
	file_for_updating = db.query(
		models.File
	).filter_by(id=file_id).first()
	if file_for_updating is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

	return crud.update_file(file_for_updating=file_for_updating, updated_file=file, db=db)


@app.delete("/files/{file_id}", response_model=schemas.File)
def delete_file(
	file_id: Annotated[int, Path(ge=1)],
	db: Session = Depends(dependencies.get_db)
):
	"""
	Удалить файл по ИД, указанному в url. Возвращается Pydantic-объект удаленного файла
	"""
	file = db.query(
		models.File
	).filter_by(id=file_id).first()
	if file is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
	return crud.delete_file(file=file, db=db)
