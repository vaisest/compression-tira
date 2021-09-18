import heapq
from collections import Counter
from dataclasses import dataclass
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
    symbol: str
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    def __lt__(self, other) -> bool:
        return (self.frequency, self.symbol) < (other.frequency, other.symbol)

    def __str__(self, level=0) -> None:
        # koska SyntaxError: f-string expression part cannot include a backslash:
        tab = "\t"

        if not self.left or not self.right:
            return f"{tab * level} {self.symbol}: {self.frequency}"

        return f"""
        {tab * level} {self.symbol}: {self.frequency}
        {self.right.__str__(level=level + 1)}
        {self.left.__str__(level=level + 1)}
        """


def generate_tree(string: str) -> HuffmanNode:
    """
    Hyväksyy merkkijonon ja palauttaa siitä tehdyn
    Huffmanin puun.
    """

    # Counter laskee jokaisen merkin frekvenssin
    frequencies = Counter(string)

    # minimikeko
    heap = []

    # jokaiselle merkille tehdään lehtisolmu, jossa solmun todennäköisyys on
    # merkin määrä tekstissä
    for char, freq in zip(frequencies, frequencies.values()):
        heapq.heappush(heap, HuffmanNode(freq, char))

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

        first.parent = internal_node
        second.parent = internal_node

    # jäljelle jäävä solmu on puun juuri
    return heap[0]


def generate_dictionary(tree: HuffmanNode) -> dict[str, str]:
    """
    Funktio hyväksyy syötteenä Huffmanin puun ja muuttaa sen
    sanakirjaksi.
    """

    codes = {}

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


def apply_dictionary_to_string(input_str: str, codes: dict[str, str]) -> str:
    "Koodaa syötemerkkijonon sanakirjan avulla ja palauttaa bittimerkkijonon."

    return "".join([codes[char] for char in input_str])


def encode(string: str) -> tuple[dict[str, str], str]:
    """
    Apufunktio joka tekee syötemerkkijonolle Huffmanin puun,
    puusta sanakirjan ja koodaa merkkijonon sen avulla.
    Palauttaa dict-tyypin, joka sisältää sanakirjan, ja bittimerkkijonon.
    """

    tree = generate_tree(string)

    dictionary = generate_dictionary(tree)

    return dictionary, apply_dictionary_to_string(string, dictionary)


def decode(dictionary: dict[str, str], string: str) -> str:
    """
    Purkaa syötebittimerkkijonon annetun sanakirjan
    perusteella ja palauttaa merkkijonon.
    """

    # käännetään sanakirja ympäri eli koodi -> merkki
    dictionary = {v: k for k, v in dictionary.items()}

    result_string = ""

    buffer = ""

    # bittejä kerätään kunnes sanakirjasta löytyy vastaava koodi.
    # tämä toimii koska Huffmanin koodauksessa koodien etuliitteitä ei
    # voi sekoittaa vaan koodi löydetään hakemalla bittejä järjestyksessä.
    for bit in string:
        buffer += bit
        if buffer in dictionary:
            result_string += dictionary[buffer]
            buffer = ""

    return result_string
