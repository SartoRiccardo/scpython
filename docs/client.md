
The `Client` class is what is used to make all requests.

# Simple usage

Below is a simple example of how to make requests.
```python
from scpython import Client

conn = Client("YOUR-TOKEN")
scp173 = conn.getScpArticle("SCP-173")

print(scp173.page_source)
```

You can get SCPs from different branches.
```python
from scpython import Client

conn = Client("YOUR-TOKEN")
scp040it = conn.getScpArticle("SCP-040-IT")

print(scp040it.page_source)
```

...and in any language it's been translated to.
```python
from scpython import Client, Language

conn = Client("YOUR-TOKEN")
scp173 = conn.getScpArticle("SCP-173", language=Language.IT)

print(scp173.page_source)
```

# Reference

### **Client** *(access_token)*

The client used to communicate with Wikidot.

**Arguments:**
+ *access_token* `str`: A valid wikidot token7.

#### getScpArticle(code, branch=None, language=None)

Gets the requested SCP.

**Arguments:**
+ *code* `str`: The SCP's full code (SCP-XXXX-BRANCH).
+ *branch* [`Branch`](./models.md): In case the Client cannot determine which branch the SCP was originally written in, you can specify it manually.
+ *language* [`Language`](./models.md): The language to return the SCP in.

**Returns:** [`ScpArticle`](./models.md) The article that was fetched.