from sqlalchemy.orm import Session
from . import models, schemas


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author: schemas.AuthorCreate):
    db_author = get_author(db, author_id)
    if db_author:
        db_author.name = author.name
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
        return True
    return False


def get_books(db: Session, author_id: int = None):
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    return query.all()


def create_book(db: Session, book: schemas.BookCreate):
    if not get_author(db, book.author_id):
        return None

    db_book = models.Book(
        title=book.title,
        year=book.year,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
