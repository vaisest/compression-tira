# Viikkoraportti 1

## Tällä viikolla

Aikaa käytetty: 7 tuntia

Aloitin tekemään itse projektin koodia. Osa ajasta meni Pythonin projektimuodon opettelemiseen, mutta valmiina on nyt ensimmäinen toteutus  
Huffmanin koodauksesta. Ohjelmalla pakkaa ja purkaa sille annetun merkkijonon, joten itse algoritmi vaikuttaa toimivan oikein.  
Testit on toteutettu ohjelman nykyiselle tilalle pois lukien ohjelman yksinkertaisen käyttöliittymän.

### Testikattavuus

Seuraava taulukko on tehty Python paketilla [pytest-cov](https://pypi.org/project/pytest-cov/):

```powershell
Desktop\pakkaus-tira> pytest --cov-report term-missing --cov=pakkaus tests/
tests\test_huffman.py ...  [100%]

----------- coverage: platform win32, python 3.9.4-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
pakkaus\__init__.py       2      0   100%
pakkaus\__main__.py      11     11     0%   1-18
pakkaus\huffman.py       55      0   100%
---------------------------------------------------
TOTAL                    68     11    84%

```

## Seuraavaksi

Ensi viikolla tavoitteena olisi luultavasti tehdä mahdolliseksi tiedostojen tallennus, muuttaa Huffmanin koodaus bittipohjaiseksi.
