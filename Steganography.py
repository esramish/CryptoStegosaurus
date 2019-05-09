import random

def convert_msg_to_bits(msg):
    bits = []
    for char in msg: 
        val = ord(char)
        for i in range(8):
            bits.append(not not (val & (2**i)))
    return bits

array = [] # this will ultimately be the image provided through CLI input
def main():
    for i in range(3072): # This loop will be removed once we input images
        array.append(random.randint(0,1))

    
if __name__ == "__main__":
    main()