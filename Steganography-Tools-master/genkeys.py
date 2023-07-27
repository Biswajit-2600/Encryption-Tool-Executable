import os.path
import random
import sys
from tkinter import *
from tkinter import filedialog


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def find_mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def rabin_miller(num):
    s = num - 1
    t = 0

    while s % 2 == 0:
        s = s // 2
        t += 1
    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
        return True


def is_prime(num):
    if num < 2:
        return False
    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                  103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                  211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                  331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                  449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                  587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                  709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                  853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                  991, 997]

    if num in low_primes:
        return True
    for prime in low_primes:
        if num % prime == 0:
            return False
    return rabin_miller(num)


def generate_large_prime(key_size=1024):
    while True:
        num = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if is_prime(num):
            return num


def generate_key(key_size):
    p = generate_large_prime(key_size)
    q = generate_large_prime(key_size)
    n = p * q
    t = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if gcd(e, t) == 1:
            break

    d = find_mod_inverse(e, t)
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key


def make_key_files(user_name, key_size):
    public_key, private_key = generate_key(key_size)

    directory_window = Tk()
    directory_window.withdraw()

    selected_directory = filedialog.askdirectory()
    if not selected_directory:
        raise

    pub_file_path = f"{selected_directory}/{user_name}.pub"
    pub_file = open(pub_file_path, 'w+')
    pub_file.write('%s,%s' % (public_key[0], public_key[1]))
    pub_file.close()

    prv_file_path = f"{selected_directory}/{user_name}.prv"
    prv_key = open(prv_file_path, 'w+')
    prv_key.write('%s,%s' % (private_key[0], private_key[1]))
    prv_key.close()


if __name__ == '__main__':
    size = 1024
    name = ""
    if len(sys.argv) > 1:
        name = sys.argv[1]
    if os.path.exists('%s.pub' % name) and os.path.exists('%s.prv' % name):
        if sys.argv[2] == "1":
            make_key_files(name, size)
        else:
            raise FileExistsError
    else:
        make_key_files(name, size)
    # print("\n!!! THE PUBLIC AND PRIVATE KEYS HAVE BEEN GENERATED !!!\n"
    #       "\n!!! THEY HAVE BEEN STORED IN THE RESPECTIVE FILES IN THE SAME DIRECTORY !!!\n"
    #       "\n!!! KEEP THE PRIVATE KEY SAFE AND \"SECRET\" !!!\n"
    #       "\n!!! YOU CAN SHARE THE PUBLIC KEY TO ANYONE TO PERFORM THE ENCRYPTION !!!")
