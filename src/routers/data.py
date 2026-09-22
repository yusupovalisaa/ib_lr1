from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import User, Post
from ..schemas import UserOut, PostCreate, PostOut

router = APIRouter(prefix="/api", tags=["data"])


@router.get("/data", response_model=List[UserOut])
def get_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Список пользователей. Только с валидным JWT."""
    return db.query(User).all()


@router.get("/posts", response_model=List[PostOut])
def list_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Post).all()


@router.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = Post(title=payload.title, content=payload.content, author_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post