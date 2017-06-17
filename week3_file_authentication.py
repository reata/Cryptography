#!/usr/bin/python3
# -*- coding: utf-8 -*-
# python_version: 3.4.0
__author__ = "ryan"
__date__ = "2015-2-5"

"""
Suppose a web site hosts large video file F that anyone can download. Browsers who download the file need to make sure
the file is authentic before displaying the content to the user.
Certainly a collision resistant hash would make the trick. First browsers would download the entire file F, check that
H(F) is equal to the authentic hash value h and if so, display the video to the user. However, this means that video
will only begin playing after the *entire* file F has been downloaded.
Our goal in this project is to build a file authentication system that lets browsers authenticate and play video chunks
as they are downloaded without having to wait for the entire file.
"""

from Crypto.Hash import SHA256
import urllib.request
import os
import doctest

test_file_url = "https://class.coursera.org/crypto-013/lecture/download.mp4?lecture_id=28"
target_file_url = "https://class.coursera.org/crypto-013/lecture/download.mp4?lecture_id=27"


def download_file(url, file_name):
    """
    (string, string) -> none

    download files from web and store in local environment

    :param url: the url to the file to be downloaded
    :param file_name: the local file name
    :return: none
    """
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        data = response.read()
        out_file.write(data)


def file_authentication(file_path):
    """
    string -> string

    cut the files into 1kb blocks, start from the last block, hash it and append the hash value to the second last
    block, then every blocks will be hashed with the hash value of next block's hash value appended. Finally, we will
    get the h0 value of the 0th block.

    >>> file_authentication("resources/6 - 2 - Generic birthday attack (16 min).mp4")
    '03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8'

    :param file_path: the path to the file to be hashed
    :return: the h0 hash result.
    """
    block_size = 1024
    blocks = []
    with open(file_path, 'rb') as file:
        buf = file.read(block_size)
        while len(buf) > 0:
            blocks.append(buf)
            buf = file.read(block_size)
    file.close()
    n = len(blocks)
    last_block = blocks[n-1]
    h = SHA256.new()
    h.update(last_block)
    while n >= 2:
        message = blocks[n-2] + h.digest()
        h = SHA256.new()
        h.update(message)
        n -= 1
    result = h.hexdigest()
    return result


def main():
    if not os.path.isfile("resources/6 - 2 - Generic birthday attack (16 min).mp4"):
        download_file(test_file_url, 'resources/6 - 2 - Generic birthday attack (16 min).mp4')
    if not os.path.isfile("resources/6 - 1 - Introduction (11 min).mp4"):
        download_file(target_file_url, "resources/6 - 1 - Introduction (11 min).mp4")
    print(file_authentication("resources/6 - 1 - Introduction (11 min).mp4"))


if __name__ == "__main__":
    doctest.testmod()
    main()