# RSA exercise
RSA exercise in Python. (use in lab ONLY)

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
Exercise in this project represents a simplified RSA public-key cryptography.

- public key = [`N`, `e`] stored in decimal integer
- private key = [`N`, `d`] stored in decimal integer

For symmetric cipher usage (e.g. AES), refer to [PyCryptodome - Examples](https://www.pycryptodome.org/en/latest/src/examples.html).

### genkeys.py
To generate a RSA key pair (public/private) given an input user.

Output files:
- {user}.pub
- {user}.prv

### crypt.py
To encrypt/decrypt a given inpute file using RSA (for KEK) and AES-128 (for contexts).

Output file:
- {file} in either ciphertext or plaintext

## Test
