from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.routes.user_routes import get_current_user
from pydantic import BaseModel
from app.models import User, Chat, Message

router = APIRouter(prefix="/chat", tags=["Chat"]) 


class ChatCreate(BaseModel):
    name: str


@router.post("")
def create_chat(chat: ChatCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_chat = Chat(**chat.model_dump(), user_id=user.id)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


@router.get("")
def get_chats(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chats = db.query(Chat).filter(Chat.user_id == user.id).all()
    return chats


@router.get("/{chat_id}")
def get_chat(chat_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chat")
    return chat


@router.patch("/{chat_id}")
def update_chat(chat_id: int, chat_update: ChatCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this chat")
    chat.name = chat_update.name
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


@router.delete("/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this chat")
    db.delete(chat)
    db.commit()
    return {"detail": "Chat deleted"}


@router.get("/{chat_id}/messages")
def get_chat_messages(chat_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access messages for this chat")
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    return messages

