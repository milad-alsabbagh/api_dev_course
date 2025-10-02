from typing import Optional
from .. import schemas, models,oauth2
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import  get_db
from sqlalchemy import func

router = APIRouter( 
    prefix="/posts",
    tags=["Posts"]
)


# @router.get("/",response_model=list[schemas.PostResponse])
@router.get("/",response_model=list[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),curr_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    results=db.query(models.Post,func.count(models.Vote.user_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # type: ignore
    return results


@router.post("/", status_code=201,response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),curr_user:models.User =Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=curr_user.id, **post.model_dump())  # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/mine",response_model=list[schemas.PostOut])
def get_my_posts(db:Session=Depends(get_db),curr_user:int=Depends(oauth2.get_current_user)):
    posts=db.query(models.Post,func.count(models.Vote.user_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(curr_user.id==models.Post.owner_id).all() # type: ignore
    return posts


@router.get("/latest",response_model=schemas.PostOut)
def get_latest_posts(db: Session = Depends(get_db),curr_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post,func.count(models.Vote.user_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).order_by(models.Post.id.desc()).first()   # type: ignore
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no posts found"
        )
    return post


@router.get("/{id}",response_model=schemas.PostOut,)
def get_post(id: int, db: Session = Depends(get_db),curr_user:int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post,func.count(models.Vote.user_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()  # type: ignore
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found"
        )
    return post


@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db),curr_user:int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)  # type: ignore
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found"
        )
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(post)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    if post.first().owner_id == curr_user.id: # type: ignore
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='you do not have permission')


@router.put("/{id}", status_code=200,response_model=schemas.Post,)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db),curr_user:int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)  # type: ignore

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found"
        )
    if post_query.first().owner_id !=curr_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='do not have permission')
    post_query.update(post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()

    return  post_query.first()  # type: ignore

