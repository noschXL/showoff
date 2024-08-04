import math
import random
import time
from sys import exit

testdata = "test"
passcode = "ppLojXiX"

replacement = "1234567890?ß+#*'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

'''
spiral:
abcd # 1
lmne # 2
kpof # 3
jihg #if to much just add the rest from top to bottom

matrix:
abcd
efgh
ijkl
mnop

if to much its the same as spiral

normal:
abcdefghijklmnop123

reversed:
321ponmlkjihgfedcba
'''

def my_hash(passcode):
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
        
    
    #hashing the passcode
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

def my_encodeing(data: str, passcode: str = ""):

    hashed_passcode = my_hash(passcode)
    if hashed_passcode == None:
        exit()

    # handeling the data to be encrypted
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]

    oldmode = 2
    for charp in range(0, len(hashed_passcode), 2):
        mode = int(hashed_passcode[charp]) % 4

        if mode == 0:
            #spiral mode
            lenght = math.floor(math.sqrt(len(data)))
            curr_dir = 0
            for i in range(lenght ** 2):
                pass
            pass
        elif mode == 1:
            #matrix mode
            pass
        elif mode == 2:
            #normal mode
            pass
        elif mode == 3:
            #reversed mode
            pass
        else:
            print(f"something went wrong {mode = }")

generated = []
start = time.time()
for x in range(100000):
    gened = my_hash(str(x))
    if gened in generated:
        #print(f"whoops at{generated.index(gened)} which is {generated[generated.index(gened)]} and {x} with hash {gened}")
        pass
    else:
        generated.append(gened)
    print(f"{x = }")

print(f"runtime: {time.time() - start}s")