from datetime import datetime
import uuid
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UUID,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from backend.utils.base import Base

role = Table(
    "role",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)


user_chat_members = Table(
    "user_chat_members",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("user.id")),
    Column("chat_id", UUID, ForeignKey("group_chats.id")),
)

user_chat_bans = Table(
    "user_chat_bans",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("user.id")),
    Column("chat_id", UUID, ForeignKey("group_chats.id")),
)

user_post = Table(
    "user_post",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("user.id")),
    Column("post_id", UUID, ForeignKey("posts.id")),
)
user_community = Table(
    "user_community",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("user.id")),
    Column("community_id", UUID, ForeignKey("communities.id")),
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    username = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(role.c.id))
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)

    @hybrid_property
    def chats(self):
        return self.personal_chats + self.group_chats

    personal_chats = relationship(
        "PersonalChat", foreign_keys="[PersonalChat.sender_id]", backref="users"
    )
    group_chats = relationship(
        "GroupChat", foreign_keys="[GroupChat.owner]", backref="users"
    )
    posts = relationship("Post", secondary="user_post", backref="user")
    # photos = relationship("photos", backref="user", lazy="dynamic")

    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


class PersonalChat(Base):
    __tablename__ = "personal_chats"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    receiver_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, unique=True
    )
    messages = relationship("PersonalMessage", backref="chat")


class GroupChat(Base):
    __tablename__ = "group_chats"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    owner = Column(ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("GroupMessage", backref="chat")
    members = relationship("User", secondary="user_chat_members")


class PersonalMessage(Base):
    __tablename__ = "personal_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    sender_id = Column(UUID, ForeignKey("user.id"))
    receiver_id = Column(UUID, ForeignKey("personal_chats.receiver_id"), nullable=True)

    user = relationship("User", backref=backref("personal_messages", order_by=id))


class GroupMessage(Base):
    __tablename__ = "group_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    chat_id = Column(UUID, ForeignKey("group_chats.id"), nullable=True)
    sender_id = Column(UUID, ForeignKey("user.id"))

    user = relationship("User", backref=backref("group_messages", order_by=id))


class Community(Base):
    __tablename__ = "communities"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255))
    description = Column(Text)
    owner = Column(ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), index=True)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    content = Column(Text, index=True)
    owner_id = Column(ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, index=True)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    post_id = Column(UUID, ForeignKey("posts.id"))
    parent_id = Column(UUID, ForeignKey("comments.id"))

    children = relationship(
        "Comment",
        cascade="all, delete-orphan",
        backref=backref("parent", remote_side=[id]),
    )
    post = relationship("Post", back_populates="comments")


UserChatBans = user_chat_bans
UserChatMember = user_chat_members
