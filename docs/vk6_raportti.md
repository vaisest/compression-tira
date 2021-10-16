# Viikkoraportti 6

## Tällä viikolla

Aikaa käytetty: 6 tuntia

Suurin osa viikon ajasta on kulunut dokumentoinnin, kommenttien, testien parannukseen ja vertaisarvointiin.

Olen yrittänyt parantaa LZW:n tehoa, mutta tässä vaiheessa olen aika varma, että se on oikeasti O(n) ja syynä on Python, sillä while-loopin muuttaminen for-loopiksi nopeutti 100 MB tiedoston prosessointia kymmenellä sekunnilla. Veikkaisin, että jos ohjelma olisi tehty nopealla kielellä, se voisi oikeasti olla todella nopea, mutta se on kuitenkin käyttökelpoisen nopea nyt, sillä enwik8-tiedoston pakkaus vie "vain" 53 sekuntia.

### Testikattavuus

Seuraava taulukko on tehty Python paketilla [pytest-cov](https://pypi.org/project/pytest-cov/):

```powershell
platform win32 -- Python 3.10.0, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: C:\Users\Turtvaiz\Desktop\pakkaus-tira
plugins: cov-3.0.0
collected 9 items

tests\test_huffman.py ......                                        [ 66%]
tests\test_lzw.py ...                                               [100%]

---------- coverage: platform win32, python 3.10.0-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
pakkaus\__init__.py       3      0   100%
pakkaus\__main__.py      47     47     0%   2-71
pakkaus\huffman.py      128      0   100%
pakkaus\lzw.py           81      0   100%
---------------------------------------------------
TOTAL                   259     47    82%
```

## Seuraavaksi

Ensi viikolla teen enemmän tehokkuustestausta algoritmeille ja seuraavana taitaakin olla demotilaisuus.
