# modules/video_entry.py

class VideoEntry:
    """Represents one YouTube trending video entry."""

    def __init__(self, row):
        # row is a dictionary from csv.DictReader
        self.video_id = row.get("video_id", "")
        self.trending_date = row.get("trending_date", "")
        self.title = row.get("title", "")
        self.channel_title = row.get("channel_title", "")
        self.category_id = row.get("category_id", "")
        self.publish_time = row.get("publish_time", "")
        self.tags = row.get("tags", "")
        self.views = self.to_int(row.get("views"))
        self.likes = self.to_int(row.get("likes"))
        self.dislikes = self.to_int(row.get("dislikes"))
        self.comment_count = self.to_int(row.get("comment_count"))
        self.thumbnail_link = row.get("thumbnail_link", "")
        self.comments_disabled = row.get("comments_disabled", "")
        self.ratings_disabled = row.get("ratings_disabled", "")
        self.video_error_or_removed = row.get("video_error_or_removed", "")
        self.description = row.get("description", "")

    def to_int(self, value):
        """Convert numeric text to integer safely."""
        try:
            return int(value)
        except Exception:
            return 0

    def to_dict(self):
        """Convert object back to dictionary for export."""
        return {
            "video_id": self.video_id,
            "trending_date": self.trending_date,
            "title": self.title,
            "channel_title": self.channel_title,
            "category_id": self.category_id,
            "publish_time": self.publish_time,
            "tags": self.tags,
            "views": self.views,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "comment_count": self.comment_count,
            "thumbnail_link": self.thumbnail_link,
            "comments_disabled": self.comments_disabled,
            "ratings_disabled": self.ratings_disabled,
            "video_error_or_removed": self.video_error_or_removed,
            "description": self.description
        }
