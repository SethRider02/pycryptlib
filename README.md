# pycryptlib

Multiple cryptologic functions ranging from a simple caesar cipher up to AES!

[![PyPI](https://img.shields.io/pypi/v/pycryptlib)](https://pypi.org/project/pycryptlib/)
[![Python](https://img.shields.io/pypi/pyversions/pycryptlib)](https://pypi.org/project/pycryptlib/)
[![License](https://img.shields.io/pypi/l/pycryptlib)](LICENSE)

> **Security notice:** This library has not been independently audited.
> It is intended for learning and experimentation. For production systems,
> use a well-established library such as `cryptography`.

## Features

- Affine Cipher
- Viginere Cipher
- LFSR
- KidRSA
- RSA
- DES
- AES (NEW!)

## Installation

```bash
pip install cgacryptpy
```

Requires Python 3.9 or newer.

## Update
```bash
pip update cgacrypt
```

## Quick start

```python
from pycryptlib.lfsr import lfsr_encrypt

seed_3 = [1,0,0,0,1]

ciphertext, keystream = lfsr_encrypt("ACADEMY", seed_3)
print("7. Ciphertext bits:", ciphertext)
print("7. Keystream:", keystream)


## Supported algorithms

| Algorithm | Module |     Notes     |
|-----------|--------|---------------|
| DES       | `pycryptlib.des`       | 64-bit keys         |
| LSFR      | `pycryptlib.lsfr`      |                     |
| Classical | `pycryptlib.classical` | Caesar, stream, etc |
| KidRSA    | `pycryptlib.rsa`       |
|   RSA     | `pycryptlib.rsa`       |

## Feedback / Security Concerns
If you have any concerns regarding usage or issues (ie. function not working or not helpful explanation.),
feel free to email me or message me at sethrider02@gmail.com

## Development

```bash
git clone https://github.com/SethRider02/pycryptlib
cd pycryptlib
pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).