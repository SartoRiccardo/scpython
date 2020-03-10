from scpython import Client, Language
from scpython.exceptions import ArticleException
import os
TOKEN = os.environ['TOKEN']

def test_get_scp():
    conn = Client(TOKEN)
    try:
        scp173 = conn.getScpArticle("SCP-173", language=Language.IT)
    except ArticleException:
        pass
