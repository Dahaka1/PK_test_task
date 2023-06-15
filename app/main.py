from fastapi import FastAPI, UploadFile, Depends, Path, HTTPException, status
from fastapi.encoders import jsonable_encoder
from . import crud
from typing import Annotated
from . import dependencies
from sqlalchemy.orm import Session
from . import schemas
from shutil import rmtree
import src.settings

app = FastAPI()


@app.post("/files/", response_model=schemas.File)
def create_file(
	file: Annotated[UploadFile, Depends(dependencies.upload_file)],
	db: Session = Depends(dependencies.get_db)
):
	file: schemas.File = crud.create_file(db=db, uploaded_file=file)

	return file


@app.get("/files/", response_model=list[schemas.File])
def get_files(
	db: Session = Depends(dependencies.get_db)
):
	return crud.get_files(db=db)


@app.get("/files/{file_id}")
def get_file(
	file: Annotated[schemas.File, Depends(dependencies.get_file)],
	db: Session = Depends(dependencies.get_db)
):
	response = crud.get_file(*file, db=db)
	rmtree(src.settings.TEMPORARY_FILES_DIR)  # remove after creating in crud.get_file func
	if isinstance(response, Exception):
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
							detail=str(response))

	response_serialized = jsonable_encoder(response)
	return response_serialized
