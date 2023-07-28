import os
import pickle
import pyaes
import sys
import wave
import numpy as np
import cv2


def txt_encode(text, text_cover_file):
    i = 0
    add = ''
    while i < len(text):
        t = ord(text[i])
        if 32 <= t <= 64:
            t1 = t + 48
            t2 = t1 ^ 170  # 170: 10101010
            res = bin(t2)[2:].zfill(8)
            add += "0011" + res

        else:
            t1 = t - 48
            t2 = t1 ^ 170
            res = bin(t2)[2:].zfill(8)
            add += "0110" + res
        i += 1
    res1 = add + "111111111111"
    zwc = {"00": u'\u200C', "01": u'\u202C', "11": u'\u202D', "10": u'\u200E'}
    file1 = open(text_cover_file, "r+")
    name_of_file = "stego_text.txt"
    file3 = open(name_of_file, "w+", encoding="utf-8")
    word = []
    for line in file1:
        word += line.split()
    i = 0
    while i < len(res1):
        s = word[int(i / 12)]
        j = 0
        hm_sk = ""
        while j < 12:
            x = res1[j + i] + res1[i + j + 1]
            hm_sk += zwc[x]
            j += 2
        s1 = s + hm_sk
        file3.write(s1)
        file3.write(" ")
        i += 12
    t = int(len(res1) / 12)
    while t < len(word):
        file3.write(word[t])
        file3.write(" ")
        t += 1
    file3.close()
    file1.close()
    print("\nData successfully stored in the file : %s" % name_of_file)


def encode_txt_data(msg, file_type):
    count2 = 0
    cover_file = input("\nEnter name of text file in which you want to encode the data : ")
    textfile = open(cover_file, "r")
    for line in textfile:
        for _ in line.split():
            count2 = count2 + 1
    textfile.close()
    bt = int(count2)
    print("\nMaximum number of words that can be inserted : ", int(bt / 6))
    text1 = msg + ("#type#%s" % file_type)
    length = len(text1)
    if length <= bt:
        print("\nInput message can be hidden in the cover file")
        txt_encode(text1, cover_file)
    else:
        print("Total bytes in the provided data : ", length)
        print("\nData size is too big! Please reduce data size or hide data in a bigger text file")
        return


def binary_to_decimal(binary):
    string = int(binary, 2)
    return string


def decode_txt_data():
    zwc_reverse = {u'\u200C': "00", u'\u202C': "01", u'\u202D': "11", u'\u200E': "10"}
    stego = input("\nEnter the PATH of stego TEXT file (!! WITH EXTENSION !!) to decode the message : ")
    file4 = open(stego, "r", encoding="utf-8")
    temp = ''
    for line in file4:
        for words in line.split():
            t1 = words
            binary_extract = ""
            for letter in t1:
                if letter in zwc_reverse:
                    binary_extract += zwc_reverse[letter]
            if binary_extract == "111111111111":
                break
            else:
                temp += binary_extract
    i = 0
    a = 0
    b = 4
    c = 4
    d = 12
    final = ''
    while i < len(temp):
        t3 = temp[a:b]
        a += 12
        b += 12
        i += 12
        t4 = temp[c:d]
        c += 12
        d += 12
        if t3 == '0110':
            decimal_data = binary_to_decimal(t4)
            final += chr((decimal_data ^ 170) + 48)
        elif t3 == '0011':
            decimal_data = binary_to_decimal(t4)
            final += chr((decimal_data ^ 170) - 48)
    return final


def msg_to_binary(msg):
    if type(msg) == str:
        result = ''.join([format(ord(i), "08b") for i in msg])

    elif type(msg) == bytes or type(msg) == np.ndarray:
        result = [format(i, "08b") for i in msg]

    elif type(msg) == int or type(msg) == np.uint8:
        result = format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    return result


def encode_img_data(msg, file_type):
    img = cv2.imread(input("\nEnter PATH of image in which data is to be encrypted : "))
    data = msg + ("#type#%s" % file_type)
    if len(data) == 0:
        raise ValueError('Data entered to be encoded is empty')

    name_of_file = "stego_image.png"

    no_of_bytes = (img.shape[0] * img.shape[1] * 3) // 8

    print("\t\nMaximum bytes that can be encoded in Image :", no_of_bytes)

    try:
        if len(data) > no_of_bytes:
            raise ValueError()
    except ValueError:
        print("Total bytes in the provided data : ", len(data))
        print("Insufficient bytes Error, Need Bigger Image or give Less Data !!")
        return

    data += '*^*^*'

    binary_data = msg_to_binary(data)

    length_data = len(binary_data)

    index_data = 0

    for i in img:
        for pixel in i:
            r, g, b = msg_to_binary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data >= length_data:
                break
    cv2.imwrite(name_of_file, img)
    print("\nEncoded the data successfully in the Image and it is successfully saved with name : %s" % name_of_file)


def decode_img_data():
    img = cv2.imread(input("\nEnter the PATH of the image you need to Decode to get the Secret message : "))
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = msg_to_binary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
            total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    return decoded_data[:-5]


def encode_aud_data(msg, file_type):
    name_of_file = input("\nEnter name of the file (!! WITH EXTENSION !!) in which message is to be encoded : ")
    song = wave.open(name_of_file, mode='rb')

    n_frames = song.getnframes()
    frames = song.readframes(n_frames)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    data = msg + ("#type#%s" % file_type)

    data = data + '*^*^*'

    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0
    for i in range(0, len(result), 1):
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res) - 4] == result[i]:
            frame_bytes[j] = (frame_bytes[j] & 253)  # 253: 11111101
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j = j + 1

    frame_modified = bytes(frame_bytes)

    stego_file = "stego_audio.wav"
    with wave.open(stego_file, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    print("\nEncoded the data successfully in the audio file : %s" % stego_file)
    song.close()


def decode_aud_data():
    name_of_file = input("\nEnter name of the stego file to be decoded : ")
    song = wave.open(name_of_file, mode='rb')

    n_frames = song.getnframes()
    frames = song.readframes(n_frames)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    extracted = ""
    for i in range(len(frame_bytes)):
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res) - 2] == 0:
            extracted += res[len(res) - 4]
        else:
            extracted += res[len(res) - 1]

        all_bytes = [extracted[i: i + 8] for i in range(0, len(extracted), 8)]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "*^*^*":
                return decoded_data[:-5]


def ksa(key):
    key_length = len(key)
    s_list = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s_list[i] + key[i % key_length]) % 256
        s_list[i], s_list[j] = s_list[j], s_list[i]
    return s_list


def prga(s_list, n):
    i = 0
    j = 0
    key = []
    while n > 0:
        n = n - 1
        i = (i + 1) % 256
        j = (j + s_list[i]) % 256
        s_list[i], s_list[j] = s_list[j], s_list[i]
        k_add = s_list[(s_list[i] + s_list[j]) % 256]
        key.append(k_add)
    return key


def preparing_key_array(s):
    return [ord(c) for c in s]


def encryption(plaintext, key):
    key = preparing_key_array(key)

    s_list = ksa(key)

    key_stream = np.array(prga(s_list, len(plaintext)))
    plaintext = np.array([ord(i) for i in plaintext])

    cipher = key_stream ^ plaintext
    ctext = ''
    for c in cipher:
        ctext = ctext + chr(c)
    return ctext


def decryption(ciphertext, key):
    key = preparing_key_array(key)

    s_list = ksa(key)

    key_stream = np.array(prga(s_list, len(ciphertext)))
    ciphertext = np.array([ord(i) for i in ciphertext])

    decoded = key_stream ^ ciphertext
    decoded_text = ''
    for c in decoded:
        decoded_text = decoded_text + chr(c)
    return decoded_text


def embed(frame, msg, key):
    data = msg
    data = encryption(data, key)
    if len(data) == 0:
        raise ValueError('Data entered to be encoded is empty')

    data += '*^*^*'

    binary_data = msg_to_binary(data)
    length_data = len(binary_data)

    index_data = 0

    for i in frame:
        for pixel in i:
            r, g, b = msg_to_binary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data >= length_data:
                break
        return frame


def extract(frame, key):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msg_to_binary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
            total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    for j in range(0, len(decoded_data) - 5):
                        final_decoded_msg += decoded_data[j]
                    final_decoded_msg = decryption(final_decoded_msg, key)
                    return final_decoded_msg


def encode_vid_data(msg, file_type):
    cover_video = input("\nEnter the video file (!! WITH EXTENSION !!) in which you want to encode data : ")
    cap = cv2.VideoCapture(cover_video)
    vid_cap = cv2.VideoCapture(cover_video)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vid_cap.get(3))
    frame_height = int(vid_cap.get(4))

    size = (frame_width, frame_height)
    out = cv2.VideoWriter('stego_video.mp4', fourcc, 25.0, size)
    max_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        max_frame += 1
    cap.release()
    msg = msg + ("#type#%s" % file_type)
    each_msg_len = len(msg) // 7
    msg_list = [msg[i:i + each_msg_len] for i in range(0, len(msg), each_msg_len)]
    print("\nTotal number of frames in selected Video :", max_frame)
    print("\nMaximum available start frame : ", max_frame - len(msg_list))
    n = int(input("\nEnter the start frame number where you want to embed data "
                  "(!! FRAME VALUE MUST BE <= %s : " % (max_frame - len(msg_list))))
    key = input("\nEnter the key : ")
    frame_number = 0
    total_frames = []
    while vid_cap.isOpened():
        frame_number += 1
        ret, frame = vid_cap.read()
        if not ret:
            break
        if frame_number == n - 1:
            for i in range(len(msg_list)):
                ret, frame = vid_cap.read()
                change_frame_with = embed(frame, msg_list[i], key)
                frame = change_frame_with
                out.write(frame)
                total_frames.append(frame)
        out.write(frame)

    print("\nEncoded the data successfully in the video file : %s" % "stego_video.mp4")
    with open('video_frame_file.pkl', 'wb') as file:
        pickle.dump(total_frames, file)


def decode_vid_data():
    with open('video_frame_file.pkl', 'rb') as file:
        frame_ = pickle.load(file)

    cap = cv2.VideoCapture('stego_video.mp4')
    max_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        max_frame += 1
    print("\nTotal number of Frame in selected Video : ", max_frame)
    n = int(input("\nEnter the secret frame number from where you want to start extracting data : "))
    key = input("\nEnter the key : ")
    vid_cap = cv2.VideoCapture('stego_video.mp4')
    frame_number = 0
    final_message = ""
    while vid_cap.isOpened():
        frame_number += 1
        ret, frame = vid_cap.read()
        if not ret:
            break
        if frame_number == n - 1:
            for i in frame_:
                final_message += extract(i, key)
    return final_message


def encrypt():
    pub_key = input("\nEnter PUBLIC KEY file name (!! WITH EXTENSION !!) : ")
    plain_text = input("\nEnter PATH of file TO BE ENCRYPTED : ")
    msg_type = plain_text.split(".")[-1]
    n, e = open(pub_key, 'r').read().split(',')
    plain_text = open(plain_text, 'rb').read()
    aes_key = os.urandom(16)
    cipher_text = pyaes.AESModeOfOperationCTR(aes_key).encrypt(plain_text)
    p = int.from_bytes(aes_key, sys.byteorder)
    e, n = int(e), int(n)
    cipher_key = pow(p, e, n)
    cipher_key = bytes(str(cipher_key).encode())
    return (b'%b %b' % (cipher_text, cipher_key)), msg_type


def decrypt(encoded_message):
    file_type = encoded_message.split("#type#")[-1]
    prv_key = input("\nEnter PRIVATE KEY file name (!! WITH EXTENSION !!) : ")
    plain_text = "secretMessage.%s" % file_type
    n, d = open(prv_key, 'r').read().split(',')
    c_items = bytes.fromhex(encoded_message.split("#type#")[-2]).split(b' ')
    cipher_text = b' '.join(c_items[:-1])
    cipher_key = c_items[-1]
    cipher_key, d, n = int(cipher_key), int(d), int(n)
    aes_key = pow(cipher_key, d, n)
    aes = pyaes.AESModeOfOperationCTR(aes_key.to_bytes(16, sys.byteorder))
    decrypted = aes.decrypt(cipher_text)
    plain_text_file = open(plain_text, 'wb')
    plain_text_file.write(decrypted)
    plain_text_file.close()
    print("\nData has been decrypted successfully and stored in the file : %s" % plain_text)


def main():
    while True:
        print("\n***** WELCOME TO THE ENCRYPTION TOOL *****\n"
              "\n***** ENCRYPT YOUR DATA USING RSA + AES + STEGANOGRAPHY *****\n"
              "\n!!! IF YOU DON'T HAVE YOUR KEYS, PLEASE GENERATE THEM BEFORE PROCEEDING !!!\n"
              "\n***** CHOOSE FROM THE OPTIONS BELOW *****\n"
              "\n1. ENCRYPT"
              "\n2. DECRYPT"
              "\n3. EXIT")

        crypt_choice = int(input("\nEnter Your Choice : "))
        if crypt_choice == 1:
            encrypt_val, file_type = encrypt()
            stego_encrypt_choices(encrypt_val.hex(), file_type)
        elif crypt_choice == 2:
            encoded_data = stego_decrypt_choices()
            decrypt(encoded_data)
        elif crypt_choice == 3:
            print("\n***** THANK YOU FOR USING THE TOOL *****")
            break
        else:
            print("\nIncorrect Choice\n")


def stego_encrypt_choices(enc, file_type):
    print("\n***** CHOOSE THE STEGANOGRAPHY TECHNIQUE *****\n"
          "\n1. IMAGE STEGANOGRAPHY {Hiding Data in Image cover file}"
          "\n2. TEXT STEGANOGRAPHY {Hiding Data in Text cover file}"
          "\n3. AUDIO STEGANOGRAPHY {Hiding Data in Audio cover file}"
          "\n4. VIDEO STEGANOGRAPHY {Hiding Data in Video cover file}")

    stego_choice = int(input("\nEnter Your Choice: "))
    if stego_choice == 1:
        encode_img_data(enc, file_type)
    elif stego_choice == 2:
        encode_txt_data(enc, file_type)
    elif stego_choice == 3:
        encode_aud_data(enc, file_type)
    elif stego_choice == 4:
        encode_vid_data(enc, file_type)
    else:
        print("\nIncorrect Choice\n")
        stego_encrypt_choices(enc, file_type)


def stego_decrypt_choices():
    print("\n***** CHOOSE THE STEGANOGRAPHY TECHNIQUE *****\n"
          "\n1. IMAGE STEGANOGRAPHY {Hiding Data in Image cover file}"
          "\n2. TEXT STEGANOGRAPHY {Hiding Data in Text cover file}"
          "\n3. AUDIO STEGANOGRAPHY {Hiding Data in Audio cover file}"
          "\n4. VIDEO STEGANOGRAPHY {Hiding Data in Video cover file}")

    stego_choice = int(input("\nEnter Your Choice: "))
    if stego_choice == 1:
        return decode_img_data()
    elif stego_choice == 2:
        return decode_txt_data()
    elif stego_choice == 3:
        return decode_aud_data()
    elif stego_choice == 4:
        return decode_vid_data()
    else:
        print("\nIncorrect Choice\n")
        stego_decrypt_choices()


if __name__ == "__main__":
    main()
