from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import Base

class LanguageChoice(Base):
    __tablename__ = "language_choices"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String, index=True)
    image_path = Column(String, index=True)


class LanguageChoiceBase(BaseModel):
    language: str
    image_path: str


class LanguageChoiceCreate(LanguageChoiceBase):
    pass


class LanguageChoiceSchema(LanguageChoiceBase):
    id: int


def get_language(db: Session, lang_id: int) -> LanguageChoice | None:
    return db.query(LanguageChoice).filter(LanguageChoice.id == lang_id).first()


def get_languages(db: Session, skip: int = 0, limit: int = 100) -> list[LanguageChoice]:
    return db.query(LanguageChoice).offset(skip).limit(limit).all()


def create_language(db: Session, lang: LanguageChoiceCreate) -> LanguageChoice:
    db_lang = LanguageChoice(language=lang.language, image_path=lang.image_path)
    db.add(db_lang)
    db.commit()
    db.refresh(db_lang)
    return db_lang
