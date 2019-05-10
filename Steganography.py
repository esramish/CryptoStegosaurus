import random

# This program currently represents the least significant bit (of a given byte) first

BITS_MODIFIED_PER_PIXEL = 1

def convert_msg_to_bits(msg):
    bits = []
    for char in msg: 
        val = ord(char)
        for i in range(8):
            bit_as_bool = not not (val & (2**i))
            bits.append(bit_as_bool * 1)
    return bits

def encode_msg(msg_bits, img_bits):
    if len(msg_bits) * 8 / BITS_MODIFIED_PER_PIXEL > len(img_bits):
        print("A message that long can't be encoded in an image that small.")
        return
    for i in range(len(msg_bits)):
        bit_to_encode = msg_bits[i]
        img_bits[ (i // BITS_MODIFIED_PER_PIXEL * 8) + (i % BITS_MODIFIED_PER_PIXEL)] = bit_to_encode
    return img_bits

def main():
    img_array = [] # this will ultimately be the image provided through CLI input
    for i in range(3072): # This loop will be removed once we input images
        img_array.append(random.randint(0,1))
    msg = input("Enter message to encode: ")
    msg_bits = convert_msg_to_bits(msg)
    print("Message bits: " + str(msg_bits))
    print("Array with message encoded inside: " + str(encode_msg(msg_bits, img_array)))
    
if __name__ == "__main__":
    main()