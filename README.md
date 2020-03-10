# SCPython 

A package to fetch data from the SCP Foundation Wiki.

| Resource | Badge |
| -------- | ----- |
| Documentation | [![Documentation Status](https://readthedocs.org/projects/scpython/badge/?version=latest)](https://scpython.readthedocs.io/en/latest/?badge=latest) |
| Status | [![Build Status](https://travis-ci.org/SartoRiccardo/scpython.svg?branch=master)](https://travis-ci.org/SartoRiccardo/scpython) |

## Installation and Usage

This library can be found with `pip`.

`pip install scpython`

Once installed, all requests are handled with a `Client` object:
```python
from scpython import Client
from config import YOUR_TOKEN

conn = Client(YOUR_TOKEN)
scp173 = conn.getScpArticle("SCP-173")

print(scp173.page_source)
```

For more information, refer to the [documentation](https://scpython.readthedocs.io/en/latest).

## Credit

This app uses content from the SCP Foundation, which is licensed by CC-SA 3.0. Here are the link to all its branches:

[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-400.png" alt="EN" width="100">](http://www.scp-wiki.net/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-ru-400.png" alt="RU" width="100">](http://scp-ru.wikidot.com/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-ko-400.png" alt="KO" width="100">](http://ko.scp-wiki.net/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-cn-400.png" alt="CN" width="100">](http://scp-wiki-cn.wikidot.com/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-fr-400.png" alt="FR" width="100">](http://fondationscp.wikidot.com/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-pl-400.png" alt="PL" width="100">](http://scp-wiki.net.pl/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-es-400.png" alt="ES" width="100">](http://lafundacionscp.wikidot.com/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-th-400.png" alt="TH" width="100">](http://scp-th.wikidot.com/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-jp-400.png" alt="JP" width="100">](http://scp-jp.wikidot.com/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-de-400.png" alt="DE" width="100">](http://scp-wiki-de.wikidot.com/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-it-400.png" alt="IT" width="100">](http://fondazionescp.wikidot.com/)
[<img src="http://scp-wiki.wdfiles.com/local--files/scp-international/scp-logo-ua-400.png" alt="UA" width="100">](http://scp-ukrainian.wikidot.com/)
[<img src="http://scp-wiki.wdfiles.com/local--files/scp-international/scp-logo-pt-400.png" alt="PT" width="100">](http://scp-pt-br.wikidot.com/)
[<img src="http://scp-int.wdfiles.com/local--files/main/scp-logo-cs-400.png" alt="CS" width="100">](http://scp-ru.wikidot.com/)
[<img src="http://o5command-int.wdfiles.com/local--files/tech-team:graphic-templates/scp-logo-int-400.png" alt="INT" width="100">](http://scp-int.wikidot.com/)
