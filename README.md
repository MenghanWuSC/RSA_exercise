# RSA exercise
RSA exercise in Python. (use in **lab ONLY**)

## Environment
> Python 3.8.9 (default, Oct 26 2021, 07:25:53) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin

Third-party package:
- [PyCryptodome](https://pypi.org/project/pycryptodome/)
```
pip install pycryptodome
```

## Programs
There are two programs in this project:
1. genkeys.py
2. crypt.py

### Data structure
Exercise in this project represents a **simplified RSA** public-key cryptography.

- public key = [`N`, `e`] stored in decimal integer
- private key = [`N`, `d`] stored in decimal integer

For symmetric cipher usage (e.g. AES), refer to [PyCryptodome - Examples](https://www.pycryptodome.org/en/latest/src/examples.html).

### genkeys.py
To generate a RSA key pair (public/private) given an input user.
- `extended_gcd` function to yield **the greatest common divisor** (gcd) and **the coefficients** of Bézout's identity. Refer to [Extended Euclidean algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm)
- `inverse` function to find **the inverse** of given number under N modulo operation
- `genRandomRange` function to generate random **positive** integer within the range
- `PrimalityTest_Miller_Rabin` function to conduct primality test using **probabilistic** algorithm by _Miller-Rabin_. Refer to [Miller–Rabin primality test](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test)
- `genPrime` function to generate a **likely prime** in given byte size that passes primality test
- `find_p_q` function to find two prime p & q for RSA key preparation
- `compute_e_d` function to compute key pair e & d that satisfies **relatively prime**

Output files:
- {user}.pub
- {user}.prv

### crypt.py
To encrypt/decrypt a given inpute file using RSA (for KEK) and AES-128 (for contexts).
- `AES_encrypt_digest` function calling Library [PyCryptodome](https://www.pycryptodome.org/en/latest/src/examples.html) to encrypt and digest-MAC in EAX mode
- `AES_decrypt_verify` function calling Library [PyCryptodome](https://www.pycryptodome.org/en/latest/src/examples.html) to decrypt and verify-MAC in EAX mode
- `RSA_function` function to execute RSA (enc/dec) by required key pair [N, e/d]
- `getFileKey_16` function to get symmetric file key (16 bytes)

Output file:
- {file} in either ciphertext or plaintext

## Test

### genkeys.py
Given two users: {alice, bob} generate their key pairs and write into .pub & .prv files.
```
python genkeys.py alice
python genkeys.py bob
```
![genkeys](/img/genkeys.png)

### crypt.py
Given an input message file and generated key pairs of {alice, bob},
1. execute AES-128 encryption and write the results: **RSA encrypted file key** and ciphertext into file 
2. execute AES-128 decryption by using **RSA decrypted file key**, and write the plaintext into file
```
python crypt.py -e bob.pub message.txt message.cip
python crypt.py -d bob.prv message.cip message.txt
python crypt.py -e alice.pub message2.txt message2.cip
python crypt.py -d alice.prv message2.cip message2.txt
```
![crypt_01](/img/crypt_01.png)
![crypt_02](/img/crypt_02.png)
