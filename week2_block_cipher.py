#!/usr/bin/python3
# -*- coding: utf-8 -*-
# python_version: 3.4.0
__author__ = "ryan"
__date__ = "2015-1-22"

"""
This project implements two decryption systems with library PyCrypto, one using AES in CBC(Chained Block Cipher) mode
and another using AES in CTR(counter) mode. In both cases the 16-byte encryption IV is chosen at random and is prepended
to the ciphertext. For CBC encryption we use the PKCS5 padding scheme.
"""

from Crypto.Cipher import AES
from Crypto.Util import Counter
import binascii

# the first two elements of keys and ciphertexts are from CBC mode while the latter two from CTR mode
keys = ["140b41b22a29beb4061bda66b6747e14",
        "140b41b22a29beb4061bda66b6747e14",
        "36f18357be4dbd77f050515c73fcf9f2",
        "36f18357be4dbd77f050515c73fcf9f2"]
ciphertexts =["4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81",
              "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253",
              "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329",
              "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"]
block_size = AES.block_size


def decrypt_cbc(ciphertext, key):
    """
    (bytes, bytes) -> string

    Perform AES CBC decryption with PKCS5 Padding. Decrypt ciphertext with key(both are turned into bytes from hex
    encoded string) into plaintext

    :param ciphertext: ciphertext to be decrypted
    :param key: the decryption key
    :return: the plaintext
    """
    iv = ciphertext[:block_size]
    new_cipher = ciphertext[block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(new_cipher)
    plaintext = str(plaintext, 'ascii')
    # Pad logic from http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
    plaintext = plaintext[:-ord(plaintext[-1])]
    return plaintext


def decrypt_ctr(ciphertext, key):
    """
    (bytes, bytes) -> string

    Perform AES CTR decryption using Counter mechanism. We are using the Counter functionality from Crypto.Util.Counter.
    Decrypt ciphertext with key(both are turned into bytes from hex encoded) into plaintext

    :param ciphertext: ciphertext to be decrypted
    :param key: the decryption key
    :return: the plaintext
    """
    iv = ciphertext[:block_size]
    ctr = Counter.new(128, initial_value=int(binascii.hexlify(iv), 16))
    new_cipher = ciphertext[block_size:]
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    plaintext = cipher.decrypt(new_cipher)
    plaintext = str(plaintext, 'ascii')
    return plaintext


def main():
    key_unhex = [binascii.unhexlify(element) for element in keys]
    cipher_text_unhex = [binascii.unhexlify(element) for element in ciphertexts]
    plaintext1 = decrypt_cbc(cipher_text_unhex[0], key_unhex[0])
    plaintext2 = decrypt_cbc(cipher_text_unhex[1], key_unhex[1])
    plaintext3 = decrypt_ctr(cipher_text_unhex[2], key_unhex[2])
    plaintext4 = decrypt_ctr(cipher_text_unhex[3], key_unhex[3])
    print("Answers for Q1:", plaintext1, '\n')
    print("Answers for Q2:", plaintext2, '\n')
    print("Answers for Q3:", plaintext3, '\n')
    print("Answers for Q4:", plaintext4, '\n')


if __name__ == "__main__":
    main()