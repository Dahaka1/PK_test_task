from sqlalchemy import Column, Integer, String, LargeBinary, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import Session

from .database import Base


class Field(Base):
    """
    Нужно сохранить колонки сразу, чтобы при получении общего списка файлов не парсить заново их все
    """
    __tablename__ = "fields"
    __table_args__ = (
        PrimaryKeyConstraint("file_id", "name", name="file_name_pkey"),
    )

    file_id = Column(Integer, ForeignKey("files.id", onupdate="CASCADE", ondelete="CASCADE"))
    name = Column(String(length=50))


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    size = Column(Integer)
    content = Column(LargeBinary)

    def get_fields(self, db: Session) -> list[str]:
        fields = db.query(
            Field
        ).filter_by(file_id=self.id).all()

        return [str(field.name) for field in fields]
