from sqlalchemy import Column, DateTime, String, Integer, JSON, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import ColumnProperty

import db
from datetime import datetime


Base = declarative_base()
Base.metadata.create_all(db.engine)


class BaseMixin(object):
    def as_dict(self):
        result = {}
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, ColumnProperty):
                result[prop.key] = getattr(self, prop.key)
        return result


class ReceivedMessage(BaseMixin, Base):
    __tablename__ = 'received_messages'
    id = Column(Integer, primary_key=True)
    phone_from = Column(String, default=None) 
    msg_body = Column(String, default=None)
    created_at = Column(DateTime, default=datetime.utcnow())
    processed_at = Column(DateTime, default=None)


class MessageToSend(BaseMixin, Base):
    __tablename__ = 'messages_to_send'
    id = Column(Integer, primary_key=True)
    phone_to = Column(String, default=None) 
    msg_body = Column(String, default=None)
    created_at = Column(DateTime, default=datetime.utcnow())
    sent_at = Column(DateTime, default=None)