import time
import math
import random
from sys import exit

def my_hash(passcode):
    # Your provided hash function
    if passcode == "":
        yorn = input("you entered an empty passcode, shame on you. should i generate an random 8 character code instead?\n" +
                     "If you type n the process will end and nothing happens(y/n): ")
        if yorn.lower() == "y" or yorn.lower() == "yes":
            passcode = ""
            for _ in range(8):
                passcode += random.choice(replacement)
            print(f"your {passcode} = ")
        else:
            print("i cant use an empty passcode, sry.")
            return None
        
    # hashing the passcode
    passcode = "a" + passcode
    passcode = passcode.encode().hex()
    new = ""
    passcode = int(passcode[len(passcode) // 2:], 16) * int(passcode[:math.floor(len(passcode) // 2)], 16)
    passcode = bin(passcode)
    reversedpasscode = passcode[2:][::-1]
    newhashedpasscode = ""

    for i, bit in enumerate(passcode[2:]):
        boola = int(bit)
        boolb = int(reversedpasscode[i])
        fbool = boola ^ boolb
        newhashedpasscode += str(int(fbool))

    passcode = str(int(newhashedpasscode,2))

    if len(passcode) % 2 == 1:
        qsum = 0
        for char in passcode:
            qsum += int(char)
        passcode += str(qsum)[-1]

    return passcode

def detect_collisions(range_limit):
    hash_dict = {}
    collisions = []
    
    start = time.time()
    
    for x in range(range_limit):
        hash_value = my_hash(str(x))
        
        if hash_value in hash_dict:
            collisions.append((hash_dict[hash_value], x, hash_value))
        else:
            hash_dict[hash_value] = x
    
    print(f"Runtime: {time.time() - start}s")
    
    if collisions:
        print("Collisions found:")
        for item in collisions:
            print(f"Original input: {item[0]}, Collision input: {item[1]}, Hash: {item[2]}")
    else:
        print("No collisions found.")

# Adjust the range limit based on your needs
detect_collisions(10000)
