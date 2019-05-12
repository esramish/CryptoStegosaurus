import random
from PIL import Image
import numpy as np
import bitarray

# This program currently represents the least significant bit (of a given byte) first

BITS_MODIFIED_PER_PIXEL = 1
NUM_MSG_LEN_BITS = 16

seed = None


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





def insertMessege(image_pixels, message):
    global seed
    width = len(image_pixels[0])
    index = 0
    msg_length = len(message)
    len_bin_str = bin(msg_length)[2:]
    len_ba = bitarray.bitarray()
    for i in range(NUM_MSG_LEN_BITS - len(len_bin_str)):
        len_ba.append(0)
    for bit in len_bin_str:
        len_ba.append(int(bit))
    random.seed(seed)
    for i in range(msg_length + NUM_MSG_LEN_BITS):
        index_x = (index + i) % width
        index_y = (index + i) // width
        pixel_tuple = image_pixels[index_y][index_x]
        pixel_list = list(pixel_tuple)
        color_num = random.randint(0, 2)
        parity = pixel_list[color_num] % 2
        if i < NUM_MSG_LEN_BITS:
            pixel_list[color_num] += len_ba[i] - parity
        else:
            pixel_list[color_num] += message[ i - NUM_MSG_LEN_BITS] - parity
        image_pixels[index_y][index_x] = tuple(pixel_list)
    return image_pixels



def createEncodedImage(image_pixels, old_filename):
    image = Image.fromarray(image_pixels)
    image.save("output_"+old_filename)
    print("Encoded image saved as 'output_%s'" % old_filename)

def decodeImage(image):
    image_pixels = getPixelList(image)
    width = len(image_pixels[0])
    index = 0
    bit_list = []
    word_len = len("nukes in cuba")
    str_bits = ""
    for i in range(8*word_len):
        index_x = (index + i) % width
        index_y = (index + i) // width
        parity = image_pixels[index_y][index_x][0] % 2
        str_bits += str(parity)
        bit_list.append(parity)
    return bit_list

def decodeMessege(bit_list):

    ba = bitarray.bitarray()
    for i in bit_list:

        ba.append(i)
    return_string = ba.tobytes().decode('utf-32')
    print(return_string)

def set_seed():
    global seed
    while True: 
        try: 
            seed = int(input("Enter secret seed: \n"))
            return seed
        except: 
            print("Please enter a number.")

def do_encoding():
    if seed == None:
        print("Need to set seed first")
        return
    while True:
        try:
            filename = input("Enter image filename: ")
            image = Image.open(filename)
            break
        except: 
            print("File '%s' not found" % filename)
    image_pixels_unModified = getPixelList(image)
    msg = input("Enter message to encode: ")
    msg_bits = convert_msg_to_bits(msg)
    image_pixels_modified = insertMessege(image_pixels_unModified, msg_bits)
    createEncodedImage(image_pixels_modified, filename)
    
def do_decoding():
    if seed == None:
        print("Need to set seed first")
        return
    image2 = Image.open("cat_new.png")
    bit_list = decodeImage(image2)
    decodeMessege(bit_list)


def main():
    while True:
        print("\nWhat would you like to do?")
        print("1: Set secret seed")
        print("2: Encode message in image")
        print("3: Decode message from image")
        print("4: Quit")
        selection = input("> ")
        if selection == "1":
            set_seed()
        elif selection == "2":
            do_encoding()
        elif selection == "3":
            do_decoding()
        elif selection == "4":
            return
        else:
            print("Please enter one of the numbers above.")


if __name__ == "__main__":
    main()