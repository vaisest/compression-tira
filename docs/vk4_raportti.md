# Viikkoraportti 3

## Tällä viikolla

Aikaa käytetty: 14 tuntia

Tein ensimmäisen version LZW:stä. Aluksi sen rakentaminen hoitui nopeasti, mutta nyt olen törmännyt hitauden ongelmaan. Itse algoritmi toimii kyllä, mutta  
se on käytännössä todella hidas. Se vaikuttaa olevan O(n) testauksen mukaan, mutta jokin tekee siitä erittäin hitaan. Edes ohjelman profilointi ei auttanut, sillä ohjelma näyttää pyörivän vain yksinkertaisissa kohdissa, kuten hajautustaulun tarkistuksessa, eikä hidastus tule vain yhdestä asiasta. 100 MB tekstiä (enwik8) vie 85 sekuntia, kun Huffmanin koodaus vie vain 11 sekuntia.  
Ongelma saattaisi johtua hajautustaulun ylikäytöstä, mutta kokeilin myös Trie-tietorakennetta, joka oli noin 3 kertaa hitaampi. Tämä saattaa johtua  
Pythonin hitaista olioista, mutta nyt en keksi mitään ratkaisuja.

Tosin Huffmanin koodauksessa tuli huomattua, että sen eniten aikaa kuluttavat ovat yksinkertaiset asiat, kuten merkkien laskeminen ja koodin kääntäminen, joissa  
hitaus vaikuttaa johtuvan Pythonista. Tosin toivottavasti se ei johdu kielestä.

Itse pakkaus vaikuttaa toimivan vielä hyvin vaikka siinä on selvästi parannettavaa, kuten muuttuvat koodipituudet (tällä hetkellä koodit ovat aina  
16 bittiä, vaikka niiden sisältö mahtuisi esim. kahdeksaan). Enwik8:n (100 MB Wikipediaa) pakkaus saavuttaa LZW:llä 48% pakkaussuhteen.
Testit on toteutettu ohjelman nykyiselle tilalle pois lukien ohjelman yksinkertaisen käyttöliittymän.

### Testikattavuus

Seuraava taulukko on tehty Python paketilla [pytest-cov](https://pypi.org/project/pytest-cov/):

```powershell
Desktop\pakkaus-tira> pytest --cov-report term-missing --cov=pakkaus tests/
tests\test_huffman.py ......                                [ 85%]
tests\test_lzw.py .                                         [100%]

----------- coverage: platform win32, python 3.9.4-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
pakkaus\__init__.py       1      0   100%
pakkaus\__main__.py      37     37     0%   2-58
pakkaus\huffman.py      101      0   100%
pakkaus\lzw.py           62      0   100%
---------------------------------------------------
TOTAL                   201     37    82%
```

## Seuraavaksi

Ensi viikolla toivottavasti korjaan LZW:n kohtuullisen nopeaksi tai edes selvitän mikä ongelmana on.
