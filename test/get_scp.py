from scpython import Client
from scpython.exceptions import ArticleException
import os
TOKEN = os.environ['TOKEN']

def test_get_scp():
    conn = Client(TOKEN)
    try:
        scp173 = conn.getScpArticle("SCP-173")
    except ArticleException:
        pass
