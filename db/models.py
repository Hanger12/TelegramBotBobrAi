from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.orm import relationship

from config import Config

Base = declarative_base()
engine = create_engine(Config.DATABASE_URL)


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_settings.user_id', ondelete="CASCADE"))  # Добавлен внешний ключ
    command = Column(String)
    response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Связь с настройками пользователя
    settings = relationship("UserSettings", uselist=False, back_populates="user")


class UserSettings(Base):
    __tablename__ = 'user_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)  # Убрали внешний ключ здесь, потому что он должен быть в Log
    default_city = Column(String, nullable=True)

    # Связь с логами
    user = relationship("Log", back_populates="settings")


Base.metadata.create_all(bind=engine)
