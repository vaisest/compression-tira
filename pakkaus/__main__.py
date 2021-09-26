"Sallii ohjelman käytön komennolla `python -m pakkaus`."
import sys
import os

from . import huffman


def simple_ui():
    print("Tämä ohjelma pakkaa ja purkaa tietoa")
    input_string = input("Syötä merkkijono: ")

    dictionary, encoded_string = huffman.encode_string(input_string)

    print()
    print(f"Syötteestä saatu sanakirja on: {dictionary}")
    print(
        f"Pakattu merkkijono on: {encoded_string}, eli bitteinä: {bin(int.from_bytes(encoded_string, byteorder='big'))}"
    )

    decoded_string = huffman.decode_to_string(dictionary, encoded_string)
    print(f"Uudelleen purettu merkkijono on: {decoded_string}")

    print(a := huffman.pack(dictionary, encoded_string))
    print(huffman.unpack(a))

    print("Pakataan ja puretaan tiedosto")
    source_file = input("Syötä lähdetiedoston nimi:")
    destination_file = input("Syötä kohdetiedoston nimi:")
    print("Pakataan...")

    huffman.pack_file(source_file, destination_file)

    source_size = os.path.getsize(source_file)
    destination_size = os.path.getsize(destination_file)
    print(
        f"Alkuperäisen koko: {source_size}, pakatun koko: {destination_size}, pakkaussuhde: {(destination_size/source_size)*100}%."
    )

    decode_file = input("Syötä purkamisen kohdetiedoston nimi:")
    print("Puretaan...")

    huffman.unpack_file(destination_file, decode_file)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        simple_ui()
    elif sys.argv[1] in ["c", "compress"]:
        source_file = sys.argv[2]
        destination_file = sys.argv[3]
        huffman.pack_file(source_file, destination_file)
        source_size = os.path.getsize(source_file)
        destination_size = os.path.getsize(destination_file)
        print(
            f"Alkuperäisen koko: {source_size}, pakatun koko: {destination_size}, pakkaussuhde: {(destination_size/source_size)*100}%."
        )
    elif sys.argv[1] in ["u", "uncompress"]:
        exit()
