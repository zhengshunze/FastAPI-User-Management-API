from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Create SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Define SQLAlchemy model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic model for user creation
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# CRUD operations
def create_user(db, user: UserCreate):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


# API endpoints
@app.post("/users/", response_model=UserCreate)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return create_user(db, user)


@app.get("/users/{user_id}", response_model=UserCreate)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserCreate)
def update_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, user_id, user)


@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
