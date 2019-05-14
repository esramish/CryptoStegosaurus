import random
from PIL import Image
import numpy as np
import bitarray

def convert_msg_to_bits(msg):
    ba = bitarray.bitarray()
    ba.frombytes(msg.encode('utf-8'))
    return ba

def makeRandomString(avalible_pixels):
    return_str = ""
    for i in range(avalible_pixels):
        return_str += chr(random.randint(0,126))
    return return_str


def changeBits(number, postion, new_val):
    return_str = ""
    bin_list = list(number);
    postion = len(bin_list) - postion -1
    bin_list[postion] = new_val


    for i in bin_list:
        return_str += str(int(i))

    return return_str


def fillImage(message, pixel_list,  colors_used, bits_per_color):
    mod_pixel_list = pixel_list

    i = 0
    try:
        for z in mod_pixel_list:

            for j in range(len(z)):
                for colors in range(len(colors_used)):

                    if colors_used[colors] == 0:
                        x = 1
                        #color_vals.append(z[j][colors])


                    else:
                        binary = bin(z[j][colors])[2:]


                        if len(binary) != 8:
                            for k in range(8- len(binary)):
                                binary = "0" + binary

                        for bit_pos in range(bits_per_color):

                            if(i == len(message)):
                                return mod_pixel_list

                            binary = changeBits(binary, bit_pos, int(message[i]))
                            i += 1


                        z[j][colors] = int(binary, 2)



    except IndexError:
        return mod_pixel_list

    return mod_pixel_list








def main():
    image = Image.open("cat.png")

    pixel_array = np.array(image)
    height = len(pixel_array)
    width = len(pixel_array[0])

    color_list = [1,1,1,0]
    colors_used = 0
    bits_per_color = 7
    for i in color_list:
        if i == 1:
            colors_used += 1

    message_len = height*width * bits_per_color * colors_used

    message = makeRandomString(message_len)
    message_bits = convert_msg_to_bits(message)

    hi_message_bits = convert_msg_to_bits("h")

    pixel_list = fillImage(message_bits, pixel_array, color_list, bits_per_color)


    image = Image.fromarray(pixel_list)
    image.save("cat_new.png")

if __name__ == "__main__":
    main()