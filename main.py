from fastapi import FastAPI, Depends, HTTPException
import services, models, schemas
from db import get_db, engine
from sqlalchemy.orm import Session
from models import Book, Employee,Student

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import status
from jose import JWTError, jwt


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

#-------------------------for Book------------------------

@app.get("/books/", response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    return services.get_books(db)

@app.post("/books/", response_model=schemas.Book)
def create_new_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return services.create_book(db, book)

@app.put("/books/{id}", response_model=schemas.Book)
def update_book(id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_update = services.update_book(db, id, book)
    if not db_update:
        raise HTTPException(status_code=404, detail="Book Not Found")
    return db_update

@app.delete("/books/{id}", response_model=schemas.Book)
def delete_book(id: int, db: Session = Depends(get_db)):
    deleted = services.delete_book(db, id)
    if deleted:
        return deleted
    raise HTTPException(status_code=404, detail="Book Not Found")



#-------------------------for Employee------------------------



@app.get("/employees/", response_model=list[schemas.Employee])
def get_all_employees(db: Session = Depends(get_db)):
    return services.get_employees(db)

@app.post("/employees/", response_model=schemas.Employee)
def create_new_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return services.create_employee(db, emp)

@app.put("/employees/{id}", response_model=schemas.Employee)
def update_employee(id: int, emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_update = services.update_employee(db, id, emp)
    if not db_update:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    return db_update

@app.delete("/employees/{id}", response_model=schemas.Employee)
def delete_employee(id: int, db: Session = Depends(get_db)):
    deleted = services.delete_employee(db, id)
    if deleted:
        return deleted
    raise HTTPException(status_code=404, detail="Employee Not Found")



#-------------------------for Student------------------------



@app.get("/students/", response_model=list[schemas.Student])
def get_all_students(db: Session = Depends(get_db)):
    return services.get_students(db)

@app.post("/students/", response_model=schemas.Student)
def create_new_student(std: schemas.StudentCreate, db: Session = Depends(get_db)):
    return services.create_student(db, std)

@app.put("/students/{id}", response_model=schemas.Student)
def update_student(id: int, std: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_update = services.update_student(db, id, std)
    if not db_update:
        raise HTTPException(status_code=404, detail="Student Not Found")
    return db_update

@app.delete("/students/{id}", response_model=schemas.Student)
def delete_student(id: int, db: Session = Depends(get_db)):
    deleted = services.delete_student(db, id)
    if deleted:
        return deleted
    raise HTTPException(status_code=404, detail="Student Not Found")















# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, services.SECRET_KEY, algorithms=[services.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = services.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


# ---------- Auth Routes ----------

@app.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = services.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return services.create_user(db, user)


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = services.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# ---------- Protected Route ----------

@app.get("/secure-data/")
def secure_data(current_user: schemas.User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you're authenticated!"}
