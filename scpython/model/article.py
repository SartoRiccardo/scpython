from abc import ABC
from datetime import datetime


class Article(ABC):
    """Represents any article on Wikidot.

    **Attributes**
        id :class:`int` — The article ID.

        rating :class:`int` — The article's rating.

        url :class:`str` — The article's URL.

        tags :class:`str[]` — The article's tags.

        poster :class:`str` — The user who first posted the article.

        page_version :class:`int` — The number of changes the page went through.

        last_change :class:`datetime` — The day the page was last changed.
    """

    def __init__(self, data):
        self.id = int(data["id"])
        self.url = data["url"]
        self.tags = data["tags"]
        self.page_version = int(data["page_version"]) if data["page_version"] else None
        if isinstance(data["last_change"], datetime):
            self.last_change = data["last_change"]
        elif isinstance(data["last_change"], str):
            self.last_change = datetime.strptime(data["last_change"], "%d %b %Y %H:%M")
        else:
            self.last_change = None
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
        """Turns the data into a dictionary.

        **Returns**
            json :class:`dict` — A dictionary containing all of the article's data.
        """
        return {
            "id": self.id,
            "rating": self.rating,
            "url": self.url,
            "tags": self.tags,
            "poster": self.poster,
            "page_version": self.page_version,
            "last_change": self.last_change,
        }
