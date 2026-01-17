from fastapi import APIRouter, Depends
from app.models import Chat
from app.database import get_db
from sqlalchemy.orm import Session
from app.routes.user_routes import get_current_user
from pydantic import BaseModel, ConfigDict
from app.models import User
from app.models import Chat
from app.models import Message
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(
    prefix="/message",
    tags=["Message"]
)


class MessageCreate(BaseModel):
    chat_id: int
    content: str
    role: str

@router.get("")
async def get_messages(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    messages = db.query(Message).filter(Message.user_id == user.id).all()
    return messages

@router.get("/{message_id}")
async def get_message(message_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.post("/message")
async def create_message(message: MessageCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    message = Message(**message.model_dump(), user_id=user.id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.patch("/message/{message_id}")
async def update_message(message_id: int, message_update: MessageCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.chat_id = message_update.chat_id
    message.content = message_update.content
    message.role = message_update.role
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.delete("/message/{message_id}")
async def delete_message(message_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return message

@router.get("/message/chat/{chat_id}")
async def get_chat_messages(chat_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    return messages

