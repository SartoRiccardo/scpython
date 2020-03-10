from enum import Enum


class Branch(Enum):
    """All SCP official branches.

    Each variable is set to the branch's link.

    Available branches are:
        * INT
        * EN
        * RU
        * KO
        * CN
        * FR
        * PL
        * ES
        * TH
        * JP
        * DE
        * IT
        * UA
        * PT
        * BR
        * CZ
    """

    INT = "http://scp-int.wikidot.com/"
    EN = "http://www.scp-wiki.net/"
    RU = "http://scp-ru.wikidot.com/"
    KO = "http://ko.scp-wiki.net/"
    CN = "http://scp-wiki-cn.wikidot.com/"
    FR = "http://fondationscp.wikidot.com/"
    PL = "http://scp-wiki.net.pl/"
    ES = "http://lafundacionscp.wikidot.com/"
    TH = "http://scp-th.wikidot.com/"
    JP = "http://scp-jp.wikidot.com/"
    DE = "http://scp-wiki-de.wikidot.com/"
    IT = "http://fondazionescp.wikidot.com/"
    UA = "http://scp-ukrainian.wikidot.com/"
    PT = "http://scp-pt-br.wikidot.com/"
    BR = PT
    CZ = "http://scp-cs.wikidot.com/"
