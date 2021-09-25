from pakkaus.huffman import HuffmanNode
import unittest
from pakkaus import huffman


class TestHuffmanNode(unittest.TestCase):
    def test_printing(self):
        tree = HuffmanNode(
            frequency=2,
            symbol="12",
            left=HuffmanNode(frequency=1, symbol="1", left=None, right=None),
            right=HuffmanNode(frequency=1, symbol="2", left=None, right=None),
        )

        expected = "12: 2\n\t2: 1\n\t1: 1\n"

        self.assertEqual(str(tree), expected)


class TestHuffmanFunctions(unittest.TestCase):
    def test_encode(self):
        dictionary, string = huffman.encode("IUFGIUFGUDFYUY")
        self.assertEqual(
            dictionary, {"D": "000", "G": "001", "F": "01", "I": "100", "Y": "101", "U": "11"}
        )

        self.assertEqual(string, "10011010011001101001110000110111101")

        big_dictionary, big_string = huffman.encode(
            "IUFGIUFGUDFYUY453845845675464587bndguf348yyhgft84i7hy587t48558hyt8g475IUFGIUFGUDFYUY453845845675464587bndguf348yyhgft84i7hy587t48558hyt8g475"
        )
        self.assertEqual(
            big_dictionary,
            {
                "t": "0000",
                "3": "00010",
                "6": "00011",
                "D": "001000",
                "b": "001001",
                "G": "00101",
                "I": "00110",
                "Y": "00111",
                "U": "0100",
                "d": "010100",
                "i": "010101",
                "f": "01011",
                "4": "011",
                "5": "100",
                "8": "101",
                "y": "1100",
                "7": "1101",
                "n": "111000",
                "u": "111001",
                "F": "11101",
                "g": "11110",
                "h": "11111",
            },
        )

        self.assertEqual(
            big_string,
            "00110010011101001010011001001110100101010000100011101001110100001110111000001010101110010101110000011110110001100011011100101110100100111100001010011110111001010110001001110111001100111111111001011000010101101010111011111111001001011101000001110110010010111111110000001011111001111011000011001001110100101001100100111010010101000010001110100111010000111011100000101010111001010111000001111011000110001101110010111010010011110000101001111011100101011000100111011100110011111111100101100001010110101011101111111100100101110100000111011001001011111111000000101111100111101100",
        )

    def test_decode(self):
        dictionary = {
            "M": "000",
            "N": "001",
            "O": "01",
            "R": "100",
            "!": "1010",
            "E": "1011",
            "I": "1100",
            "J": "1101",
            "K": "111",
        }
        string = "00010111001111111100110101001011010"

        decoded = huffman.decode(dictionary, string)
        self.assertEqual(decoded, "MERKKIJONO!")

        big_dictionary = {
            " ": "000",
            "!": "0010",
            "A": "00110",
            "L": "001110",
            "P": "001111",
            "E": "0100",
            "M": "01010",
            "N": "01011",
            "S": "01100",
            "_": "011010",
            "m": "011011",
            "a": "01110",
            "j": "01111",
            "k": "1000",
            "o": "10010",
            "r": "10011",
            "I": "1010",
            "K": "1011",
            "O": "1100",
            "s": "110100",
            "Ä": "110101",
            "J": "11011",
            "R": "11100",
            "e": "11101",
            "i": "11110",
            "ä": "111110",
            ",": "1111110",
            "?": "1111111",
        }

        big_string = "1010011001100011010010100100111001011101110101101111000101111001111110000001111001100011101101111000101100001001110010101011110010100110010100011000001010010011100101110110100110111101010000111101110000111011001111110000100010010100010010111101101001111001110000011011111011001110001000111010111111111000100010001000101111111"

        big_decoded = huffman.decode(big_dictionary, big_string)
        # :D
        self.assertEqual(
            big_decoded, "ISO_MERKKIJONO, PALJON ERIKOISIA MERKKEJÄ ja eri kokoisia merkkejä!!!!?"
        )


if __name__ == "__main__":
    unittest.main()