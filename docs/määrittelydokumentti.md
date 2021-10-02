# (Alustava) Määrittelydokumentti

Opinto-ohjelma: Tietojenkäsittelytieteen kandiohjelma

Projektin kieli: Suomi

Ohjelmointikieli: Python

## Käytettävät algoritmit

Tavoitteena on vertailla Huffmanin koodausta ja Lempel-Ziv-Welch pakkausmenetelmää. Huffmanin koodauksen toteuttamiseen käytetään minimikekoa ja hajautustaulua (dict).

## Mitä ongelmaa ratkaistaan

Ongelmana on näiden kahden pakkausmenetelmän vertailu.
Valittuna on kaksi suhteellisen yksinkertaista, mutta erittäin suosittua menetelmää.
Modernit pakkausmenetelmät saattavat olla tehokkaampia, mutta esimerkiksi Huffmanin koodausta käytetään yhtenä vaiheena monessa eri menetelmässä.

## Ohjelman syötteet ja niiden käyttö

Ohjelman tulisi voida sekä pakata tekstiä, että purkaa jo valmiiksi pakatut tekstit.

## Tavoitetut aikavaativuudet

Huffmanin koodaus on mahdollista toteuttaa ajassa O(nlogn + m), missä n on eri merkkien määrä ja m syötteen määrä. Käytännössä rajoittava tekijä on syötteen merkkien laskeminen ja kääntäminen, mikä on yksinkertainen operaatio.

## Lähteet

- https://en.wikipedia.org/wiki/Huffman_coding

- https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch

- https://www2.cs.duke.edu/csed/curious/compression/lzw.html
