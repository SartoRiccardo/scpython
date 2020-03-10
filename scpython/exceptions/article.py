class ArticleException(Exception):
    """A generic exception that happened with an article."""
    pass


class ScpArticleNotFound(ArticleException):
    """Is thrown when an SCP Article does not exist in any branch."""
    def __init__(self, code, branch=None):
        on_branch = f" on branch -{branch.name}" if branch else ""
        super().__init__(f"SCP '{code}' does not exist{on_branch}.")


class ScpArticleNotTranslated(ArticleException):
    """Is thrown when an SCP Article exists, but was not translated in the specified language."""
    def __init__(self, code, language):
        super().__init__(f"SCP '{code}' was not translated to {language}")
