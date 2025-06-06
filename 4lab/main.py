from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return db.query(models.Author).all()


@app.post("/authors", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return db_author


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.update_author(db, author_id, author)
    if not db_author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return db_author


@app.delete("/authors/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    if not crud.delete_author(db, author_id):
        raise HTTPException(status_code=404, detail="Автор не найден")


@app.get("/books", response_model=list[schemas.Book])
def read_books(author_id: int = None, db: Session = Depends(get_db)):
    return crud.get_books(db, author_id)


@app.post("/books", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.create_book(db, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return db_book
