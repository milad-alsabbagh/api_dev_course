from .. import schemas, models, utils
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import  get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#create user (signUp)
@router.post("/", status_code=201,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password= hashed_password
    new_user = models.User(**user.model_dump())  # type: ignore
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#get User by id
@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()  # type: ignore
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} not found"
        )
    return user