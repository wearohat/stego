#  Stego — Image-Based Text Steganography Too

Stego is a simple command-line steganography tool that lets you **hide** and **extract** secret text messages inside PNG images using the least significant bit (LSB) technique.

---

## Features

-  Hide secret UTF-8 messages in PNG images
-  Extract hidden messages from images
-  Supports both RGB and RGBA image modes
-  Smart capacity checking to prevent oversized messages

---

## Requirements

- Python 3.x
- Pillow (Python Imaging Library)

---

## Usage

### Embed a message

```bash
python stego.py embed input.png output.png "Your secret message"
```

### Extract a message

```bash
python stego.py extract input.png
```

## How It Works

- Encodes your message into binary
- Stores the bit length of the message in the first 32 bits (header)
- Embeds the message bits in the least significant bits of the image pixels
- Image appearance remains unchanged to the human eye

---

## Limitations

- Only supports PNG format
- Maximum message size depends on the image's pixel count
- 32 bits are used to store the message length (header)

---


