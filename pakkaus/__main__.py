from . import huffman

"Sallii ohjelman käytön komennolla `python -m pakkaus`."

if __name__ == "__main__":
    print("Tämä ohjelma pakkaa ja purkaa tietoa")
    input_string = input("Syötä merkkijono: ")

    dictionary, encoded_string = huffman.encode(input_string)

    print()
    print(f"Syötteestä saatu sanakirja on: {dictionary}")
    print(f"Pakattu merkkijono on: {encoded_string}")

    print("Puretaan...")

    decoded_string = huffman.decode(dictionary, encoded_string)
    print(f"Uudelleen purettu merkkijono on {decoded_string}")