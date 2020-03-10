from scpython.model.article import Article
from scpython.options import Branch, Language
import re


class ScpArticle(Article):
    """Represents an SCP Article on Wikidot.

    **Attributes**
        page_source :class:`str` — The SCP's text.
        number :class:`int` — The SCP's number.
        branch :class:`Branch` — The SCP's original branch.
        language :class:`Language` — The fetched SCP's language.
        is_joke :class:`boolean` — Whether the SCP has a -J flag.
        full_code :class:`str` — The SCP's full code (``"SCP-XXXX-LANG-J"``).
    """

    def __init__(self, data):
        super().__init__(data)

        self.page_source = data["page_source"]
        self.is_joke = "joke" in self.tags
        self.full_code = data["full_code"]
        self.number = int(re.search(r"(\d+)", self.full_code).group(1))
        self.language = data["language"]
        self.branch = data["branch"]

    def toJson(self):
        """Turns the data into a dictionary.

        **Return**
            json :class:`dict` — A dictionary containing all of the SCP article's data.
        """
        article = super().toJson()
        return {
            **article,
            "page_source": self.page_source,
            "is_joke": self.is_joke,
            "number": self.number,
            "full_code": self.full_code,
            "language": self.language,
            "branch": self.branch
        }
