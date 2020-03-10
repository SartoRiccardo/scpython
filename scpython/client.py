import scpython.model.scparticle
from scpython.options import Branch, Language
from scpython.util.enum import getScpBranch, getItemByName

from threading import Thread
import json
import html
import urllib3
import re


class Client:
    """
    A client to communicate with Wikidot.

    Attributes:
        __token (str): The user's identity.
        __pool: The pool to make requests with.
    """

    __AJAX_CONNECTOR = "/ajax-module-connector.php"

    def __init__(self, wikidot_token7):
        """Registers the token.

        Args:
            wikidot_token7 (str): The user's Wikidot token.
        """
        self.__token = wikidot_token7
        self.__pool = urllib3.PoolManager()

    def getScpArticle(self, code, branch=None, language=None):
        """Gets an SCP from a certain wiki.

        Args:
            code (str): The SCP's code.
            branch (scpython.options.Branch): The SCP's original branch.
            language (scpython.options.Language): The language to return the SCP in.
        """
        branch = branch if branch is not None and isinstance(branch, Branch) \
            else getScpBranch(code)

        if language is None:
            language = getItemByName(Language, branch.name)
            if branch is Branch.INT:
                language = Language.EN

        wiki_url = branch.value
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
                result = re.search(regex[var], raw_html).group(1)
                scp_data[var] = result

            raw_tags = re.search(r"<div class=\"page-tags\">\s+<span>\s+(?:<a href=\".+?\">.+?</a>)+", raw_html) \
                .group(0)
            tags = re.findall(r"<a href=\".+?\">(.+?)</a>", raw_tags)
            scp_data = {
                **scp_data,
                "tags": tags
            }

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

            req_poster.join()
            req_page_source.join()

            res_poster = req_poster.getResponse()
            author = None if not res_poster \
                else re.search(
                    r"<a href=\".+?\" onclick=\".+?\" ?>(.+)</a></span></td>",
                    json.loads(res_poster.decode("utf-8"))["body"]
                ).group(1)

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
        else:
            raise Exception("Invalid response status")

    class __RequestThread(Thread):
        """A Thread to make requests, to speed up things.

        Attributes:
            __pool: The pool to make requests with.
            __method (str): The HTTP Method.
            __url (str): The URL to send the request to.
            __request_kwargs (dict): The optional parameters to send to the request.
            __response: The request response.
        """

        def __init__(self, pool):
            super().__init__()

            self.__pool = pool
            self.__method = None
            self.__url = None
            self.__request_kwargs = {}

            self.__response = None

        def set_request(self, method, url, **kwargs):
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
            return self.__response
