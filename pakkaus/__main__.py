"Sallii ohjelman käytön komennolla `python -m pakkaus`."
import sys
import os

from . import huffman


def simple_ui():
    print("Tämä ohjelma pakkaa ja purkaa tietoa")
    input_string = input("Syötä merkkijono: ")

    packed = huffman.pack_data(input_string)

    print()
    print(
        f"Pakattu merkkijono on: {packed}, eli bitteinä: {bin(int.from_bytes(packed, byteorder='big'))}"
    )
    print(f"Pakkaussuhde on: {sys.getsizeof(packed)/sys.getsizeof(input_string) * 100}%")
    decoded_string = huffman.unpack_data(packed).decode("UTF-8")
    print(f"Uudelleen purettu merkkijono on: {decoded_string}")


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
        source_file = sys.argv[2]
        destination_file = sys.argv[3]
        huffman.unpack_file(source_file, destination_file)
