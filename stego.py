"""

CREATED BY WEARDHAT


"""

import sys
from PIL import Image

HEADER_SIZE = 32 

def _int_to_bits(n, length):
    return [(n >> i) & 1 for i in range(length)]

def _bits_to_int(bits):
    n = 0
    for i, b in enumerate(bits):
        n |= (b & 1) << i
    return n

def _bytes_to_bits(data_bytes):
    for byte in data_bytes:
        for i in range(8):
            yield (byte >> i) & 1

def _bits_to_bytes(bits):
    b = bytearray()
    byte = 0
    count = 0
    for i, bit in enumerate(bits):
        byte |= (bit & 1) << (count)
        count += 1
        if count == 8:
            b.append(byte)
            byte = 0
            count = 0
    return bytes(b)

def embed_message(in_path, out_path, message):
    img = Image.open(in_path)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")
    pixels = list(img.getdata())
    total_channels = len(pixels) * (4 if img.mode == "RGBA" else 3)

    data_bytes = message.encode("utf-8")
    msg_bits_len = len(data_bytes) * 8

    if HEADER_SIZE + msg_bits_len > total_channels:
        raise ValueError("Message too large to fit in the image.")

    header_bits = _int_to_bits(msg_bits_len, HEADER_SIZE)
    message_bits = list(_bytes_to_bits(data_bytes))
    all_bits = header_bits + message_bits

    flat = []
    for px in pixels:
        if img.mode == "RGBA":
            flat.extend(px)  
        else:
            flat.extend(px)  

    for i, bit in enumerate(all_bits):
        flat[i] = (flat[i] & ~1) | bit

    new_pixels = []
    step = 4 if img.mode == "RGBA" else 3
    for i in range(0, len(flat), step):
        new_pixels.append(tuple(flat[i:i+step]))

    stego = Image.new(img.mode, img.size)
    stego.putdata(new_pixels)
    stego.save(out_path, "PNG")
    print(f"Embedded {len(data_bytes)} bytes ({msg_bits_len} bits) into {out_path}")

def extract_message(in_path):
    img = Image.open(in_path)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")
    pixels = list(img.getdata())
    flat = []
    for px in pixels:
        if img.mode == "RGBA":
            flat.extend(px)
        else:
            flat.extend(px)

    header_bits = [flat[i] & 1 for i in range(HEADER_SIZE)]
    msg_bits_len = _bits_to_int(header_bits)
    if msg_bits_len == 0:
        print("No hidden message found (length 0).")
        return

    bits = [flat[i] & 1 for i in range(HEADER_SIZE, HEADER_SIZE + msg_bits_len)]
    message_bytes = _bits_to_bytes(bits)
    try:
        message = message_bytes.decode("utf-8")
    except UnicodeDecodeError:
        message = None
    print(f"Extracted {len(message_bytes)} bytes ({msg_bits_len} bits).")
    if message is None:
        print("Warning: extracted bytes could not be decoded as UTF-8. Raw bytes follow:")
        print(message_bytes.hex())
    else:
        print("Message:")
        print(message)

def print_usage():
    print("Usage:")
    print("  python stego.py embed input.png output.png \"Secret message\"")
    print("  python stego.py extract input.png")

def main():
    if len(sys.argv) < 3:
        print_usage(); return
    cmd = sys.argv[1].lower()
    if cmd == "embed":
        if len(sys.argv) != 5:
            print_usage(); return
        in_path = sys.argv[2]
        out_path = sys.argv[3]
        message = sys.argv[4]
        embed_message(in_path, out_path, message)
    elif cmd == "extract":
        if len(sys.argv) != 3:
            print_usage(); return
        extract_message(sys.argv[2])
    else:
        print_usage()

if __name__ == "__main__":
    main()
