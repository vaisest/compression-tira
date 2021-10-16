# Testausdokumentti

Ohjelman testaus on toteutettu Pythonin omalla unittest-moduulilla. Tyyppitarkastukseen käytetään pakettia mypy ja koodin laadun tarkkailemiseen työkalua pylint, vaikkakin kaikki koodi on jo formatoitu blackilla.

## Yksikkötestit

Yksikkötestit voidaan suorittaa komennolla `python -m unittest`. Testikattavuus saadann komennolla `pytest --cov-report term-missing --cov=pakkaus tests/`, laadun tarkastus komennolla `pylint pakkaus` ja tyyppitarkastus komennolla `mypy -m pakkaus`.

Projektissa on seuraavat Huffman testit:

1. test_huffman.test_printing

   - Testaa Huffmanin puun tietorakenteen tulostamista.

2. test_huffman.test_pack_data

   - Testaa tiedon pakkaamista yksimerkkisellä syötteellä, yksinkertaisella pakatulla syötteellä, ja uudestaan suuremmalla syötteellä. Testaa virhettä tyhjällä syötteellä. Vertailee oletettua ja tuloksena saatua dataa.

3. test_huffman.test_unpack_data

   - Testaa tiedon purkamista yksimerkkisellä syötteellä, yksinkertaisella pakatulla syötteellä, ja uudestaan suuremmalla syötteellä. Testaa virhettä tyhjällä syötteellä. Vertailee tuloksina saatuja merkkijonoja.

4. test_huffman.test_pack

   - Testaa sanakirjan ja datan pakkaamista.

5. test_huffman.test_unpack

   - Testaa pakatun sanakirjan ja datan purkamista.

6. test_huffman.test_packing_files

   - Testaa tiedoston pakkaamista ja purkamista. Varmistaa, että alkuperäinen tiedosto ja lopputulos ovat sama. Varmistaa myös, että virheiden ilmoittaminen toimii tiedostojen kanssa.

Ja seuraavat LZW testit:

1. test_lzw.test_compress

   - Testaa tiedon pakkaamista yksimerkkisellä syötteellä, yksinkertaisella pakatulla syötteellä, ja uudestaan suuremmalla syötteellä. Testaa virhettä tyhjällä syötteellä. Vertailee oletettua ja tuloksena saatua dataa.

2. test_lzw.test_uncompress

   - Testaa tiedon purkamista yksimerkkisellä syötteellä, yksinkertaisella pakatulla syötteellä, ja uudestaan suuremmalla syötteellä. Testaa virhettä tyhjällä syötteellä. Vertailee tuloksina saatuja merkkijonoja.

3. test_lzw.test_compressing_files

   - Testaa suuren tiedoston pakkausta ja purkamista. Varmistaa, että alkuperäinen tiedosto ja lopputulos ovat sama. Varmistaa myös, että virheiden ilmoittaminen toimii tiedostojen kanssa.

### Testikattavuus

Pytest-cov komennosta saatu testikattavuus

```
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
