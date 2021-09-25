from pakkaus.huffman import HuffmanNode
import unittest
from pakkaus import huffman


class TestHuffmanNode(unittest.TestCase):
    def test_printing(self):
        tree = HuffmanNode(
            frequency=2,
            symbol=99,
            left=HuffmanNode(frequency=1, symbol=50, left=None, right=None),
            right=HuffmanNode(frequency=1, symbol=49, left=None, right=None),
        )

        expected = "0b1100011: 2\n\t0b110001: 1\n\t0b110010: 1\n"

        self.assertEqual(str(tree), expected)


class TestHuffmanFunctions(unittest.TestCase):
    def test_encode(self):
        dictionary, string = huffman.encode_string("IUFGIUFGUDFYUY")
        self.assertEqual(dictionary, {70: "00", 68: "010", 71: "011", 85: "10", 73: "110", 89: "111"})

        self.assertEqual(string, b"\x0e\x87\xa1\xc8\xf7")

        big_dictionary, big_string = huffman.encode_string(
            "IUFGIUFGUDFYUY453845845675464587bndguf348yyhgft84i7hy587t48558hyt8g475IUFGIUFGUDFYUY453845845675464587bndguf348yyhgft84i7hy587t48558hyt8g475"
        )
        self.assertEqual(
            big_dictionary,
            {
                116: "0000",
                85: "0001",
                51: "00100",
                54: "00101",
                121: "0011",
                71: "01000",
                73: "01001",
                89: "01010",
                102: "01011",
                52: "011",
                53: "100",
                56: "101",
                68: "110000",
                98: "110001",
                100: "110010",
                105: "110011",
                55: "1101",
                110: "111000",
                117: "111001",
                70: "11101",
                103: "11110",
                104: "11111",
            },
        )

        self.assertEqual(
            big_string,
            b"\x14\x8fP\x91\xea\x07\x0e\xa8T\xe1+\x95\xc2\xecer\xee<e\xeeVGL\xff\xe5\x85y\xef\xce]\x07d\xbf0\xbe{\x12=BG\xa8\x1c:\xa1S\x84\xaeW\x0b\xb1\x95\xcb\xb8\xf1\x97\xb9Y\x1d3\xff\x96\x15\xe7\xbf9t\x1d\x92\xfc\xc2\xf9\xec",
        )

    def test_decode(self):
        dictionary = {
            73: "000",
            74: "001",
            77: "010",
            78: "011",
            82: "100",
            75: "101",
            79: "110",
            33: "1110",
            69: "1111",
        }
        string = b"\n\xf9h9\xee"

        decoded = huffman.decode_to_string(dictionary, string)
        self.assertEqual(decoded, "MERKKIJONO!")

        big_dictionary = {
            164: "00000",
            77: "00001",
            33: "0001",
            69: "0010",
            107: "0011",
            78: "01000",
            83: "01001",
            97: "01010",
            106: "01011",
            44: "011000",
            63: "011001",
            111: "01101",
            114: "01110",
            64: "011110",
            65: "011111",
            76: "100000",
            80: "100001",
            195: "10001",
            95: "100100",
            109: "100101",
            115: "100110",
            132: "100111",
            73: "1010",
            75: "1011",
            79: "1100",
            74: "11010",
            82: "11011",
            101: "11100",
            105: "11101",
            32: "1111",
        }

        big_string = b"4\x9c\x90%\xbb\xba\xd6#\x18\xf8_\x83X\x8f-\xd5\xe5&\x9e\xf0\x96\xee\xcbQ\x9f\xd6\xaf\xe3\xbb\xe6\xd3of\xea\xbe^8\xcf\x8b\x88\x04DY"

        big_decoded = huffman.decode_to_string(big_dictionary, big_string)
        # :D
        self.assertEqual(
            big_decoded, "ISO_MERKKIJONO, PALJON ERIKOISI@ MERKKEJÄ ja eri kokoisia merkkejä!!!!?"
        )


if __name__ == "__main__":
    unittest.main()