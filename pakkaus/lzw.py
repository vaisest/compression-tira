"Tämä moduuli toteuttaa LZW-pakkausalgoritmin Tiralabraa varten."


def compress(data: bytes) -> bytes:
    dictionary = dict()
    for i in range(0, 256):
        dictionary[i.to_bytes(1, "big")] = i.to_bytes(2, "big")

    results = bytes()

    string = bytes()

    pointer = 0

    while len(data) > pointer:
        char = data[pointer : pointer + 1]
        if string + char in dictionary:
            string += char
        else:
            results += dictionary[string]

            dictionary[string + char] = len(dictionary).to_bytes(2, "big")
            string = char
        pointer += 1
    results += dictionary[string]

    return results


def decompress(data: bytes) -> bytes:

    dictionary: list[bytes] = list()
    for i in range(0, 256):
        dictionary.append(i.to_bytes(1, "big"))

    output = bytes()

    for i in range(0, len(data) - 1, 2):
        code = (data[i] << 8) | data[i + 1]

        string = dictionary[code]
        output += string

        if i + 3 < len(data) and (data[i + 2] << 8) | data[i + 3] < len(dictionary):
            next_code = (data[i + 2] << 8) | data[i + 3]
            string += dictionary[next_code][0:1]
        else:
            string += string[0:1]
        dictionary.append(string)

    return output
