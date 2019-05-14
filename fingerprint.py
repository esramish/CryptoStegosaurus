import random, json
from PIL import Image
import numpy as np
import bitarray
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

DEFAULT_BACKEND = default_backend()
# This program currently represents the least significant bit (of a given byte) first

BITS_MODIFIED_PER_PIXEL = 1
NUM_MSG_LEN_BITS = 16
ORIGINAL_COPY = "cat.png"

STORAGE = "id_table.txt"


def sha256( data ):
    h = hashes.Hash( hashes.SHA256(), backend=DEFAULT_BACKEND )
    h.update( data )
    return h.finalize()

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

    width = len(image_pixels[0])
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
        pixel_tuple = image_pixels[index_y][index_x]
        pixel_list = list(pixel_tuple)

        parity = pixel_list[0] % 2
        if i < NUM_MSG_LEN_BITS:
            pixel_list[0] += len_ba[i] - parity
        else:
            pixel_list[0] += message[ i - NUM_MSG_LEN_BITS] - parity
        image_pixels[index_y][index_x] = tuple(pixel_list)
    return image_pixels

def createEncodedImage(image_pixels, id):
    image = Image.fromarray(image_pixels)
    image.save(id +"_"+ ORIGINAL_COPY)

    print("Encoded image saved as '%s'" % (id +"_"+ ORIGINAL_COPY))

def extractMessage(image):

    image_pixels = getPixelList(image)
    width = len(image_pixels[0])
    index = 0
    message_length = 0

    i = 0
    message_ba = bitarray.bitarray()
    while i < NUM_MSG_LEN_BITS + message_length:
        index_x = (index + i) % width
        index_y = (index + i) // width

        parity = image_pixels[index_y][index_x][0] % 2
        if i < NUM_MSG_LEN_BITS:
            message_length += parity * 2**(NUM_MSG_LEN_BITS - i - 1)
        else:
            message_ba.append(parity)
        i+=1
    try:
        return_string = message_ba.tobytes().decode('utf-32')
        return return_string
    except:
        return None



def do_encoding(msg, id):
    image = Image.open(ORIGINAL_COPY)
    image_pixels_unModified = getPixelList(image)
    msg_bits = convert_msg_to_bits(msg)
    image_pixels_modified = insertMessege(image_pixels_unModified, msg_bits)
    createEncodedImage(image_pixels_modified, id)

def do_decoding(filename):

    image = Image.open(filename)
    message = extractMessage(image)
    return message

def fprintNew(id):
    list = []
    file_write = open(STORAGE,"a+")
    file_read = open(STORAGE, "r")
    counter = 0
    while file_read.readline() != "":
        counter+=1
    message = sha256(counter.to_bytes(8, 'big',  signed=False)).hex()
    do_encoding(message, id)
    list.append(message)
    list.append(id)
    file_write.write(json.dumps(list))
    file_write.write("\n")

def findID():
    try:
        filename = input("Enter the filename of the image: ")
        image = Image.open(filename)
    except:
        print("File '%s' not found" % filename)
        return
    message = do_decoding(filename)
    if message == None:
        print("Decoding failed. Sad.")
        return
    try:
        file = open(STORAGE,'r')
    except:
        print("You lost your table, sad")
        return
    line = file.readline()
    while line != "":
        list = json.loads(line)
        if (message == list[0]):
            print (list[1])
            return
        line = file.readline()
    print("Sorry couldn't find it")

def main():
    while True:
        print("\nWhat would you like to do?")
        print("1: Fingerprint a new copy")
        print("2: Find the identity of a copy")
        print("3: Quit")
        selection = input("> ")
        if selection == "1":
            issueTo = input("Who are you issuing this copy to? ")
            fprintNew(issueTo)
        elif selection == "2":
            findID()
        elif selection == "3":
            return
        else:
            print("Please enter one of the numbers above.")


if __name__ == "__main__":
    main()
