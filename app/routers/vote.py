from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first() # type: ignore
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{vote.post_id} not found")
    # if dir==1 that mean I want to like post else I want to unlike it
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id) # type: ignore
    found_vote=vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted the post") # type: ignore
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id) # type: ignore
        db.add(new_vote)
        db.commit()
        return {"message":"vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote deleted successfully"}
        