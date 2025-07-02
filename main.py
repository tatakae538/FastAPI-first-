from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import SessionLocal, Message

app = FastAPI(title="API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class InputMess(BaseModel):
    sender: str = "Anons"
    text: str = Field(..., min_length=1, title="Text", description="Message of the user")

class OutputMess(BaseModel):
    id: int = Field(example=1)
    sender: str = Field(example="username")
    text: str = Field(example="Сообщение")
    timestamp: str = Field(example="2023-01-01T12:00:00Z")

@app.post("/messages",
          response_model=OutputMess,
          responses={
              200: {
                  "description": "Успешный ответ",
                  "content": {
                      "application/json": {
                          "example": {
                              "id": 1,
                              "sender": "test_user",
                              "text": "Пример сообщения",
                              "timestamp": "2023-01-01T12:00:00Z"
                          }
                      }
                  }
              }
          })
async def create_message(message: InputMess, db: Session = Depends(get_db)):
    db_message = Message(
        sender=message.sender,
        text=message.text
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return OutputMess(
        id=db_message.id,
        sender=db_message.sender,
        text=db_message.text,
        timestamp=db_message.timestamp.isoformat()
    )



@app.get("/get", response_model=list[OutputMess])
async def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).all()