
def decode(input: str):

    ret = input.encode("ascii")
    ret = int(ret.hex(), 16)
    ret = bin(ret)
    return ret

if __name__ == "__main__":
    print(decode("www.youtube.com"))