from pydantic import Field, BaseModel
from typing import Optional


class FileBase(BaseModel):
	name: str = Field(max_length=50)
	size: Optional[int] = Field(ge=1, default=None)


class FileCreate(FileBase):
	pass


class File(FileBase):
	id: int
	fields: list[str]

	class Config:
		orm_mode = True
