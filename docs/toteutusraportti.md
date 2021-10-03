# Toteutus

## Huffmanin koodaus

Algoritmi käyttää pääosin binääripuuta ja minimikekoa, joilla Huffmanin puu rakennetaan. Puu on toteutettu yksinkertaisena dataluokkana ja tällä hetkellä minimikeko käyttää toistaiseksi heapq moduulia. Huffmanin puuta läpi käymällä rakennetaan sanakirja. Puun juuresta alkaen vasemmalle mentäessä lisätään 0 ja oikealla 1. Kun saavutaan lehteen, koodi tallennetaan sanakirjaan. Sanakirjalla käännetään data ja se pakataan koodatun tiedon mukaan. Paketin eteen tallennetaan sanakirjan tietojen tavupituus, ja seuraavat tavut sisältävät sanakirjan, joissa jokaiselle koodille on merkkitavu, koodin bittipituus tavussa, ja itse koodi mahdollisesti monessa tavussa. Näillä sanakirjan tiedoilla koodi voidaan purkaa pelkän tiedoston avulla.

## Lempel-Ziv-Welch

LZW:n pakkaus käyttää hajautustaulua, jonka avulla koodit muodostetaan. Purkaessa koodit voidaan muodostaa pelkällä taulukolla, sillä silloin koodeja, jotka ovat kokonaislukuja käännetään tavuiksi.
