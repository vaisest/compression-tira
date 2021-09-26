# Viikkoraportti 3

## Tällä viikolla

Aikaa käytetty: 11 tuntia

Muutin Huffmanin koodauksen toteutuksen bittipohjaiseksi. Tähän kului paljon enemmän aikaa kuin ajattelin, että siihen menisi, sillä Pythonissa ainoa tavuja käsittelevä tietotyyppi on bytes, mikä on käytännössä lista 8-bittisiä kokonaislukuja. Ensinnäkin tämä vaikeutti yksittäisten bittien prosessointia ja lisäksi koodien muuttaminen kokonaisluvuksi pudotti alusta kaikki nollat, mikä rikkoi koodin. Ja itse koodattu data säilyy kokonaislukuna, koska sen eteen lisätään bitti 1, jottei alun nollat putoa. Epävirallisia tietorakennepaketteja ilmeisesti on, mutta niiden käyttö taitaa olla hieman outoa tira projektissa.

Aikaisemmin sanakirja tallennetiin avaimina (kokonaisluku) ja merkkijonoina. Nyt jokainen pari tallennetaan muodossa [merkki, koodin bittipituus, koodi kokonaislukuna].
Pikaisella testillä tämä säästi huimat 2 kilotavua 100 megatavun Wikipedia tekstitiedoston pakkaamisessa, vaikka jokainen sanakirjan pari vie enintään 3-4 tavua. Se voi kuitenkin olla suhteellisen suuri hyöty muun kuin teksin pakkaamisessa.

Ohjelmalla kuitenkin nyt pakkaa ja purkaa sille annetun merkkijonon lisäksi nyt tiedostoja, ja pienen testauksen pohjalta tulokset ovat uskottavia.
Esimerkiksi Wikipedia-artikkelin koko pieneni noin 35%.  
Testit on toteutettu ohjelman nykyiselle tilalle pois lukien ohjelman yksinkertaisen käyttöliittymän.

### Testikattavuus

Seuraava taulukko on tehty Python paketilla [pytest-cov](https://pypi.org/project/pytest-cov/):

```powershell
Desktop\pakkaus-tira> pytest --cov-report term-missing --cov=pakkaus tests/
tests\test_huffman.py ...  [100%]

----------- coverage: platform win32, python 3.9.4-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
pakkaus\__init__.py       1      0   100%
pakkaus\__main__.py      25     25     0%   2-41
pakkaus\huffman.py      100      0   100%
---------------------------------------------------
TOTAL                   126     25    80%

```

## Seuraavaksi

Ensi viikolla on tarkoitus aloittaa LZW:n koodaaminen.
