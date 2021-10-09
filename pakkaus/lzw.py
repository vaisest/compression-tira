"Tämä moduuli toteuttaa LZW-pakkausalgoritmin Tiralabraa varten."


# @dataclass
# class _TrieNode:
#     "Dataclass Trie-luokan solmuja varten."

#     children: dict[int, "_TrieNode"] = field(default_factory=dict)
#     value: Optional[bytes] = None


# class _TrieNode:
#     "class Trie-luokan solmuja varten."
#     __slots__ = "children", "value"

#     def __init__(self) -> None:
#         self.children: dict[int, _TrieNode] = dict()
#         self.value: Optional[bytes] = None


# class _Trie:
#     "Toteuttaa Trie-tietorakenteen LZW-algoritmia varten tupleja käyttäen."

#     def __init__(self) -> None:
#         # mypy ei taida tukea rekursiivisia tyyppejä
#         self.data: Any = [dict(), None]
#         self.size = 0

#     def __str__(self):
#         return str(self.data)

#     def get(self, key: bytes) -> bytes:
#         pair = self.data
#         for integer in key:
#             if integer in pair[0]:
#                 pair = pair[0][integer]
#             else:
#                 raise KeyError("Trie get() did not find key.")
#         # # mypy valittaa optionalista:
#         # if map.value is None:
#         #     raise ValueError()
#         return pair[1]

#     def __getitem__(self, item: bytes) -> bytes:
#         return self.get(item)

#     def __setitem__(self, key: bytes, value: bytes) -> None:
#         return self.insert(key, value)

#     def __contains__(self, item: bytes) -> bool:
#         pair = self.data
#         for integer in item:
#             if integer in pair[0]:
#                 pair = pair[0][integer]
#             else:
#                 return False
#         return True

#     def insert(self, key: bytes, value: bytes) -> None:
#         pair = self.data
#         for integer in key:
#             if integer not in pair[0]:
#                 pair[0][integer] = [dict(), None]
#             pair = pair[0][integer]
#         pair[1] = value
#         self.size += 1

#     def __len__(self):
#         return self.size


def compress(data: bytes) -> bytes:
    """
    Pakkaa annetun bytes-rakenteen LZW-algoritmilla.
    """

    # koska bytes konkatenaatio on hidasta,
    # käytetään bytearrayita
    data = bytearray(data)

    DICTIONARY_MAX_SIZE = 2 ** 16
    # Testissä oli Trie tietorakenne hitauden selvittämiseksi
    # Se oli jotenkin vielä hitaampi kuin dict.
    # Luultavasti koska Pythonin oliot ovat erittäin hitaita ja
    # dict on osittain optimoitua C-koodia.
    # Myös Trie ilman luokkia on noin 2.5 kertaa hitaampi
    # kuin dict
    # dictionary = _Trie()
    dictionary = dict()

    # sanakirjan laitetaan kaikki yhden tavun koodit
    for i in range(0, 256):
        dictionary[i.to_bytes(1, "big")] = i.to_bytes(2, "big")

    results: list[bytes] = list()

    word = bytearray()

    pointer = 0
    dict_size_counter = 256

    # itse algoritmi
    while len(data) > pointer:
        if dict_size_counter >= DICTIONARY_MAX_SIZE:
            # if len(dictionary) >= DICTIONARY_MAX_SIZE:
            del dictionary
            dict_size_counter = 256
            # dictionary = _Trie()
            dictionary = dict()
            for i in range(0, 256):
                dictionary[i.to_bytes(1, "big")] = i.to_bytes(2, "big")

        byte = data[pointer : pointer + 1]
        if bytes(word + byte) in dictionary:
            word.extend(byte)
        else:
            # fnd = dictionary.get(string)
            # results.append(fnd)
            results.append(dictionary[bytes(word)])

            # dictionary.insert(string + char, len(dictionary).to_bytes(2, "big"))
            dictionary[bytes(word + byte)] = len(dictionary).to_bytes(2, "big")
            dict_size_counter += 1
            word = byte
        pointer += 1

    # results.append(dictionary.get(string))
    results.append(dictionary[bytes(word)])

    return b"".join(results)


def uncompress(data: bytes) -> bytes:
    """
    Purkaa annetun LZW-pakatun bytes rakenteen.
    Toisin kuin compress(), tämän funktion
    nopeus pitäisi olla hyväksyttävää.
    """

    # koska bytesin konkatenaatio on erittäin hidasta,
    data = bytearray(data)

    DICTIONARY_MAX_SIZE = 2 ** 16

    # sanakirjana käytetään pelkkää listaa
    dictionary: list[bytearray] = list()
    for i in range(0, 256):
        dictionary.append(bytearray(i.to_bytes(1, "big")))

    # lista tallennetaan muuttujaan, josta se voidaan
    # kopioida takaisin, kun se sanakirja pitää tyhjentää
    # original_dictionary = copy.deepcopy(dictionary)

    output: list[bytearray] = list()

    last_code = (data[0] << 8) | data[1]
    code = last_code
    output.append(dictionary[last_code])

    for i in range(2, len(data) - 1, 2):

        code = (data[i] << 8) | data[i + 1]
        if code < len(dictionary):
            output.append(dictionary[code])

            dictionary.append(dictionary[last_code] + dictionary[code][0:1])
        else:
            dictionary.append(dictionary[last_code] + dictionary[last_code][0:1])
            output.append(dictionary[last_code] + dictionary[last_code][0:1])

        last_code = code

        if len(dictionary) == DICTIONARY_MAX_SIZE:
            dictionary.clear()
            for i in range(0, 256):
                dictionary.append(bytearray(i.to_bytes(1, "big")))
                # dictionary.append(i.to_bytes(1, "big"))

    return b"".join(output)


def compress_file(source_name: str, destination_name: str) -> None:
    """
    Avaa annetun tiedoston, lukee, pakkaa ja tallentaa sen.
    Pakatut tiedot tallennetaan toiseen annettuun tiedostoon.
    Pakkauksen tekee funktio compress().
    """

    with open(source_name, "rb") as f:
        data = f.read()

    compressed = compress(data)

    with open(destination_name, "wb") as f:
        f.write(compressed)


def uncompress_file(source_name: str, destination_name: str) -> None:
    """
    Avaa funktion pack_file() pakkaaman tiedoston, purkaa sen, ja kääntää sen.
    Lopuksi käännetty data tallennetaan toiseen annettuun tiedostoon.
    Purkamisen hoitaa uncompress().
    """

    with open(source_name, "rb") as f:
        data = f.read()

    uncompressed = uncompress(data)

    with open(destination_name, "wb") as f:
        f.write(uncompressed)
