from auth.token import get_current_user
from data.database import get_db
from data.models import User
from data.schemas import CreateTopicRequest
from fastapi import APIRouter, Depends, HTTPException, status
from services.topic_service import (
    create_topic,
    get_topic,
    get_topics,
    lock_topic_for_users,
)
from sqlalchemy.orm import Session

topics_router = APIRouter(prefix="/topics", tags=["topics"])


@topics_router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_topic(
    topic: CreateTopicRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_topic(db, topic, current_user)


@topics_router.get("/category/{category_id}")
def view_topics(
    category_id: int,
    skip: int = 0,
    limit: int = 100,
    sort: str = None or None,
    search: str = None or None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_topics(
        db,
        category_id=category_id,
        skip=skip,
        limit=limit,
        sort=sort,
        search=search,
        current_user=current_user,
    )


@topics_router.get("/{topic_id}")
def view_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    topic = get_topic(db, topic_id, current_user)
    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found."
        )
    return topic


@topics_router.put("/{topic_id}/lock")
def lock_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return lock_topic_for_users(db, topic_id, current_user)
