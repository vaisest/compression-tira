# Toteutus

## Huffmanin koodaus

Algoritmi käyttää pääosin binääripuuta ja minimikekoa, joilla Huffmanin puu rakennetaan. Puu on toteutettu yksinkertaisena dataluokkana ja tällä hetkellä minimikeko käyttää toistaiseksi heapq moduulia. Huffmanin puuta läpi käymällä rakennetaan sanakirja. Puun juuresta alkaen vasemmalle mentäessä lisätään 0 ja oikealla 1. Kun saavutaan lehteen, koodi tallennetaan sanakirjaan. Sanakirjalla käännetään data ja se pakataan koodatun tiedon mukaan. Paketin eteen tallennetaan sanakirjan tietojen tavupituus, ja seuraavat tavut sisältävät sanakirjan, joissa jokaiselle koodille on merkkitavu, koodin bittipituus tavussa, ja itse koodi mahdollisesti monessa tavussa. Näillä sanakirjan tiedoilla koodi voidaan purkaa pelkän tiedoston avulla.

## Lempel-Ziv-Welch

LZW:n pakkaus käyttää hajautustaulua, jonka avulla koodit muodostetaan. Purkaessa koodit voidaan muodostaa pelkällä taulukolla, sillä silloin koodeja, jotka ovat kokonaislukuja käännetään tavuiksi. LZW perustuu siihen, että merkkijonoille annetaan koko ajan pidempiä koodeja, kunnes sanakirja on täynnä (max 2^16 eli koodit olisivat pidempiä kuin 2 tavua), jolloin se tyhjennetään. Sanakirjan alussa siinä on kaikki 1 tavun merkit, joiden koodi on oma arvonsa. Purkamisessa käytetään samaa alkusanakirjaa, joten ainoa asia, joka purkamiseen tarvitaan on algoritmin tekemät koodit.

## Saavutetut aikavaativuudet

Huffmanin koodaus toimii ajassa O(nlogn + m), missä n on eri merkkien määrä ja m syötteen merkkien määrä. Käytännössä rajoittava tekijä m on syötteen merkkien laskeminen ja kääntäminen, mikä on yksinkertainen operaatio ja jossa Pythonin hitaus vaikuttaa nopeuteen suuresti.

LZW toimii ajassa O(n), missä n on syötteen määrä. Huffmaniin verrattuna jokaiselle merkille tehty operaatio on monimutkaisempi, joten vaikka algoritmi toimii lineaarisessa ajassa, se on silti suhteellisen hidas, luultavasti Pythonin hitauden takia, sillä profilointi näyttää hitauden olevan todella yksinkertaisissa operaatioissa.

## Saavutettu tehokkuus

Testissä on [enwik8-tiedosto](https://cs.fit.edu/~mmahoney/compression/textdata.html), mikä on 100MB Wikipediasta otettua XML tekstiä. Huffmanin koodaus saavuttaa 64% pakkaussuhteen ja koodaus vie noin 11 sekuntia aikaa. LZW:n pakkaussuhde on 48% ja se vie 54 sekuntia. Vertauksena Linuxin [ncompress](https://github.com/vapier/ncompress) käyttää LZW:tä ja saavuttaa 46% pakkaussuhteen ajassa 4 sekuntia. Ja modernina algoritmina [Zstd](https://github.com/facebook/zstd):n pakkaussuhde on 35.6% alle yhdessä sekunnissa oletusasetuksilla.
