from pydantic import Field, BaseModel


class FileBase(BaseModel):
	name: str = Field(max_length=50)
	size: int = Field(ge=1)


class FileCreate(FileBase):
	pass


class File(FileBase):
	id: int
	fields: list[str]

	class Config:
		orm_mode = True
