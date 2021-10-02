"Tämä moduuli toteuttaa Huffmanin koodauksen Tiralabraa varten."
import heapq
from collections import Counter
from dataclasses import dataclass
from textwrap import indent
from typing import Optional


@dataclass(order=False)
class _HuffmanNode:
    """
    Solmuluokka, joka toteuttaa Huffmanin puu.
    Solmussa arvo (käytännössä merkin frekvenssi) ja
    itse merkki ovat pakollisia. Vasen ja oikea alasolmu
    ovat vapaaehtoisia.
    """

    frequency: int
    symbol: int
    left: Optional["_HuffmanNode"] = None
    right: Optional["_HuffmanNode"] = None

    def __lt__(self, other) -> bool:
        return (self.frequency, self.symbol) < (other.frequency, other.symbol)

    def __str__(self) -> str:
        # koska SyntaxError: f-string expression part cannot include a backslash:
        tab = "\t"

        if not self.left or not self.right:
            return f"{bin(self.symbol)}: {self.frequency}"

        return (
            f"{bin(self.symbol)}: {self.frequency}\n"
            + indent(f"{self.right.__str__()}\n", tab)
            + indent(f"{self.left.__str__()}\n", tab)
        )


def _generate_tree(data: bytes) -> _HuffmanNode:
    """
    Hyväksyy tavuja ja palauttaa niistä tehdyn
    Huffmanin puun.
    """

    # Counter laskee jokaisen tavun frekvenssin
    # tässä kohtaa tulee huomattua, että bytes on enemmänkin
    # lista 8-bittisiä kokonaislukuja, joten tyyppi
    # on dict[int, int]
    frequencies: dict[int, int] = Counter(data)

    # minimikeko
    heap: list[_HuffmanNode] = []

    # jokaiselle merkille tehdään lehtisolmu, jossa solmun
    # todennäköisyys on kyseisen tavun määrä
    for byte, freq in zip(frequencies, frequencies.values()):
        heapq.heappush(heap, _HuffmanNode(freq, byte))

    while len(heap) > 1:
        # keosta otetaan kaksi pienintä
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)

        # näistä tehdään uusi solmu, jonka lapset ovat nämä kaksi solmua
        # uuden solmun arvo on sen lapsien arvon summa
        internal_node = _HuffmanNode(
            first.frequency + second.frequency,
            first.symbol + second.symbol,
            first,
            second,
        )

        # uusi solmu lisätään takaisin kekoon
        heapq.heappush(heap, internal_node)

    # jäljelle jäävä solmu on puun juuri
    return heap[0]


def _generate_dictionary(tree: _HuffmanNode) -> dict[int, str]:
    """
    Funktio hyväksyy syötteenä Huffmanin puun ja muuttaa sen
    sanakirjaksi.
    """

    # koodit ovat siis merkkijonoja syystä, että
    # pythonissa ei vaikuta olevan mitään parempaa
    # tapaa lisätä bittejä toisiinsa
    codes: dict[int, str] = {}

    # puu käydään läpi rekursiivisesti ja vasemmalle mentäessä koodiin lisätään 0,
    # ja oikealle mentäessä 1
    # kun saavutaan lehtisolmuun, koodi lisätään sanakirjaan
    def recurse(node: _HuffmanNode, codes: dict, bits: str) -> None:
        if node.left and node.right:
            recurse(node.left, codes, bits + "0")
            recurse(node.right, codes, bits + "1")
        else:
            # lehtisolmu
            codes[node.symbol] = bits

    recurse(tree, codes, "")

    return codes


def _apply_dictionary_to_data(data: bytes, codes: dict[int, str]) -> str:
    "Koodaa syötetavut sanakirjan avulla ja palauttaa koodatun bittijonon."

    return "".join([codes[byte] for byte in data])


def encode_string(string: str) -> tuple[dict[int, str], bytes]:
    """
    Yksinkertainen apufunktio joka muuttaa syötemerkkijonon tavuiksi ja
    suorittaa funktion encode_data() niillä.
    """
    return encode_data(bytes(string, "UTF-8"))


def encode_data(data: bytes) -> tuple[dict[int, str], bytes]:
    """
    Apufunktio joka tekee syötemerkkijonolle Huffmanin puun,
    puusta sanakirjan ja koodaa merkkijonon sen avulla.
    Palauttaa dict-tyypin, joka sisältää sanakirjan, ja bittijonon.
    """

    tree = _generate_tree(data)

    dictionary = _generate_dictionary(tree)

    # bittimerkkijonoon lisätään bitti yksi eteen ettei muunnos
    # kokonaisluvuksi poista alusta kaikkia nollia
    encoded_string = "1" + _apply_dictionary_to_data(data, dictionary)

    # bittimerkkijono muutetaan kokonaisluvuksi
    encoded_int = int(encoded_string, 2)

    # kokonaisluku muutetaan tavuiksi
    encoded_data = encoded_int.to_bytes((encoded_int.bit_length() + 7) // 8, "big")

    return dictionary, encoded_data


def decode_to_string(base_dictionary: dict[int, str], data: bytes) -> str:
    """
    Yksinkertainen apufunktio purkaa anetun syötteen ja muuntaa saadut
    tavut merkkijonoksi. Käyttää funktiota decode_to_data().
    """
    return decode_to_data(base_dictionary, data).decode("UTF-8")


def decode_to_data(base_dictionary: dict[int, str], data: bytes) -> bytes:
    """
    Purkaa syötebittimerkkijonon annetun sanakirjan
    perusteella ja palauttaa merkkijonon.
    """

    # käännetään sanakirja ympäri eli koodi -> tavu/kokonaisluku
    dictionary: dict[str, int] = {code: byte for byte, code in base_dictionary.items()}

    result_bytes = bytearray()

    # pythonissa ei taida olla mitään muuta hyvää
    # tapaa käsitellä syöte bitti kerrallaan kuin
    # merkkijonot, joten käytetään taas niitä.
    buffer = ""

    # bittejä kerätään kunnes sanakirjasta löytyy vastaava koodi.
    # tämä toimii koska Huffmanin koodauksessa koodien etuliitteitä ei
    # voi sekoittaa vaan koodi löydetään hakemalla bittejä järjestyksessä.

    big_number = int.from_bytes(data, byteorder="big")
    # muutetaan bytesistä saatu int muotoon
    # 0b110101, josta poistetaan 0b ja ensimmäinen bitti 1, joka
    # lisättiin ettei kokonaisluvuksi muunnos poistaisi alusta nollia.
    # näin voidaan käsitellä bitit yksi kerrallaan
    bit_string = bin(big_number)[3:]

    for bit in bit_string:
        buffer += bit
        if buffer in dictionary:
            result_bytes.append(dictionary[buffer])
            buffer = ""

    return result_bytes


def pack(dictionary: dict[int, str], data: bytes) -> bytes:
    """
    Funktio, joka pakkaa sanakirjan ja datan yhdeksi tavulistaksi.
    Tavulistassa on alussa 8 tavua (64 bittiä) pitkä kokonaisluku,
    joka määrittelee sanakirjan tietojen pituuden tavuissa.

    Tämän jälkeen paketissa on sanakirjan tiedot, joissa joka parille on
    ensin avain yhdessä tavussa, toisena koodin pituus, ja n tavua koodia.
    """
    # pakataan muotoon:
    # sanakirjan pituus 8 tavua, sanakirjan tiedot ensimmäisen 8 tavun perusteella, data...
    # sanakirjan tiedot ovat [merkki1, pituus1, koodi1, merkki2, pituus2, koodi2, ...].
    barray = bytearray()

    # jokainen sanakirjan pari
    for symbol, code in dictionary.items():
        # lisätään alkuun avain, eli kokonaisluku
        barray.append(symbol)

        # code on vielä str muotoa "00011010101"
        bit_length = len(code)
        # toinen tavu on 8 bittiä/1 tavu koodin bittipituutta
        barray.extend(len(code).to_bytes(1, "big"))

        # kolmantena on itse koodi kokonaislukuna
        # nollat häviävät alusta, mutta ne voidaan lisätä
        # bittipituuden perusteella takaisin
        code_int = int(code, 2)
        barray.extend(code_int.to_bytes((bit_length + 7) // 8, "big"))

    # 64 bittiä/8 tavua pituutta alkuun
    barray = bytearray(len(barray).to_bytes(8, "big")) + barray

    # lisätään pakettiin itse data loppuun
    barray.extend(data)

    return bytes(barray)


def unpack(bytelist: bytes) -> tuple[dict[int, str], bytes]:
    """
    Purkaa paketin, jonka pack() teki. Muuttaa siis tavulistan
    sanakirjaksi ja dataksi.
    """

    # # luetaan sanakirjan tietojen pituus ensimmäisestä 8 tavusta
    dict_length = int.from_bytes(bytelist[0:8], "big")

    # valitaan sanakirjan tavut slicellä
    dict_data = bytelist[8 : dict_length + 8]

    dictionary = {}
    i = 0

    # ensiksi luetaan avain, sitten sitä seuraava koodin pituus, ja sen jälkeen
    # itse koodi pituuden perusteella, joka muutetaan merkkijonoksi
    while i < len(dict_data):
        key = dict_data[i]
        int_bits = dict_data[i + 1]
        int_bytes = (int_bits + 7) // 8
        # jako ylös pyöristäen
        code_int = int.from_bytes(dict_data[i + 2 : i + 2 + int_bytes], "big")

        dictionary[key] = bin(code_int)[2:].zfill(int_bits)
        i += 2 + int_bytes

    return dictionary, bytelist[8 + dict_length :]


def pack_file(source_name: str, destination_name: str) -> None:
    """
    Avaa tiedoston annetun tiedoston, lukee, koodaa ja pakkaa sen.
    Pakatut tiedot tallennetaan toiseen annettuun tiedostoon.
    Koodaus tapahtuu funktiolla encode_data() ja
    pakkaus funktiolla pack().
    """

    with open(source_name, "rb") as f:
        data = f.read()

    dictionary, encoded = encode_data(data)
    packed = pack(dictionary, encoded)

    with open(destination_name, "wb") as f:
        f.write(packed)


def unpack_file(source_name: str, destination_name: str) -> None:
    """
    Avaa funktion pack_file() pakkaaman tiedoston, purkaa sen, ja kääntää sen.
    Lopuksi käännetty data tallennetaan toiseen annettuun tiedostoon.
    Purkamisen hoitaa unpack() ja kääntämisen decode_to_data().
    """

    with open(source_name, "rb") as f:
        data = f.read()

    dictionary, encoded = unpack(data)

    decoded = decode_to_data(dictionary, encoded)

    with open(destination_name, "wb") as f:
        f.write(decoded)
