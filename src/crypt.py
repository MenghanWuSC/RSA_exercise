#!/usr/bin/python3

import sys, argparse, os, typing
from Crypto.Cipher import AES


def AES_encrypt_digest(key:bytes, plaintext:bytes) -> typing.Tuple[bytes, bytes, bytes]:
    """
    Library 'PyCryptodome' to encrypt and digest-MAC in EAX mode
    Return: (nonce, ciphertext, tag) in bytes
    """
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return (nonce, ciphertext, tag)


def AES_decrypt_verify(key:bytes, nonce:bytes, ciphertext:bytes, tag:bytes) -> bytes:
    """
    Library 'PyCryptodome' to decrypt and verify-MAC in EAX mode
    Return: decrypted plaintext in bytes
    """
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


def RSA_function(base:bytes, pair:typing.Tuple[int,int]) -> bytes:
    """
    Execute RSA function (enc/dec) by required key pair [N, e/d]
    Return: results in bytes
    """
    assert base != None and pair != None
    # Convert bytes to int for calculation 
    baseInt = int.from_bytes(base, byteorder='big', signed=False)
    # Execute RSA encryption: m^e mod N
    func_baseInt = pow(baseInt, pair[1], pair[0])
    # Recover int to bytes for storage
    func_base = func_baseInt.to_bytes((func_baseInt.bit_length()+7) // 8, byteorder='big', signed=False)
    return func_base


def getFileKey_16(encrypted:str=None, prvKey:typing.Tuple[int,int]=None) -> bytes:
    """
    Get symmetric file key (16 bytes) by:
        1. Generate a random one
        2. Execute RSA decryption by required private key to get one
    Return: plain file key in 16 bytes
    """
    getKey = None
    # 1. Generate a random file key in 
    if encrypted == None:
        getKey = os.urandom(16)
    # 2. Execute RSA decryption to recover the file key
    else:
        assert prvKey != None
        # Convert encrypted hex string to bytes
        encryptedBytes = bytes.fromhex(encrypted)
        getKey = RSA_function(encryptedBytes, prvKey)
    return getKey


def main():
    # Initialization: argparse
    parser = argparse.ArgumentParser()
    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--encrypt", metavar=".pub", help="execute encryption")
    group.add_argument("-d", "--decrypt", metavar=".prv", help="execute decryption")
    # Require positional arguments
    parser.add_argument("input", help="read from file as input")
    parser.add_argument("output", help="write to file as output")
    # Convert argument strings to objects
    args = parser.parse_args()
    # To be used variables
    N = None
    e = None
    d = None
    fileKey = None
    # Depend on conditions:
    # [-e .pub] input output
    if args.encrypt:
        # Prepare necessary parameters: pubKey[N,e]
        with open(args.encrypt, mode='r') as filePtr:
            for line in filePtr:
                lineList = line.split(" ")
                if lineList[0] == 'N':
                    N = int(lineList[2])
                elif lineList[0] == 'e':
                    e = int(lineList[2])
                else:
                    continue
        assert N != None and e != None
        fileKey = getFileKey_16()
        # Input contexts from file
        with open(args.input, mode='r') as filePtr:
            fileText = filePtr.read()
        fileBytes = fileText.encode(encoding='utf-8')
        # Execute AES encryption for contexts
        (nonce, enc_fileBytes, tag) = AES_encrypt_digest(fileKey, fileBytes)
        # Output results in hex to file
        with open(args.output, mode='w') as filePtr:
            # Line:(0) encrypted file key
            enc_fileKey = RSA_function(fileKey, (N,e))
            filePtr.write(enc_fileKey.hex()+" \n")
            # Line:(1) nonce
            filePtr.write(nonce.hex()+" \n")
            # Line:(2) ciphertext of AES
            filePtr.write(enc_fileBytes.hex()+" \n")
            # Line:(3) MAC tag
            filePtr.write(tag.hex()+" \n")
        sys.exit(0)
    # [-d .prv] input output
    elif args.decrypt:
        # Prepare necessary parameters: prvKey[N,d]
        with open(args.decrypt, mode='r') as filePtr:
            for line in filePtr:
                lineList = line.split(" ")
                if lineList[0] == 'N':
                    N = int(lineList[2])
                elif lineList[0] == 'd':
                    d = int(lineList[2])
                else:
                    continue
        assert N != None and d != None
        # Parse the input file for stored info in hex
        with open(args.input, mode='r') as filePtr:
            # Line:(0) encrypted file key
            lineList = filePtr.readline().split(" ")
            fileKey = getFileKey_16(lineList[0], (N,d))
            # Line:(1) nonce
            lineList = filePtr.readline().split(" ")
            nonce = bytes.fromhex(lineList[0])
            # Line:(2) ciphertext of AES
            lineList = filePtr.readline().split(" ")
            enc_fileBytes = bytes.fromhex(lineList[0])
            # Line:(3) MAC tag
            lineList = filePtr.readline().split(" ")
            tag = bytes.fromhex(lineList[0])
        # Execute AES decryption for contexts
        fileBytes = AES_decrypt_verify(fileKey, nonce, enc_fileBytes, tag)
        fileText = fileBytes.decode(encoding='utf-8')
        # Output results in hex to file
        with open(args.output, mode='w') as filePtr:
            filePtr.write(fileText)
        sys.exit(0)
    else:
        # Exception handler: none [-e | -d]
        parser.print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
