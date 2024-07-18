import struct
import zlib
import numpy

path = "/home/nosch/Documents/logo.png"
PngSignature = b'\x89PNG\r\n\x1a\n'

def read_chunk(f):
    # Returns (chunk_type, chunk_data)
    chunk_length, chunk_type = struct.unpack('>I4s', f.read(8))
    chunk_data = f.read(chunk_length)
    checksum = zlib.crc32(chunk_data, zlib.crc32(struct.pack('>4s', chunk_type)))
    chunk_crc, = struct.unpack('>I', f.read(4))
    if chunk_crc != checksum:
        raise Exception('chunk checksum failed {} != {}'.format(chunk_crc,
            checksum))
    return chunk_type, chunk_data

def Recon_a(Recon, stride,r, c, bytesPerPixel):
    return Recon[r * stride + c - bytesPerPixel] if c >= bytesPerPixel else 0

def Recon_b(Recon, stride,r, c, bytesPerPixel):
    return Recon[(r-1) * stride + c] if r > 0 else 0

def Recon_c(Recon, stride,r, c, bytesPerPixel):
    return Recon[(r-1) * stride + c - bytesPerPixel] if r > 0 and c >= bytesPerPixel else 0

def PaethPredictor(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        Pr = a
    elif pb <= pc:
        Pr = b
    else:
        Pr = c
    return Pr

def decodepng(path):
    f = open(path, "rb")
    if f.read(len(PngSignature)) != PngSignature:
        raise Exception('Invalid PNG Signature')
    chunks = []
    while True:
        chunk_type, chunk_data = read_chunk(f)
        chunks.append((chunk_type, chunk_data))
        if chunk_type == b'IEND':
            break

    _, IHDR_data = chunks[0] # IHDR is always first chunk
    width, height, bitd, colort, compm, filterm, interlacem = struct.unpack('>IIBBBBB', IHDR_data)
    if compm != 0:
        raise Exception('invalid compression method')
    if filterm != 0:
        raise Exception('invalid filter method')
    if colort != 6:
        raise Exception('we only support truecolor with alpha')
    if bitd != 8:
        raise Exception('we only support a bit depth of 8')
    if interlacem != 0:
        raise Exception('we only support no interlacing')
    
    print(f"{width, height = }")

    IDAT_data = b''.join(chunk_data for chunk_type, chunk_data in chunks if chunk_type == b'IDAT')
    IDAT_data = zlib.decompress(IDAT_data)
    

    Recon = []
    bytesPerPixel = 4
    stride = width * bytesPerPixel


    i = 0
    for r in range(height): # for each scanline
        filter_type = IDAT_data[i] # first byte of scanline is filter type
        i += 1
        for c in range(stride): # for each byte in scanline
            Filt_x = IDAT_data[i]
            i += 1
            if filter_type == 0: # None
                Recon_x = Filt_x
            elif filter_type == 1: # Sub
                Recon_x = Filt_x + Recon_a(Recon, stride, r, c, bytesPerPixel)
            elif filter_type == 2: # Up
                Recon_x = Filt_x + Recon_b(Recon, stride, r, c, bytesPerPixel)
            elif filter_type == 3: # Average
                Recon_x = Filt_x + (Recon_a(Recon, stride, r, c, bytesPerPixel) + Recon_b(Recon, stride, r, c, bytesPerPixel)) // 2
            elif filter_type == 4: # Paeth
                Recon_x = Filt_x + PaethPredictor(Recon_a(Recon, stride, r, c, bytesPerPixel), Recon_b(Recon, stride, r, c, bytesPerPixel), Recon_c(Recon, stride, r, c, bytesPerPixel))
            else:
                raise Exception('unknown filter type: ' + str(filter_type))
            Recon.append(Recon_x & 0xff) # truncation to byte

    data = numpy.array(Recon).reshape((height, width, 4))
    data = numpy.fliplr(data)
    data = numpy.rot90(data , 1, axes=(0,1))
    return width, height, data
    

if __name__ == "__main__":
    decodepng("/home/nosch/Documents/code/ascii/basn6a08.png")