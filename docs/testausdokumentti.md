# Testausdokumentti

Ohjelman testaus on toteutettu Pythonin omalla unittest-moduulilla. Tyyppitarkastukseen käytetään pakettia mypy ja koodin laadun tarkkailemiseen työkalua pylint,  
vaikkakin kaikki koodi on jo formatoitu blackilla.

## Yksikkötestit

Yksikkötestit voidaan suorittaa komennolla `python -m unittest`. Testikattavuus saadann komennolla `pytest --cov-report term-missing --cov=pakkaus tests/`, laadun tarkastus komennolla `pylint pakkaus` ja tyyppitarkastus komennolla `mypy -m pakkaus`.

Projektissa on seuraavat testit:

1. test_huffman.test_printing

   - Testaa Huffmanin puun tietorakenteen tulostamista.

2. test_huffman.test_encode

   - Testaa tiedon pakkausta yksinkertaisella syötteellä, ja uudestaan suuremmalla syötteellä. Vertailee oletettua ja
     tuloksena saatua sanakirjaa ja dataa.

3. test_huffman.test_decode

   - Testaa tiedon purkamista yksinkertaisella sanakirja- ja datasyötteellä, ja uudestaan suuremmalla syötteellä. Vertailee tuloksena saatua merkkijonoa.

4. test_huffman.test_pack

   - Testaa sanakirjan ja datan pakkaamista.

5. test_huffman.test_unpack

   - Testaa pakatun sanakirjan ja datan purkamista.

6. test_huffman.test_packing_files
   - Testaa tiedoston pakkaamista ja purkamista. Varmistaa, että alkuperäinen tiedosto
     ja lopputulos ovat sama.

### Testikattavuus

Pytest-cov komennosta saatu testikattavuus

```
========================= test session starts =========================
platform win32 -- Python 3.9.4, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
plugins: cov-2.12.1
collected 6 items

tests\test_huffman.py ......                                     [100%]

----------- coverage: platform win32, python 3.9.4-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
pakkaus\__init__.py       1      0   100%
pakkaus\__main__.py      25     25     0%   2-41
pakkaus\huffman.py      100      0   100%
---------------------------------------------------
TOTAL                   126     25    80%
```
