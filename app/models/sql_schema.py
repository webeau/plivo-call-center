from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

class BaseModel(object):
    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))

        return d

class CallQueue(Base, BaseModel):
    __tablename__ = "call_queue"
    Id = Column(String(255), primary_key=True) # CallUUID
    Direction = Column(String(10))
    From = Column(String(255), nullable=False)
    CallerName = Column(String(255))
    BillRate = Column(String(10), nullable=False)
    To = Column(String(255), nullable=False)
    CallStatus = Column(String(255), nullable=False)
    QueueTime = Column(DateTime)
    IsCompleted = Column(Boolean, default=False)
    Agent = Column(String(255))

class AgentPresence(Base, BaseModel):
    __tablename__ = "agent_presence"
    Id = Column(String(255), primary_key=True)
    DateAdded = Column(DateTime)
    OnCall = Column(Boolean, default=False, nullable=False)