from app.database import get_db
from app import oauth2, schemas, models
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote_sch: schemas.Vote, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote_sch.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{vote_sch.post_id} doesn't exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_sch.post_id,
                                              models.Vote.user_id == user.id)
    found_vote = vote_query.first()
    if vote_sch.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"{user.id} has already voted on post {vote_sch.post_id}")
        
        new_vote = models.Vote(user_id=user.id, post_id=vote_sch.post_id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"vote doesn't exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
    
