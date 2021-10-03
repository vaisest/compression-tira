import os
import unittest
from random import shuffle

from pakkaus import lzw


class TestLzwFunctions(unittest.TestCase):
    def test_compressing_files(self):
        file_contents = (
            f"""
            This is a test file
            for the
            tir@l@Br@! :))
            """
            * 5000
        )

        # jotta saadaan sanakirjan tyhjennys toimimaan
        file_contents = list(file_contents)
        shuffle(file_contents)
        file_contents = "".join(file_contents)

        source_file = "AUTOMATED.TEST.FILE.txt"
        destination_file = "AUTOMATED.TEST.FILE.LZW"
        unpacked_file = "AUTOMATED.TEST.FILE.unpacked.txt"

        with open(source_file, "w") as f:
            f.write(file_contents)

        lzw.compress_file(source_file, destination_file)

        lzw.uncompress_file(destination_file, unpacked_file)

        with open(unpacked_file, "r") as f:
            unpacked = f.read()

        self.assertEqual(file_contents, unpacked)

        os.remove(source_file)
        os.remove(destination_file)
        os.remove(unpacked_file)
