import scpython.model.scparticle
from scpython.options import Branch, Language
from scpython.util.enum import getScpBranch, getItemByName
from scpython.exceptions import *

from threading import Thread
import json
import html
import urllib3
import re


class Client:
    """A connection to interact with Wikidot.

    **Arguments**
        wikidot_token7 :class:`str` — The user's identity.
    """

    __AJAX_CONNECTOR = "/ajax-module-connector.php"

    def __init__(self, wikidot_token7):
        self.__token = wikidot_token7
        self.__pool = urllib3.PoolManager()

    def getScpArticle(self, code, **kwargs):
        """Gets the requested SCP.

        **Arguments**
            code :class:`str` — The SCP's full code (``"SCP-XXXX-BRANCH"``).
            branch :class:`Branch` — In case the Client cannot determine which branch the SCP was originally written in, you can specify it manually.
            language :class:`Language` — The language to return the SCP in.

        **Returns**
            article :class:`Article` — The corresponding article.
        """
        branch = kwargs["branch"] if "branch" in kwargs and isinstance(kwargs["branch"], Branch) \
            else getScpBranch(code)

        if "language" not in kwargs or not isinstance(kwargs["language"], Language):
            language = getItemByName(Language, branch.name)
            if branch is Branch.INT:
                language = Language.EN
        else:
            language = kwargs["language"]

        wiki_url = Branch.INT.value if branch is not Branch.EN and language is Language.EN \
            else getItemByName(Branch, language.name).value
        url = wiki_url + code

        response = self.__pool.request(
            "GET",
            url,
            headers={"Cookie": f"wikidot_token7={self.__token}"}
        )

        if response.status == 200:
            raw_html = response.data.decode("utf-8")

            regex = {
                "id": r"WIKIREQUEST.info.pageId = (\d+);",
                "page_version": r"<div id=\"page-info\">\D+?: (\d+?), \D+?: .+?<\/div>",
                "last_change": r"<div id=\"page-info\">.+?<span class=\".+?\">(.+?)<\/span><\/div>",
                "rating": r"<span class=\"rate-points\">.+?<span class=\".+?\">((?:\+|-)\d+?)<\/span><\/span>",
            }

            scp_data = {
                "url": url,
            }
            for var in regex:
                match = re.search(regex[var], raw_html)
                result = match.group(1) if match else None
                scp_data[var] = result

            raw_tags = re.search(r"<div class=\"page-tags\">\s+<span>\s+(?:<a href=\".+?\">.+?</a>)+", raw_html) \
                .group(0)
            tags = re.findall(r"<a href=\".+?\">(.+?)</a>", raw_tags)
            scp_data = {
                **scp_data,
                "tags": tags
            }

            if scp_data["page_version"]:
                req_poster = Client.__RequestThread(self.__pool)
                req_poster.set_request(
                    "POST",
                    wiki_url + Client.__AJAX_CONNECTOR,
                    headers={"Cookie": f"wikidot_token7={self.__token}"},
                    fields={
                        "page_id": scp_data["id"],
                        "moduleName": "history/PageRevisionListModule",
                        "wikidot_token7": self.__token,
                        "options": "{\"all\":true}",
                        "page": int(scp_data["page_version"])+1,
                        "perpage": "1",
                    }
                )
                req_poster.start()

            req_page_source = Client.__RequestThread(self.__pool)
            req_page_source.set_request(
                "POST",
                wiki_url + Client.__AJAX_CONNECTOR,
                headers={"Cookie": f"wikidot_token7={self.__token}"},
                fields={
                    "page_id": scp_data["id"],
                    "moduleName": "viewsource/ViewSourceModule",
                    "wikidot_token7": self.__token,
                }
            )
            req_page_source.start()

            author = None
            if scp_data["page_version"]:
                req_poster.join()

                res_poster = req_poster.getResponse()
                poster_data = json.loads(res_poster.decode("utf-8"))
                if poster_data["status"] == "wrong_token7":
                    raise InvalidToken()

                author = None if not res_poster \
                    else re.search(
                        r"<span class=\"printuser .+?\">(?:<a .+?>)?<img .+/>(?:</a>)?(?:<a .+?>)?(.+?)(?:</a>)*</span>",
                        poster_data["body"]
                    ).group(1)

            req_page_source.join()
            res_page_source = req_page_source.getResponse()
            page_source = "" if not res_page_source \
                else json.loads(res_page_source.decode("utf-8"))["body"]
            page_source = html.unescape(
                re.match(r"<h1>.+?</h1>\s+<div class=\"page-source\">([\w\W]+)</div>", page_source)
                .group(1)
                .replace("<br />", "")
            )

            scp_data = {
                **scp_data,
                "branch": branch,
                "full_code": code,
                "page_source": page_source,
                "poster": author,
                "language": language
            }

            return scpython.model.scparticle.ScpArticle(scp_data)
        elif response.status == 404:
            if language == branch:
                raise ScpArticleNotFound(code)

            original_branch = getScpBranch(code)
            if original_branch is not branch:
                raise ScpArticleNotFound(code, branch=branch)

            exists_at_all = self.__pool.request(
                "GET",
                branch.value + code,
                headers={"Cookie": f"wikidot_token7={self.__token}"}
            ).status == 200

            if exists_at_all:
                raise ScpArticleNotTranslated(code, language)
            else:
                raise ScpArticleNotFound(code)
        else:
            raise Exception("Invalid response status")

    class __RequestThread(Thread):
        """A Thread to make requests, to speed up things.

        **Arguments**
            pool — The pool to make requests with.
        """

        def __init__(self, pool):
            super().__init__()

            self.__pool = pool
            self.__method = None
            self.__url = None
            self.__request_kwargs = {}

            self.__response = None

        def set_request(self, method, url, **kwargs):
            """Sets the request parameters.

            **Arguments**
                method :class:`str` — The HTTP Method.
                url :class:`str` — The URL to send the request to.
                request_kwargs :class:`dict` — The optional parameters to send to the request.
            """
            self.__method = method
            self.__url = url
            self.__request_kwargs = kwargs if kwargs else {}

        def run(self):
            if self.__method and self.__url:
                response = self.__pool.request(self.__method, self.__url, **self.__request_kwargs)
                if response.status == 200:
                    self.__response = response.data
                    return

            self.__response = None

        def getResponse(self):
            """Returns the last call's response.

            **Returns**
                response :class:`bytes` — The request response.
            """
            return self.__response
