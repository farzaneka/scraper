import json

import feedparser
from nameko.rpc import rpc

from feeds.database import SessionLocal
from feeds.models import Feed, FeedItem, Bookmark
from feeds.schemas import FeedSchema, BookmarkSchema


class FeedsService:
    name = 'feeds'
    session = SessionLocal()

    @rpc
    def create_feed(self, url, member_id):
        feed = Feed(
            url=url,
            member_id=member_id,
        )
        self.session.add(feed)
        self.session.commit()
        self.session.refresh(feed)

        feed = FeedSchema().dump(feed)
        return json.dumps(feed)

    @rpc
    def update_feed(self, feed_id, url):
        feed = self.session.query(Feed) \
            .filter(Feed.id == feed_id) \
            .one_or_none()

        if feed is None:
            return Exception("Feed not found")

        feed.url = url
        self.session.commit()
        self.session.refresh(feed)
        feed = FeedSchema().dump(feed)
        return json.dumps(feed)

    @rpc
    def create_feed_items(self, feed_url, feed_id):
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            try:
                feed_item = FeedItem(
                    feed_id=feed_id,
                    title=entry.title,
                    link=entry.link,
                    summary=entry.summary,
                    published=entry.published,
                )
                self.session.add(feed_item)
            except Exception as ex:
                self.session.rollback()
                raise Exception(f'Transaction rollback: {ex}')
            else:
                self.session.commit()
                self.session.refresh(feed_item)

        return json.dumps({"feed_url": feed_url})

    @rpc
    def subscribe_feed_item(self, feed_id):
        feed_items = self.session.query(FeedItem) \
            .filter(FeedItem.feed_id == feed_id) \
            .all()

        if len(feed_items) == 0:
            return Exception("Feed item not found")

        for feed_item in feed_items:
            feed_item.is_subscribe = True
            self.session.commit()
            self.session.refresh(feed_item)

        return json.dumps({"status_code": 200})

    @rpc
    def create_bookmark(self, feed_item_id, member_id):
        feed_item = self.session.query(FeedItem) \
            .filter(FeedItem.id == feed_item_id) \
            .one_or_none()

        if feed_item is None:
            return Exception("Feed item not found")

        bookmark = Bookmark(
            feed_item_id=feed_item.id,
            member_id=member_id,
        )
        self.session.add(bookmark)
        self.session.commit()
        self.session.refresh(bookmark)

        bookmark = BookmarkSchema().dump(bookmark)
        return json.dumps(bookmark)

    @rpc
    def list_bookmark(self, member_id):
        bookmarks = self.session.query(Bookmark) \
            .filter(Bookmark.member_id == member_id) \
            .all()

        if len(bookmarks) == 0:
            return Exception("Feed item not found")

        result = []
        for bookmark in bookmarks:
            bookmark = BookmarkSchema().dump(bookmark)
            result.append(bookmark)

        return json.dumps({"bookmarks": result})

