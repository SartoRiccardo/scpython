from abc import ABC
from datetime import datetime


class Article(ABC):
    """Represents any Article on Wikidot.

    Attributes:
        id (int): The article ID.
        rating (int): The article's rating.
        url (str): The article's URL.
        tags (str[]): The article's tags.
        poster (str): The user who first posted the article.
        page_version (int): The number of changes the page went through.
        last_change (date): The day the page was last changed.
    """

    def __init__(self, data):
        """Parses the raw values from the data.

        Args:
            data (dict): The raw data from Wikidot.
        """
        self.id = int(data["id"])
        self.url = data["url"]
        self.tags = data["tags"]
        self.page_version = int(data["page_version"])
        self.last_change = data["last_change"] if isinstance(data["last_change"], datetime) \
            else datetime.strptime(data["last_change"], "%d %b %Y %H:%M")
        self.poster = data["poster"]

        self.rating = None
        rating = data["rating"]
        if isinstance(rating, int):
            self.rating = rating
        elif isinstance(rating, str):
            if rating.isnumeric():
                self.rating = rating
            elif len(rating) > 2 and rating[0] == "+":
                self.rating = int(rating[1:])

    def toJson(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "url": self.url,
            "tags": self.tags,
            "poster": self.poster,
            "page_version": self.page_version,
            "last_change": self.last_change,
        }

