import os
import unittest

from pakkaus import huffman
from pakkaus.huffman import _HuffmanNode


class TestHuffmanNode(unittest.TestCase):
    def test_printing(self):
        tree = _HuffmanNode(
            frequency=2,
            symbol=99,
            left=_HuffmanNode(frequency=1, symbol=50, left=None, right=None),
            right=_HuffmanNode(frequency=1, symbol=49, left=None, right=None),
        )

        expected = "0b1100011: 2\n\t0b110001: 1\n\t0b110010: 1\n"

        self.assertEqual(str(tree), expected)


class TestPublicFunctions(unittest.TestCase):
    def test_pack_data(self):
        little_data = huffman.pack_data(b"B")
        self.assertEqual(little_data, b"\x00\x00\x00\x00\x00\x00\x00\x03B\x01\x01\x03")

        data = huffman.pack_data("IUFGIUFGUDFYUY")
        self.assertEqual(
            data,
            b"\x00\x00\x00\x00\x00\x00\x00\x12F\x02\x00D\x03\x02G\x03\x03U\x02\x02I\x03\x06Y\x03\x07\x0e\x87\xa1\xc8\xf7",
        )

        big_data = huffman.pack_data(
            "IUFGIUFGUDFYUY453845845675464587bndguf348yyhgft84i7hy587t48558hyt8g475IUFGIUFGUDFYUY453845845675464587bndguf348yyhgft84i7hy587t48558hyt8g475"
            * 5
        )
        self.assertEqual(
            big_data,
            b"\x00\x00\x00\x00\x00\x00\x00Bt\x04\x00U\x04\x013\x05\x046\x05\x05y\x04\x03G\x05\x08I\x05\tY\x05\nf\x05\x0b4\x03\x035\x03\x048\x03\x05D\x060b\x061d\x062i\x0637\x04\rn\x068u\x069F\x05\x1dg\x05\x1eh\x05\x1f\x14\x8fP\x91\xea\x07\x0e\xa8T\xe1+\x95\xc2\xecer\xee<e\xeeVGL\xff\xe5\x85y\xef\xce]\x07d\xbf0\xbe{\x12=BG\xa8\x1c:\xa1S\x84\xaeW\x0b\xb1\x95\xcb\xb8\xf1\x97\xb9Y\x1d3\xff\x96\x15\xe7\xbf9t\x1d\x92\xfc\xc2\xf9\xecH\xf5\t\x1e\xa0p\xea\x85N\x12\xb9\\.\xc6W.\xe3\xc6^\xe5dt\xcf\xfeXW\x9e\xfc\xe5\xd0vK\xf3\x0b\xe7\xb1#\xd4$z\x81\xc3\xaa\x158J\xe5p\xbb\x19\\\xbb\x8f\x19{\x95\x91\xd3?\xf9a^{\xf3\x97A\xd9/\xcc/\x9e\xc4\x8fP\x91\xea\x07\x0e\xa8T\xe1+\x95\xc2\xecer\xee<e\xeeVGL\xff\xe5\x85y\xef\xce]\x07d\xbf0\xbe{\x12=BG\xa8\x1c:\xa1S\x84\xaeW\x0b\xb1\x95\xcb\xb8\xf1\x97\xb9Y\x1d3\xff\x96\x15\xe7\xbf9t\x1d\x92\xfc\xc2\xf9\xecH\xf5\t\x1e\xa0p\xea\x85N\x12\xb9\\.\xc6W.\xe3\xc6^\xe5dt\xcf\xfeXW\x9e\xfc\xe5\xd0vK\xf3\x0b\xe7\xb1#\xd4$z\x81\xc3\xaa\x158J\xe5p\xbb\x19\\\xbb\x8f\x19{\x95\x91\xd3?\xf9a^{\xf3\x97A\xd9/\xcc/\x9e\xc4\x8fP\x91\xea\x07\x0e\xa8T\xe1+\x95\xc2\xecer\xee<e\xeeVGL\xff\xe5\x85y\xef\xce]\x07d\xbf0\xbe{\x12=BG\xa8\x1c:\xa1S\x84\xaeW\x0b\xb1\x95\xcb\xb8\xf1\x97\xb9Y\x1d3\xff\x96\x15\xe7\xbf9t\x1d\x92\xfc\xc2\xf9\xec",
        )

        empty_data = bytes()
        self.assertRaises(ValueError, huffman.pack_data, empty_data)

    def test_unpack_data(self):
        little_data = b"\x00\x00\x00\x00\x00\x00\x00\x03B\x01\x01\x03"
        little_decoded_str = huffman.unpack_data(little_data)
        self.assertEqual(little_decoded_str, b"B")

        data = b"\x00\x00\x00\x00\x00\x00\x00\x1bI\x03\x00J\x03\x01M\x03\x02N\x03\x03R\x03\x04K\x03\x05O\x03\x06!\x04\x0eE\x04\x0f\n\xf9h9\xee"

        decoded_str = huffman.unpack_data(data).decode("UTF-8")
        self.assertEqual(decoded_str, "MERKKIJONO!")

        big_data = b"\x00\x00\x00\x00\x00\x00\x00Z\xa4\x05\x00M\x05\x01!\x04\x01E\x04\x02k\x04\x03N\x05\x08S\x05\ta\x05\nj\x05\x0b,\x06\x18?\x06\x19o\x05\rr\x05\x0e@\x06\x1eA\x06\x1fL\x06 P\x06!\xc3\x05\x11_\x06$m\x06%s\x06&\x84\x06'I\x04\nK\x04\x0bO\x04\x0cJ\x05\x1aR\x05\x1be\x05\x1ci\x05\x1d \x04\x0f\x03I\xc9\x02[\xbb\xadb1\x8f\x85\xf85\x88\xf2\xdd^Ri\xef\tn\xec\xb5\x19\xfdj\xfe;\xbem6\xf6n\xab\xe5\xe3\x8c\xf8\xb8\x80DE\x9aNH\x12\xdd\xddk\x11\x8c|/\xc1\xacG\x96\xea\xf2\x93OxKwe\xa8\xcf\xebW\xf1\xdd\xf3i\xb7\xb3u_/\x1cg\xc5\xc4\x02\",\xd2r@\x96\xee\xebX\x8cc\xe1~\rb<\xb7W\x94\x9a{\xc2[\xbb-F\x7fZ\xbf\x8e\xef\x9bM\xbd\x9b\xaa\xf9x\xe3>. \x11\x11f\x93\x92\x04\xb7wZ\xc4c\x1f\x0b\xf0k\x11\xe5\xba\xbc\xa4\xd3\xde\x12\xdd\xd9j3\xfa\xd5\xfcw|\xdam\xec\xddW\xcb\xc7\x19\xf1q\x00\x88\x8b4\x9c\x90%\xbb\xba\xd6#\x18\xf8_\x83X\x8f-\xd5\xe5&\x9e\xf0\x96\xee\xcbQ\x9f\xd6\xaf\xe3\xbb\xe6\xd3of\xea\xbe^8\xcf\x8b\x88\x04DY"

        big_decoded_str = huffman.unpack_data(big_data).decode("UTF-8")
        # :D
        self.assertEqual(
            big_decoded_str,
            "ISO_MERKKIJONO, PALJON ERIKOISI@ MERKKEJÄ ja eri kokoisia merkkejä!!!!?" * 5,
        )

        empty_data = bytes()
        self.assertRaises(ValueError, huffman.unpack_data, empty_data)

    def test_packing_files(self):
        file_contents = (
            f"""
            This is a test file
            for the
            tir@l@Br@! :))
            """
            * 99
        )

        source_file = "AUTOMATED.TEST.FILE.txt"
        destination_file = "AUTOMATED.TEST.FILE.BIN.HUFFMAN"
        unpacked_file = "AUTOMATED.TEST.FILE.unpacked.txt"

        with open(source_file, "w") as f:
            f.write(file_contents)

        huffman.pack_file(source_file, destination_file)

        huffman.unpack_file(destination_file, unpacked_file)

        with open(unpacked_file, "r") as f:
            unpacked = f.read()

        self.assertEqual(file_contents, unpacked)

        hopefully_inexistent_file = "AUTOMATED.INEXISTENT.FILE.TXT.LONG.EXTENSION"

        self.assertRaises(OSError, huffman.pack_file, hopefully_inexistent_file, unpacked_file)

        self.assertRaises(OSError, huffman.pack_file, source_file, "")

        self.assertRaises(OSError, huffman.unpack_file, hopefully_inexistent_file, unpacked_file)

        self.assertRaises(OSError, huffman.unpack_file, destination_file, "")

        os.remove(source_file)
        os.remove(destination_file)
        os.remove(unpacked_file)


class TestInternalFunctions(unittest.TestCase):
    def test_pack(self):
        dictionary = {
            104: "0000",
            105: "0001",
            106: "0010",
            117: "0011",
            50: "01",
            100: "100",
            102: "101",
            103: "110",
            51: "1110",
            49: "11110",
            53: "11111",
        }
        data = b"\xf9\xe7\x95\xf9K\xa5\x1caf"

        self.assertEqual(
            huffman._pack(dictionary, data),
            b"\x00\x00\x00\x00\x00\x00\x00!h\x04\x00i\x04\x01j\x04\x02u\x04\x032\x02\x01d\x03\x04f\x03\x05g\x03\x063\x04\x0e1\x05\x1e5\x05\x1f\xf9\xe7\x95\xf9K\xa5\x1caf",
        )

    def test_unpack(self):
        packed = b"\x00\x00\x00\x00\x00\x00\x00'f\x02\x004\x03\x02j\x03\x03s\x04\x083\x04\t9\x04\ng\x04\x0bh\x04\x0c5\x05\x1a8\x05\x1bv\x04\x0ec\x05\x1en\x05\x1f\x15\xaa\xdc\xaa\x94\xc6^\x17\x8c#\xbd\xdf"

        dictionary, data = huffman._unpack(packed)

        self.assertEqual(
            dictionary,
            {
                102: "00",
                52: "010",
                106: "011",
                115: "1000",
                51: "1001",
                57: "1010",
                103: "1011",
                104: "1100",
                53: "11010",
                56: "11011",
                118: "1110",
                99: "11110",
                110: "11111",
            },
        )

        self.assertEqual(data, b"\x15\xaa\xdc\xaa\x94\xc6^\x17\x8c#\xbd\xdf")


if __name__ == "__main__":
    unittest.main()
