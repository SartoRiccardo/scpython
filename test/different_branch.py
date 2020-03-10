from scpython import Client
from scpython.exceptions import ArticleException
import os
TOKEN = os.environ['TOKEN']

def test_get_scp():
    conn = Client(TOKEN)
    try:
        scp040it = conn.getScpArticle("SCP-040-IT")
    except ArticleException:
        pass
