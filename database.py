from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Настройки подключения
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/test_db"
engine = create_engine(DATABASE_URL)
#сначала создаем Base
Base = declarative_base()


# Затем определяем модель
class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {'schema': 'message_schema'}
    id = Column(Integer, primary_key=True)
    sender = Column(String(100))
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


    @property
    def timestamp_str(self):
        return self.timestamp.isoformat() if self.timestamp else None


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# воздаем таблицы
def init_db():
    Base.metadata.create_all(bind=engine)


# Вызов иниц
init_db()
