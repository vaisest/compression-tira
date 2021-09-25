import heapq
from collections import Counter
from dataclasses import dataclass
from textwrap import indent
from typing import Optional


@dataclass(order=False)
class HuffmanNode:
    """
    Solmuluokka, joka toteuttaa Huffmanin puu.
    Solmussa arvo (käytännössä merkin frekvenssi) ja
    itse merkki ovat pakollisia. Vasen ja oikea alasolmu
    ovat vapaaehtoisia.
    """

    frequency: int
    symbol: int
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

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


def generate_tree(data: bytes) -> HuffmanNode:
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
    heap: list[HuffmanNode] = []

    # jokaiselle merkille tehdään lehtisolmu, jossa solmun
    # todennäköisyys on kyseisen tavun määrä
    for byte, freq in zip(frequencies, frequencies.values()):
        heapq.heappush(heap, HuffmanNode(freq, byte))

    while len(heap) > 1:
        # keosta otetaan kaksi pienintä
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)

        # näistä tehdään uusi solmu, jonka lapset ovat nämä kaksi solmua
        # uuden solmun arvo on sen lapsien arvon summa
        internal_node = HuffmanNode(
            first.frequency + second.frequency,
            first.symbol + second.symbol,
            first,
            second,
        )

        # uusi solmu lisätään takaisin kekoon
        heapq.heappush(heap, internal_node)

    # jäljelle jäävä solmu on puun juuri
    return heap[0]


def generate_dictionary(tree: HuffmanNode) -> dict[int, str]:
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
    def recurse(node: HuffmanNode, codes: dict, bits: str) -> None:
        if node.left and node.right:
            recurse(node.left, codes, bits + "0")
            recurse(node.right, codes, bits + "1")
        else:
            # lehtisolmu
            codes[node.symbol] = bits

    recurse(tree, codes, "")

    return codes


def apply_dictionary_to_data(data: bytes, codes: dict[int, str]) -> str:
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

    tree = generate_tree(data)

    dictionary = generate_dictionary(tree)

    # bittimerkkijonoon lisätään bitti yksi eteen ettei muunnos
    # kokonaisluvuksi poista alusta kaikkia nollia
    encoded_string = "1" + apply_dictionary_to_data(data, dictionary)

    # bittimerkkijono muutetaan kokonaisluvuksi
    encoded_int = int(encoded_string, 2)

    # kokonaisluku muutetaan tavuiksi
    encoded_data = encoded_int.to_bytes((encoded_int.bit_length() + 7) // 8, "big")

    return dictionary, encoded_data


def decode_to_string(base_dictionary: dict[int, str], data: bytes) -> str:
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
