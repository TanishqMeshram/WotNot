from sqlalchemy import Column, Integer, String, Text, DateTime , Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, index=True)
    wa_id = Column(String, index=True)  # WhatsApp ID of the user
    message_id = Column(String)  # Unique message ID
    # message_id = Column(String, unique=True)  # Unique message ID
    phone_number_id = Column(String)  # Phone number ID
    message_content = Column(Text)  # Message body
    timestamp = Column(DateTime, default=datetime.utcnow)  # Message timestamp
    context_message_id = Column(String, nullable=True)  # ID of the message that this is replying to
    message_type = Column(String)  # Type of message (e.g., text, image)

class First_Conversation(Base):
    __tablename__ = 'first_conversations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_account_id = Column(String, nullable=False)  # ID of the business account
    sender_wa_id = Column(String, nullable=False)  # WhatsApp ID of the sender
    receiver_wa_id = Column(String, nullable=False)  # WhatsApp ID of the recipient
    first_chat_time = Column(DateTime)  # Timestamp for the first chat
    active = Column(Boolean, default=True)  # Status of the conversation

    def __init__(self, business_account_id, sender_wa_id, receiver_wa_id):
        self.business_account_id = business_account_id
        self.sender_wa_id = sender_wa_id
        self.receiver_wa_id = receiver_wa_id
        self.first_chat_time = datetime.now()