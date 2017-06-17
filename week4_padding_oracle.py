#!/usr/bin/python3
# -*- coding: utf-8 -*-
# python_version: 3.4.0
__author__ = "mgraczyk"
__date__ = "2015-2-10"

import urllib
import urllib.error
import urllib.request
import multiprocessing.dummy
import operator
from itertools import islice
from itertools import repeat
from itertools import chain
from binascii import hexlify
from binascii import unhexlify


def grouper(iterable, n, fillvalue=None):
    """

    Collect data into fixed-length chunks or blocks

    >>>grouper('ABCDEFG', 3, 'x')
    'ABC DEF Gxx'
    """

    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class PaddingOracle(object):
    block_size = 16
    hex_block_size = 2 * block_size

    def __init__(self, target_url, ct):
        self._targetURL = target_url

        self._ct = ct

        self._numPTBlocks = int(len(self._ct)/self.block_size) - 1
        self._ptGuesses = [bytearray(self.block_size) for i in range(self._numPTBlocks)]


    def attack(self):
        # poolSZ = 64
        # pool = multiprocessing.Pool(poolSZ)

        for block in range(0, self._numPTBlocks):
            self._attack_block(block)

        return b''.join(self._ptGuesses)

    def _attack_block(self, block):
        pool_sz = 128
        pool = multiprocessing.dummy.Pool(pool_sz)

        for blockPos in reversed(range(self.block_size)):
            print("Guessing [{}][{}]".format(block, blockPos))

            res = pool.map(self.query,
                           ((islice(self._ct, block*self.block_size),
                             self._guess_block(block, blockPos, g),
                             islice(self._ct, (block+1)*self.block_size, (block+2)*self.block_size))
                            for g in range(128)))

            res = list(res)

            try:
                value = next(v for v, correct in enumerate(res) if correct)
            except StopIteration:
                print("Stopped")
                # This is the start of the pad at the end of the message
                value = next(v for v, correct in enumerate(res) if correct is None)

            print("Correctly guessed [{}][{}] = {}".format(block, blockPos, value))
            self._ptGuesses[block][blockPos] = value

    def _guess_block(self, block, block_pos, value):
        pad_len = self.block_size - block_pos
        ct_pos = block*self.block_size

        guess_block = self._ptGuesses[block][:]
        guess_block[block_pos:] = map(operator.xor, islice(guess_block, block_pos, None), repeat(pad_len))
        guess_block[block_pos] = guess_block[block_pos] ^ value
        guess_block[:] = map(operator.xor, islice(guess_block, None), islice(self._ct, ct_pos, ct_pos + self.block_size))

        return guess_block

    def query(self, parts):
        query_hex = hexlify(bytes(chain.from_iterable(parts)))
        target = self._targetURL + query_hex.decode("ascii")

        req = urllib.request.Request(target)

        try:
            status = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            status = e.code
            assert(status in (403, 404))
            return status == 404


def main():
    target_url = 'http://crypto-class.appspot.com/po?er='
    target = b'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
    po = PaddingOracle(target_url, unhexlify(target))
    pt = po.attack()
    print("Plain Text")
    print(pt.decode("ascii"))
    print("Plain Text Hex")
    print(hexlify(pt))


if __name__ == "__main__":
    main()