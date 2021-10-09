"Tämä moduuli toteuttaa Huffmanin koodauksen Tiralabraa varten."
import heapq
from collections import Counter
from dataclasses import dataclass
from textwrap import indent
from typing import Dict, List, Optional, Tuple, Union


@dataclass(order=False)
class _HuffmanNode:
    """
    Solmuluokka, joka toteuttaa Huffmanin puun.
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
    # Käytössä Counter, koska sillä laskeminen on huomattavasti
    # nopeampaa kuin itse esim defaultdict() rakenteella
    # luultavasti, koska Counter() on C-koodia
    frequencies: Dict[int, int] = Counter(data)
    # tässä kohtaa tulee huomattua, että bytes on enemmänkin
    # lista 8-bittisiä kokonaislukuja, joten tyyppi
    # on dict[int, int]
    # minimikeko

    heap: List[_HuffmanNode] = []

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


def _generate_dictionary(tree: _HuffmanNode) -> Dict[int, str]:
    """
    Funktio hyväksyy syötteenä Huffmanin puun ja muuttaa sen
    sanakirjaksi.
    """

    # koodit ovat siis merkkijonoja syystä, että
    # pythonissa ei vaikuta olevan mitään parempaa
    # tapaa lisätä bittejä toisiinsa
    codes: Dict[int, str] = {}

    # jos puussa on vain yksi solmu, merkkijonon pituus on yksi.
    # rekursio ei tomi tällöin, joten palautetaa heti, "sanakirja"
    if not tree.left and not tree.right:
        return {tree.symbol: "1"}

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


def _apply_dictionary_to_data(data: bytes, codes: Dict[int, str]) -> str:
    "Koodaa syötetavut sanakirjan avulla ja palauttaa koodatun bittijonon."

    return "".join([codes[byte] for byte in data])


def _encode_to_dictionary(data: bytes) -> Tuple[Dict[int, str], bytes]:

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


def _decode_with_dictionary(base_dictionary: Dict[int, str], data: bytes) -> bytes:
    """
    Purkaa tavut annetun sanakirjan
    perusteella ja palauttaa dekoodatun datan.
    """

    # käännetään sanakirja ympäri eli koodi -> tavu/kokonaisluku
    dictionary: Dict[str, int] = {code: byte for byte, code in base_dictionary.items()}

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


def _pack(dictionary: Dict[int, str], data: bytes) -> bytes:
    """
    Funktio, joka pakkaa sanakirjan ja datan yhdeksi tavulistaksi.
    Tavulistassa on alussa 8 tavua (64 bittiä) pitkä kokonaisluku,
    joka määrittelee sanakirjan tietojen pituuden tavuissa.

    Tämän jälkeen paketissa on sanakirjan tiedot, joissa joka parille on
    ensin avain yhdessä tavussa, toisena koodin pituus, ja n tavua koodia.
    """
    # pakataan muotoon:
    # [sanakirjan pituus 8 tavua, sanakirjan tiedot ensimmäisen 8 tavun perusteella, data...]
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


def _unpack(bytelist: bytes) -> Tuple[Dict[int, str], bytes]:
    """
    Purkaa paketin, jonka _pack() teki. Muuttaa siis tavut
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


def pack_data(data: Union[bytes, str]) -> bytes:
    """
    Funktio, joka koodaa ja pakkaa joko tavuja tai merkkijonon.
    Tekee siis syötemerkkijonolle Huffmanin puun,
    puusta sanakirjan, koodaa syötteen sen avulla ja pakkaa
    sanakirjan ja koodatun datan.
    Palauttaa tavuja, joissa on pakattuna sanakirja ja koodattu data.
    """

    if len(data) == 0:
        raise ValueError("Tyhjä syöte")

    if isinstance(data, str):
        data = data.encode("UTF-8")

    dictionary, compressed_bytes = _encode_to_dictionary(data)

    packed = _pack(dictionary, compressed_bytes)

    return packed


def unpack_data(data: bytes) -> bytes:
    """
    Purkaa annetun syötteen funktioilla _unpack() ja
    _decode_with_dictionary().
    """

    if len(data) == 0:
        raise ValueError("Tyhjä syöte")

    dictionary, compressed_bytes = _unpack(data)

    uncompressed = _decode_with_dictionary(dictionary, compressed_bytes)

    return uncompressed


def pack_file(source_name: str, destination_name: str) -> None:
    """
    Avaa tiedoston annetun tiedoston, lukee, koodaa ja pakkaa sen.
    Pakatut tiedot tallennetaan toiseen annettuun tiedostoon.
    Käyttää funktiota pack_data() pakkaamiseen.
    """

    try:
        with open(source_name, "rb") as f:
            data = f.read()
    except OSError as e:
        print(f"Failed to read file {e=}")
        raise

    packed = pack_data(data)

    try:
        with open(destination_name, "wb") as f:
            f.write(packed)
    except OSError as e:
        print(f"Failed to write file {e=}")
        raise


def unpack_file(source_name: str, destination_name: str) -> None:
    """
    Avaa funktion pack_file() pakkaaman tiedoston, purkaa sen, ja kääntää sen.
    Lopuksi käännetty data tallennetaan toiseen annettuun tiedostoon.
    Käyttää funktiota unpack_data() purkamiseen.
    """

    try:
        with open(source_name, "rb") as f:
            data = f.read()
    except OSError as e:
        print(f"Failed to read file {e=}")
        raise

    unpacked = unpack_data(data)

    try:
        with open(destination_name, "wb") as f:
            f.write(unpacked)
    except OSError as e:
        print(f"Failed to write file {e=}")
        raise
