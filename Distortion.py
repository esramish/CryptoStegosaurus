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
    for z in mod_pixel_list:

        for j in range(len(z)):

            for colors in range(len(colors_used)):

                '''For each color that is set to change'''

                if colors_used[colors] == 1:
                    binary = bin(z[j][colors])[2:]


                    ''' Pad the binary to be of size 8'''
                    if len(binary) != 8:
                        for k in range(8- len(binary)):
                            binary = "0" + binary

                    '''Change bits_per_color number of bits in a selected color value'''
                    for bit_pos in range(bits_per_color):


                        '''If message is not long enough for the image'''
                        if(i == len(message)):
                            return mod_pixel_list

                        binary = changeBits(binary, bit_pos, int(message[i]))
                        i += 1

                    z[j][colors] = int(binary, 2)
    return mod_pixel_list


def getColorsToChange():

    return_list = [ 0 , 0 , 0 , 0 ]
    red_ans =  input("Do you want to change the red pixel? (y/n):")
    while True:
        if red_ans == "y":
            return_list[0] = 1
            break
        elif red_ans == "n":
            break
        red_ans = input("Please enter y/n: ")


    green_ans = input("Do you want to change the green pixel? (y/n):")
    while True:
        if green_ans == "y":
            return_list[1] = 1
            break
        elif green_ans == "n":
            break
        green_ans = input("Please enter y/n: ")

    blue_ans = input("Do you want to change the blue pixel? (y/n):")
    while True:
        if blue_ans == "y":
            return_list[2] = 1
            break
        elif blue_ans == "n":
            break
        blue_ans = input("Please enter y/n: ")

    transparency_ans = input("Do you want to change the transparency? (y/n):")
    while True:
        if transparency_ans == "y":
            return_list[3] = 1
            break
        elif transparency_ans == "n":
            break
        transparency_ans = input("Please enter y/n: ")


    while True:
        bits = input("How many bits per color value would you like to change? (1-8) ")
        try:
            if 0 <  int(bits) <= 8:
                break
        except:
            pass
        print("Not a valid answer")
    return return_list, int(bits)





def main():
    in_image = Image.open("cat.png")

    pixel_array = np.array(in_image)
    height = len(pixel_array)
    width = len(pixel_array[0])
    color_list, bits_per_color = getColorsToChange()

    colors_used = 0
    for i in color_list:
        if i == 1:
            colors_used += 1

    ''' creates a random message to fill the image '''
    message_len = height*width * bits_per_color * colors_used
    message = makeRandomString(int(message_len))
    message_bits = convert_msg_to_bits(message)

    pixel_list = fillImage(message_bits, pixel_array, color_list, bits_per_color)

    out_image = Image.fromarray(pixel_list)
    out_image.save("cat_new.png")

    print("Done, please check '"'cat_new.png'"' in this directory")


if __name__ == "__main__":
    main()