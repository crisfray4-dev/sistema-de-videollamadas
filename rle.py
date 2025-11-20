import struct
import numpy as np

def rle_encode_array(arr):
    """Recibe un array 1D uint8 y devuelve lista de pares (value, count)."""
    if arr.size == 0:
        return []
    out = []
    prev = int(arr[0])
    count = 1
    for v in arr[1:]:
        v = int(v)
        if v == prev:
            count += 1
            if count == 65535:   # límite para almacenar en uint16
                out.append((prev, count))
                count = 0
        else:
            if count > 0:
                out.append((prev, count))
            prev = v
            count = 1
    if count > 0:
        out.append((prev, count))
    return out

def rle_encode_to_bytes(arr):
    """Codifica un array 1D (numpy uint8) a bytes usando RLE compactado:
    formato por run: (uint8 value) + (uint16 count big-endian) => 3 bytes por run.
    Devuelve bytes.
    """
    pairs = rle_encode_array(arr)
    b = bytearray()
    for val, count in pairs:
        while count > 0:
            take = min(count, 65535)
            b.extend(struct.pack('>BH', val, take))
            count -= take
    return bytes(b)

def rle_decode_from_bytes(b):
    """Decodifica bytes en el formato anterior y devuelve un numpy 1D uint8 array."""
    runs = []
    i = 0
    n = len(b)
    while i + 3 <= n:
        val = b[i]
        count = int.from_bytes(b[i+1:i+3], 'big')
        runs.append((val, count))
        i += 3
    # expandir runs
    out = []
    for val, count in runs:
        out.extend([val] * count)
    return np.array(out, dtype=np.uint8)
