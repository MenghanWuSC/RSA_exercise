#!/usr/bin/python3

import sys, os, typing


def extended_gcd(num1:int, num2:int) -> typing.Tuple[int, int, int]:
    """
    Find GCD and coefficients
        r = gcd(a, b) = a x + b y
    e.g. num1, num2 = 240, 46
        gcd = -9 * 240 + 47 * 46 = 2
    Return: [r, x, y] in integer
    """
    a, b   = num1, num2
    x, y   = 0, 1
    lx, ly = 1, 0
    while b != 0:
        q = a // b
        a, b = b, a % b
        x, lx = (lx - (q * x)), x
        y, ly = (ly - (q * y)), y
    # Results: gcd = a, coefficients = (lx, ly)
    return (a, lx, ly)


def inverse(number:int, N:int) -> int:
    """
    Find the inverse of given number under N modulo operation
    Return: inverse 'positive' value OR Exception:ValueError
    """
    (gcd, found, _) = extended_gcd(number, N)
    # Should satisfy 'coprime integers'
    if gcd != 1:
        # Exception handler: to notify re-finding p & q
        raise ValueError
    # Consider positive integers
    if found < 0:
        found += N
    return found


def genRandomRange(min:int, max:int) -> int:
    """
    To generate random 'positive' integer within the range
    Return: minimum ~ maximum
    """
    # Pre-condition
    if min == max:
        return min
    assert min < max
    # Given the maximum to render the needed bytes
    (maxByteSize, leftBits) = divmod(max.bit_length(), 8)
    # To address conditions
    if leftBits != 0:
        maxByteSize += 1
    # Loop finding that satisfies the given range
    while True:
        randomData = os.urandom(maxByteSize)
        randomInt = int.from_bytes(randomData, byteorder="big", signed=False)
        if min <= randomInt and randomInt <= max:
            break
    return randomInt


def PrimalityTest_Miller_Rabin(n:int) -> bool:
    """
    Primality test using 'probabilistic' algorithm by Miller-Rabin
        Optimization with minimum k rounds
    Return: True/False
    """
    # Pre-condition: screen out even numbers
    if n < 2:
        return False
    elif n & 1 == 0:
        return False
    # 1. Decide minimum k rounds with error probability (FIPS 186-4 Appendix C)
    nBitSize = n.bit_length()
    if nBitSize >= 1536:
        k = 4
    elif nBitSize >= 1024:
        k = 5
    elif nBitSize >= 512:
        k = 6
    else:
        k = 8
    # 2. *Miller-Rabin probabilistic primality test
    # Write n as (2^r)*d + 1 with d odd
    # --by factoring out powers of 2 from n − 1
    d = n - 1
    r = 0
    while (d & 1) == 0:
        r += 1
        d >>= 1
    # Witness Loop for decided 'k' rounds
    for _ in range(k):
        # Pick a random integer within the range [2, n−2]
        a = genRandomRange(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
                # Continue Witness Loop
        else:
            # Run through the inner loop -> n is tested composite
            return False
    # Probably 'prime'
    return True


def genPrime(byteSize:int) -> int:
    """
    To generate a prime in given byte size
    Return: positive prime integer
    """
    # Loop finding available prime
    while True:
        randomData = os.urandom(byteSize)
        randomInt = int.from_bytes(randomData, byteorder="big", signed=False)
        # Primality test: Miller-Rabin
        if PrimalityTest_Miller_Rabin(randomInt):
            break
    assert randomInt > 0
    return randomInt


def find_p_q(byteSize:int=128) -> typing.Tuple[int, int]:
    """
    To find two prime p & q for RSA key preparation
        Default each holds 1024 bits = 128 bytes
    Return: [p, q] in integer
    """
    p = genPrime(byteSize)
    q = genPrime(byteSize)
    while p == q:
        # Simplified: change p only
        p = genPrime(byteSize)
    return (p, q)


def compute_e_d(p:int, q:int, e:int=65537) -> typing.Tuple[int, int]:
    """
    To compute key pair e & d that satisfies "relatively prime"
        Recommended e = 65537 = 2^16 + 1
    Return: [e, d] in integer
    """
    phi_n = (p-1) * (q-1)
    try:
        d = inverse(e, phi_n)
    except ValueError:
        # Exception handler: to notify re-finding p & q
        raise ValueError
    return (e, d)


def main():
    try:
        inputString = sys.argv[1]
        if len(sys.argv) != 2: raise IndexError
    except:
        print("\nUsage:")
        print("\t./genkeys.py alice")
        sys.exit(1)
    # 1. Prepare necessary parameters: [p, q, e, d] for RSA key preparation
    while True:
        # Find two prime p & q, default each holds 1024 bits = 128 bytes
        (p, q) = find_p_q()
        # Compute key pair e & d that satisfies "relatively prime"
        try:
            (e, d) = compute_e_d(p, q)
            break
        except ValueError:
            # Re-find two prime p & q
            continue
    # 2. Prepare key pair: public [N, e] & private [N, d]
    N = p * q
    pubKey = [N, e]
    prvKey = [N, d]
    # 3. Output to files for storage '*.pub' '*.prv'
    with open(inputString+".pub", mode='w') as filePtr:
        filePtr.write("*** BEGIN PUBLIC KEY BLOCK *** \n")
        filePtr.write("N = " + str(pubKey[0]) + " \n")
        filePtr.write("e = " + str(pubKey[1]) + " \n")
        filePtr.write("*** END PUBLIC KEY BLOCK *** \n")
    with open(inputString+".prv", mode='w') as filePtr:
        filePtr.write("*** BEGIN PRIVATE KEY BLOCK *** \n")
        filePtr.write("N = " + str(prvKey[0]) + " \n")
        filePtr.write("d = " + str(prvKey[1]) + " \n")
        filePtr.write("*** END PRIVATE KEY BLOCK *** \n")


if __name__ == "__main__":
    main()
