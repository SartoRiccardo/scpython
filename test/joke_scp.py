from scpython import Client
from scpython.exceptions import ArticleException
import os
TOKEN = os.environ['TOKEN']

def test_get_scp():
    conn = Client(TOKEN)
    try:
        scp049j = conn.getScpArticle("SCP-049-J")
    except ArticleException:
        pass
