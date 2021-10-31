# Tämä tiedosto ei varsinaisesti kuulu projektiin,
# mutta laitan sen nyt tänne, jotta
# nähdään miten tarkalleen nopeutta testattiin

import pakkaus
import matplotlib.pyplot as plt
import time

with open("enwik8", "rb") as f:
    data = f.read()

lzw_comp_results = []
huf_comp_results = []
lzw_uncomp_results = []
huf_uncomp_results = []
lzw_efficiency = []
huf_efficiency = []

size = 4096

while size < len(data):
    start_time = time.time()
    lzw_packed = pakkaus.lzw.compress(data[0:size])
    lzw_comp_results.append((size, time.time() - start_time))
    lzw_efficiency.append((size, len(lzw_packed) / size))

    start_time = time.time()
    lzw_unpacked = pakkaus.lzw.uncompress(lzw_packed)
    lzw_uncomp_results.append((size, time.time() - start_time))

    start_time = time.time()
    huf_packed = pakkaus.huffman.pack_data(data[0:size])
    huf_comp_results.append((size, time.time() - start_time))
    huf_efficiency.append((size, len(huf_packed) / size))

    start_time = time.time()
    huf_unpacked = pakkaus.huffman.unpack_data(huf_packed)
    huf_uncomp_results.append((size, time.time() - start_time))

    size *= 2

# https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
def sizeof_fmt(num, _):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}B"
        num /= 1024.0
    return f"{num:.1f}YiB"


fig, (ax1, ax2) = plt.subplots(2)


ax1.xaxis.set_major_formatter(sizeof_fmt)

fig.suptitle("enwik8 pakkaus- ja purkunopeus")

ax1.plot(*zip(*lzw_comp_results), label="LZW Pakkausnopeus")
ax1.plot(*zip(*huf_comp_results), label="Huffman Pakkausnopeus")
ax1.legend(loc="best")

fig.supxlabel("Syötteen koko tavuina")
fig.supylabel("Aika sekunteina")


ax2.xaxis.set_major_formatter(sizeof_fmt)

ax2.plot(*zip(*lzw_uncomp_results), label="LZW Purkamisnopeus")
ax2.plot(*zip(*huf_uncomp_results), label="Huffman Purkamisnopeus")
ax2.legend(loc="best")

fig, ax = plt.subplots()
fig.suptitle("enwik8 pakkaussuhde")


ax.xaxis.set_major_formatter(sizeof_fmt)
ax.yaxis.set_major_formatter(lambda x, _: f"{x*100:.1f}%")

ax.plot(*zip(*lzw_efficiency), label="LZW Pakkaussuhde")
ax.plot(*zip(*huf_efficiency), label="Huffman Pakkaussuhde")
ax.legend(loc="best")
plt.xlabel("Syötteen koko tavuina")
plt.ylabel("Pakkaussuhde")

plt.show()
