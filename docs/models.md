Here are the data models that are used in the library.

# scpython.model.Article

Article is an abstract class.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | `int` | The article ID.
| rating | `int` | The article's rating.
| url | `str` | The article's URL.
| tags | `str[]` | The article's tags.
| poster | `str` | The user who first posted the article.
| page_version | `int` | The number of changes the page went through.
| last_change | `date` | The day the page was last changed.

# scpython.model.ScpArticle

Subclass of Article, as such it has all of Article's fields.

| Field | Type | Description |
| ----- | ---- | ----------- |
| page_source | `str` | The SCP's text.
| number | `int` | The SCP's number.
| branch | `Branch` | The SCP's original branch.
| language | `Language` | The fetched SCP's language.
| is_joke | `boolean` | Whether the SCP has a -J flag.
| full_code | `str` | The SCP's full code (SCP-XXXX-LANG-J).

# scpython.Branch

Branch is an enum with the following fields:

`INT`, `EN`, `RU`, `KO`, `CN`, `FR`, `PL`, `ES`, `TH`, `JP`, `DE`, `IT`, `UA`, `PT`, `BR`, `CZ`

# scpython.Language

Language is an enum with the following fields:

`EN`, `RU`, `KO`, `CN`, `FR`, `PL`, `ES`, `TH`, `JP`, `DE`, `IT`, `UA`, `PT`, `BR`, `CZ`
