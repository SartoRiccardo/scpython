Reference
=========

The :class:`Client` class is what is used to make all requests.

Example
-------

Below is a simple example of how to make requests::

    from scpython import Client

    conn = Client("YOUR-TOKEN")
    scp173 = conn.getScpArticle("SCP-173")

    print(scp173.page_source)

You can get SCPs from different branches::

    from scpython import Client

    conn = Client("YOUR-TOKEN")
    scp040it = conn.getScpArticle("SCP-040-IT")

    print(scp040it.page_source)

And in any language it's been translated to::

    from scpython import Client, Language

    conn = Client("YOUR-TOKEN")
    scp173 = conn.getScpArticle("SCP-173", language=Language.IT)

    print(scp173.page_source)

Class Reference
---------------

.. module:: scpython
.. autoclass:: Client
    :members: