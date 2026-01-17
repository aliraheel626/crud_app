from fastapi import APIRouter, Depends
from app.models import Chat
from app.database import get_db
from sqlalchemy.orm import Session
from app.routes.user_routes import get_current_user
from pydantic import BaseModel, ConfigDict
from app.models import User
from app.models import Chat
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()


class ChatCreate(BaseModel):
    # model_config = ConfigDict(extra='forbid')
    name: str


@router.post("/chat")
def create_chat( chat: ChatCreate,db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chat = Chat(**chat.model_dump(), user_id=user.id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@router.get("/chat")
def get_chats(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chats = db.query(Chat).filter(Chat.user_id == user.id).all()
    return chats


@router.get("/chat/{chat_id}")
def get_chat(chat_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        return HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.patch("/chat/{chat_id}")
def update_chat(chat_id: int, chat_update: ChatCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat.name = chat_update.name
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@router.delete("/chat/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(chat)
    db.commit()
    return chat

@router.get("/chat/{chat_id}/messages")
def get_chat_messages(chat_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    return messages


