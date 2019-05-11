import random
from PIL import Image
import numpy as np
import bitarray

# This program currently represents the least significant bit (of a given byte) first

BITS_MODIFIED_PER_PIXEL = 1
NUM_MSG_LEN_BITS = 16


def convert_msg_to_bits(msg):
    ba = bitarray.bitarray()
    ba.frombytes(msg.encode('utf-32'))
    return ba


def encode_msg(msg_bits, img_bits):
    if len(msg_bits) * 8 / BITS_MODIFIED_PER_PIXEL > len(img_bits):
        print("A message that long can't be encoded in an image that small.")
        return
    for i in range(len(msg_bits)):
        bit_to_encode = msg_bits[i]
        img_bits[ (i // BITS_MODIFIED_PER_PIXEL * 8) + (i % BITS_MODIFIED_PER_PIXEL)] = bit_to_encode
    print(img_bits)
    return img_bits

def getPixelList(image):
    pixel_array = np.array(image)
    return pixel_array





def insertMessege(pixel_list, message):

    width = len(pixel_list[0])
    index = 0
    msg_length = len(message)
    len_bin_str = bin(msg_length)[2:]
    len_ba = bitarray.bitarray()
    for i in range(NUM_MSG_LEN_BITS - len(len_bin_str)):
        len_ba.append(0)
    for bit in len_bin_str:
        len_ba.append(int(bit))
    for i in range(msg_length + NUM_MSG_LEN_BITS):
        index_x = (index + i) % width
        index_y = (index + i) // width
        tuple_val = pixel_list[index_y][index_x]
        red_val = tuple_val[0]
        red_parity = red_val % 2
        if i < NUM_MSG_LEN_BITS:
            red_val += len_ba[i] - red_parity
        else:
            red_val += message[ i - NUM_MSG_LEN_BITS] - red_parity
        pixel_list[index_y][index_x] = (red_val,tuple_val[1],tuple_val[2],tuple_val[3])
    return pixel_list



def createEncodedImage(pixel_list):
    image = Image.fromarray(pixel_list)
    image.save("cat_new.png")

def decodeImage(image2):
    pixel_list = getPixelList(image)
    width = len(pixel_list[0])
    index = 0
    bit_list = []
    word_len = len("nukes in cuba")
    str_bits = ""
    for i in range(8*word_len):
        index_x = (index + i) % width
        index_y = (index + i) // width
        parity = pixel_list[index_y][index_x][0] % 2
        str_bits += str(parity)
        bit_list.append(parity)
    return bit_list

def decodeMessege(bit_list):

    ba = bitarray.bitarray()
    for i in bit_list:

        ba.append(i)
    return_string = ba.tobytes().decode('utf-32')
    print(return_string)






def main():
    image = Image.open("cat.png")

    pixel_list_unModified = getPixelList(image)



    img_array = [] # this will ultimately be the image provided through CLI input
    for i in range(3072): # This loop will be removed once we input images
        img_array.append(random.randint(0,1))
    msg = input("Enter message to encode: ")
    msg_bits = convert_msg_to_bits(msg)
    pixel_list_modified = insertMessege(pixel_list_unModified, msg_bits)
    print()
    createEncodedImage(pixel_list_modified)
    image2 = Image.open("cat_new.png")
    bit_list = decodeImage(image2)
    decodeMessege(bit_list)

    # print("Message bits: " + str(msg_bits))
    # print("Array with message encoded inside: " + str(encode_msg(msg_bits, img_array)))


if __name__ == "__main__":
    main()