import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, \
    Unicode, Boolean
from sqlalchemy.orm import relationship
from feeds.database import Base


class Feed(Base):
    __tablename__ = "feed"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, nullable=False)
    url = Column(String(255), nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )
    feed_item = relationship('FeedItem', back_populates='feed')


class FeedItem(Base):
    __tablename__ = "feed_item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    feed_id = Column(Integer, ForeignKey('feed.id'), nullable=False)
    title = Column(String(255), nullable=True)
    link = Column(String, nullable=True)
    summary = Column(Unicode, nullable=True)
    published = Column(DateTime, nullable=True)
    is_subscribe = Column(Boolean, default=False)
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )
    feed = relationship('Feed', back_populates='feed_item')
    bookmark = relationship('Bookmark', back_populates='feed_item')


class Bookmark(Base):
    __tablename__ = "bookmark"

    id = Column(Integer, primary_key=True, autoincrement=True)
    feed_item_id = Column(Integer, ForeignKey('feed_item.id'), nullable=False)
    member_id = Column(Integer, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )
    feed_item = relationship('FeedItem', back_populates='bookmark')

