# Viikkoraportti 3

## Tällä viikolla

Aikaa käytetty: 7 tuntia

Tällä viikolla olen korjaillut hieman projektin rakennetta ja tehnyt vertaisarvoinnin. Olen myös miettinyt hieman LZW:n hitautta, mutta muihin projekteihin vertailun jälkeen vaikuttaa siltä, että toteutus on jo aika nopea Python-ohjelmaksi, ja itse Python on ainoa "ongelma". 100 megatavun Enwik8 tiedosto pakkautuu noin 130 sekuntissa.

Itse algoritmi vaikuttaa toimivan erittäin hyvin. Ainoa parannus, minkä voin keksiä siihen on koodien vaihtelevat pituudet, mutta ilman sitäkin tulokset ovat erittäin lähellä kunnollisia toteutuksia. Esimerkiksi [ncompress](https://github.com/vapier/ncompress) pakkaa Enwik8:n 45 megatavuun ja tämän projektin algoritmi 47 megatavuun. Oletettavasti kuitenkin esimerkiksi zstd on nopeampi ja tehokkaampi. Ainoa ongelma tässä vaiheessa on pakkauksen hitaus, vaikkakin se vaikuttaa selvästi olevan lineaarisesti kasvava, mutta tämä saattaa olla normaalia, kun vertailee C-koodin 6 sekuntia Pythonin 130 sekuntiin.

Projekti alkaa pikkuhiljaa vaikuttamaan valmiilta. Jotain pieniä optimointeja voisi algoritmeihin tehdä, mutta ne olisi luultavasti vaikea tehdä Pythonissa, olisivat hitaita ja eivät parantaisi pakkaustehokkuutta paljoa.

### Testikattavuus

Seuraava taulukko on tehty Python paketilla [pytest-cov](https://pypi.org/project/pytest-cov/):

```powershell
Desktop\pakkaus-tira> pytest --cov-report term-missing --cov=pakkaus tests/
tests\test_huffman.py ......                                          [ 85%]
tests\test_lzw.py .                                                   [100%]

---------- coverage: platform win32, python 3.10.0-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
pakkaus\__init__.py       3      0   100%
pakkaus\__main__.py      45     45     0%   2-68
pakkaus\huffman.py      127     15    88%   98, 256, 275, 294-296, 303-305, 318-320, 327-329
pakkaus\lzw.py           62      0   100%
---------------------------------------------------
TOTAL                   237     60    75%


============================ 7 passed in 6.51s =============================
```

## Seuraavaksi

Ensi viikolla parannan lzw.py tiedostoa lisäämällä testejä ja virheiden käsittelyä. Huffman.py puuttuvat koodirivit ovat suurimmaksi osaksi virheiden käsittelyä, jotka myös vaativat testit.
